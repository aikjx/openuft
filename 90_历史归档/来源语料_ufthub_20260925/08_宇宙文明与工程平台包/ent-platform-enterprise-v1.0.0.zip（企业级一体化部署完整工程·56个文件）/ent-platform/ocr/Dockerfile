# =============================================================================
# OCR 服务镜像 —— 双引擎构建
#   --build-arg OCR_ENGINE=paddle : 飞桨 PaddleOCR (x86_64 默认, 精度高, 可GPU)
#   --build-arg OCR_ENGINE=rapid  : RapidOCR/ONNX Runtime (amd64/arm64 全兼容, 信创默认)
# =============================================================================
ARG PYTHON_TAG=3.10-slim
FROM python:${PYTHON_TAG}

ARG OCR_ENGINE=paddle
ENV OCR_ENGINE=${OCR_ENGINE} \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Asia/Shanghai

# 运行期系统依赖: libgl/libglib(OpenCV) 中文字体(截图中文渲染/识别环境一致)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 libgomp1 \
        fonts-noto-cjk fonts-wqy-zenhei \
        ca-certificates wget tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 按引擎装依赖 (国内构建可加 -i https://pypi.tuna.tsinghua.edu.cn/simple)
COPY requirements-common.txt ./
COPY requirements-paddle.txt requirements-rapid.txt ./
RUN set -eux; \
    pip install -r requirements-common.txt; \
    if [ "$OCR_ENGINE" = "paddle" ]; then \
        pip install -r requirements-paddle.txt ; \
    else \
        pip install -r requirements-rapid.txt ; \
    fi

COPY app/ ./app/

# 模型目录通过 volume 挂载到 /root/.paddleocr (PaddleOCR 默认下载位置), 避免重建重下
ENV OCR_MODEL_DIR=/root/.paddleocr
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
