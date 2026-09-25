# =============================================================================
# 常驻 Headless Chromium 浏览器服务
# 基础镜像为官方 Playwright (amd64/arm64 均有), 已含 Chromium 与全部系统库
# Worker 通过 CDP http://browser:9222 远程连接, 浏览器只启动一次、常驻复用
# =============================================================================
ARG PLAYWRIGHT_TAG=v1.48.0-jammy
FROM mcr.microsoft.com/playwright:${PLAYWRIGHT_TAG}

ENV TZ=Asia/Shanghai \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /app

# 中文字体(否则截图中文为方块); 镜像已含大部分依赖, 这里只补字体
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-noto-cjk fonts-wqy-zenhei wget \
    && rm -rf /var/lib/apt/lists/*

COPY start-browser.sh /app/start-browser.sh
RUN chmod +x /app/start-browser.sh

EXPOSE 9222
CMD ["/app/start-browser.sh"]
