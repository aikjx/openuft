"""
OCR HTTP 服务 (FastAPI)
=======================
双引擎统一封装:
  - paddle : PaddleOCR (飞桨), x86_64 默认, 精度高, 支持 GPU
  - rapid  : RapidOCR(ONNX), amd64/arm64 全兼容, 信创 ARM 默认

接口:
  GET  /health              健康检查 + 引擎信息
  POST /ocr                 识别单图
       参数方式1(最高性能, 同机推荐): json {"path": "/data/xxx.png"} 走共享卷
       参数方式2(跨机通用):           multipart/form-data 字段 file 上传
  POST /ocr/batch           批量识别(共享卷路径列表), GPU/CPU 吞吐最优用法

设计要点:
  1. 模型在启动时一次性加载并预热, 禁止每请求 new 模型(冷加载数秒)
  2. PaddleOCR 实例非线程安全: uvicorn 单 worker + 内部串行, 高并发靠扩容器副本
"""
import os
import time
import threading
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io

ENGINE = os.getenv("OCR_ENGINE", "paddle").lower()
LANG = os.getenv("OCR_LANG", "ch")
MODEL_DIR = os.getenv("OCR_MODEL_DIR", "/root/.ocr-models")
os.makedirs(MODEL_DIR, exist_ok=True)

app = FastAPI(title="ent-ocr", version="1.0.0")
_lock = threading.Lock()      # 串行化推理, 保护非线程安全引擎
_engine_obj = None


# ------------------------------------------------------------------ 引擎加载
def _build_engine():
    """启动时构建一次引擎对象"""
    if ENGINE == "paddle":
        from paddleocr import PaddleOCR
        use_gpu = os.getenv("USE_GPU", "false").lower() == "true"
        # 模型默认下载到 /root/.paddleocr, compose 已把该目录挂到 data/ocr-models
        return PaddleOCR(
            use_angle_cls=True,
            lang=LANG,
            use_gpu=use_gpu,
            show_log=False,
        )
    elif ENGINE == "rapid":
        from rapidocr_onnxruntime import RapidOCR
        return RapidOCR()
    raise RuntimeError(f"unknown OCR_ENGINE: {ENGINE}")


@app.on_event("startup")
def _warmup():
    """启动预热: 用 1x1 空白图走一遍完整链路, 首请求不再承担加载开销"""
    global _engine_obj
    t0 = time.time()
    _engine_obj = _build_engine()
    dummy = (np.ones((32, 128, 3), dtype=np.uint8) * 255)
    with _lock:
        _infer(dummy)
    print(f"[OCR] engine={ENGINE} warmup done in {time.time()-t0:.2f}s", flush=True)


# ------------------------------------------------------------------ 统一推理
def _infer(img: np.ndarray):
    """返回 [{'text':..,'conf':..,'box':[[x,y],...]}, ...]"""
    out = []
    if ENGINE == "paddle":
        raw = _engine_obj.ocr(img, cls=True)
        for page in raw or []:
            if not page:
                continue
            for line in page:
                box, (text, score) = line[0], line[1]
                out.append({"text": text, "conf": round(float(score), 4),
                            "box": [[float(x), float(y)] for x, y in box]})
    else:  # rapid
        result, _ = _engine_obj(img)
        if result:
            for box, text, score in result:
                out.append({"text": text, "conf": round(float(score), 4),
                            "box": [[float(x), float(y)] for x, y in box]})
    return out


def _load_image(path: Optional[str] = None, upload: Optional[bytes] = None) -> np.ndarray:
    if path:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        return np.array(Image.open(path).convert("RGB"))
    return np.array(Image.open(io.BytesIO(upload)).convert("RGB"))


class OcrPath(BaseModel):
    path: str


class OcrBatch(BaseModel):
    paths: List[str]


# ------------------------------------------------------------------ 路由
@app.get("/health")
def health():
    return {"status": "ok", "engine": ENGINE, "lang": LANG}


@app.post("/ocr")
async def ocr_one(body: Optional[OcrPath] = None, file: UploadFile = File(None)):
    t0 = time.time()
    try:
        if body is not None and body.path:
            img = _load_image(path=body.path)
        elif file is not None:
            img = _load_image(upload=await file.read())
        else:
            return JSONResponse(status_code=400,
                                content={"msg": "need json.path or multipart file"})
        with _lock:
            lines = _infer(img)
        return {
            "engine": ENGINE,
            "elapsed_ms": int((time.time() - t0) * 1000),
            "line_count": len(lines),
            "text": "\n".join(x["text"] for x in lines),
            "lines": lines,
        }
    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"msg": f"file not found: {e}"})
    except Exception as e:  # noqa
        return JSONResponse(status_code=500, content={"msg": f"{type(e).__name__}: {e}"})


@app.post("/ocr/batch")
def ocr_batch(body: OcrBatch):
    """批量识别: 共享卷路径列表, 一次请求串行处理, 省掉反复 HTTP/序列化开销"""
    t0 = time.time()
    results = []
    with _lock:
        for p in body.paths:
            item = {"path": p}
            try:
                lines = _infer(_load_image(path=p))
                item.update(line_count=len(lines),
                            text="\n".join(x["text"] for x in lines),
                            lines=lines)
            except Exception as e:  # noqa
                item.update(error=f"{type(e).__name__}: {e}")
            results.append(item)
    return {"engine": ENGINE, "total": len(body.paths),
            "elapsed_ms": int((time.time() - t0) * 1000), "results": results}
