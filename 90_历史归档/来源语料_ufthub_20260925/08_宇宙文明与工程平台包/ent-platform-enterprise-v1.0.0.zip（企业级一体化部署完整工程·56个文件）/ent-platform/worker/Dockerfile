# =============================================================================
# Python 自动化 Worker 镜像
# 只装 Playwright 客户端库, 不下载浏览器 (浏览器在独立 browser 容器中常驻)
# =============================================================================
ARG PYTHON_TAG=3.10-slim
FROM python:${PYTHON_TAG}

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-noto-cjk fonts-wqy-zenhei ca-certificates tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && rm -rf /var/lib/apt/lists/*

# 关键: 跳过本地浏览器下载, Worker 只通过 CDP 连接 browser 容器
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/ ./app/
CMD ["python", "-u", "app/main.py"]
