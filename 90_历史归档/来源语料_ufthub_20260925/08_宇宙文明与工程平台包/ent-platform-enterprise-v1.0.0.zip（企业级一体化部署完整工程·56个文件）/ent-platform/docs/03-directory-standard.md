# 03 · 目录规范

## 1. 标准安装路径（强制约定，便于交接与运维）

| 平台 | 标准路径 | 说明 |
|---|---|---|
| Linux | `/opt/ent-platform/` | 企业惯例，独立于业务用户家目录 |
| Windows | `D:\ent-platform\` | 不要放 C 盘桌面，避免数据占满系统盘 |

## 2. 完整目录树与每个文件的作用

```
ent-platform/
├── README.md                     # 总入口(先读它)
├── VERSION                       # 工程版本
├── docker-compose.yml            # 【唯一编排入口】7 个服务全部在此
├── docker-compose.gpu.yml        # NVIDIA GPU 覆盖文件(USE_GPU=1 时叠加)
├── .env.example                  # 环境变量样板
├── .env                          # 实际配置(install 生成, chmod600, 不随包分发)
│
├── mysql/
│   ├── conf/my.cnf               # MySQL 8 调优配置(内存参数由 tune-memory 改写)
│   └── init/01-init.sql          # 首启自动执行: 建 rpa_task 表
├── redis/
│   └── conf/redis.conf           # Redis 调优(AOF/淘汰策略/慢日志)
├── nginx/
│   ├── nginx.conf                # 主配置(worker/gzip/upstream/限流)
│   ├── conf.d/backend.conf       # 业务站点(/api 反代 Java、静态、健康检查)
│   └── certs/                    # (自建)放 HTTPS 证书
│
├── ocr/                          # OCR 识别服务
│   ├── Dockerfile                # CPU 双引擎镜像(paddle/rapid 构建参数切换)
│   ├── Dockerfile.gpu            # GPU 镜像(CUDA11.8+cudnn8)
│   ├── requirements-common.txt   # FastAPI/Pillow 等公共依赖
│   ├── requirements-paddle.txt   # 飞桨版本锁定(版本必须配对)
│   ├── requirements-rapid.txt    # ONNX 跨架构依赖(信创 ARM 用)
│   └── app/main.py               # OCR HTTP 服务: /health /ocr /ocr/batch
│
├── browser/                      # 常驻无头浏览器
│   ├── Dockerfile                # 基于官方 Playwright 镜像 + 中文字体
│   └── start-browser.sh          # 找 Chromium 并以 CDP 9222 常驻
│
├── worker/                       # Python 自动化 Worker
│   ├── Dockerfile
│   ├── requirements.txt          # playwright(仅客户端)/redis/pymysql/requests
│   └── app/
│       ├── main.py               # 队列消费+浏览器操控+OCR调用+落库 全链路
│       └── task_example.json     # 任务报文样例(投队列验证用)
│
├── backend/                      # Java 后端
│   ├── Dockerfile                # JDK17 JRE 运行 app.jar
│   ├── app.jar                   # 【你自己放】Spring Boot 可执行 jar
│   └── README.md                 # 接入步骤
│
├── scripts/                      # 全部运维脚本(零依赖, bash+powershell 双份)
│   ├── lib/common.sh             # 公共函数(架构探测/compose 封装/日志着色)
│   ├── check-env.sh / .ps1       # 环境自检
│   ├── install.sh / .ps1         # ★ 一键部署
│   ├── control.sh / .ps1         # start/stop/restart/status/logs/rebuild/shell
│   ├── tune-memory.sh            # 按宿主机内存自动调 MySQL/Redis
│   ├── backup.sh / restore.sh    # 备份/恢复
│   ├── build-multiarch.sh        # x86+arm64 双架构构建推送
│   ├── offline-save.sh           # 制作离线交付包
│   └── offline-load.sh           # 内网导入离线包并部署
│
├── data/                         # ★ 所有持久化数据(备份/迁移就操作它)
│   ├── mysql/                    # MySQL 数据文件
│   ├── redis/                    # Redis AOF/RDB
│   ├── shared/                   # 截图共享卷(三容器同挂, 路径传参)
│   ├── ocr-models/               # OCR 模型缓存(避免重复下载)
│   ├── static/                   # Nginx 静态站点文件
│   └── uploads/                  # 后端上传目录
├── logs/
│   ├── nginx/  backend/  worker/ # 各组件文件日志
├── backup/                       # backup.sh 输出(保留14天)
├── packages/                     # 离线包输出目录
└── docs/                         # 全套文档 + 图形架构图
```

## 3. 目录使用铁律

1. **数据只进 `./data/`**：任何容器要持久化的东西都 bind mount 到 `./data/`，`docker compose down`、删容器、升级镜像都不丢数据。
2. **配置只改 `.env` 和三个 conf**：不要进容器改配置，容器重建即丢。
3. **日志统一 `./logs/`**：容器内 stdout 同时被 docker 收集（`docker logs`），文件日志落 `./logs/`。
4. **备份只备 `./data/` + 逻辑备份包**：整机迁移 = 停服 → 打包整个目录 → 新机器解压 → `up -d`。
5. **一个环境一份目录**：测试/生产各放一份，不要共用 `data/`。
