# 企业级一体化平台 · 一键部署工程

> Nginx + Java(Spring Boot) + MySQL + Redis + Python 自动化 Worker(RPA/IP任务) + Headless Chromium + OCR(飞桨/RapidOCR)
> 一套工程，**Windows / Linux 通吃，x86_64 / ARM64(鲲鹏、飞腾) 原生兼容，支持信创内网离线交付**。

---

## 1. 30 秒快速开始

### Linux（Ubuntu/Debian/麒麟/统信/CentOS/openEuler）
```bash
# 1. 解压工程并放到标准目录(推荐)
sudo mkdir -p /opt && sudo tar -xzf ent-platform.tar.gz -C /opt && cd /opt/ent-platform
# 2. 环境自检(可选但推荐)
bash scripts/check-env.sh
# 3. 一键部署(没装 Docker 会自动装)
sudo bash scripts/install.sh
```

### Windows（Docker Desktop + WSL2）
```powershell
# 管理员 PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force
cd D:\ent-platform
.\scripts\check-env.ps1
.\scripts\install.ps1
```

部署完成后：浏览器打开 `http://服务器IP/healthz` 看到 `ok` 即成功。

### 离线/信创内网
1. 在**与目标服务器相同 CPU 架构**的联网机器上：`bash scripts/offline-save.sh`
2. 把 `packages/ent-offline-<arch>-日期.tar.gz` 拷进内网
3. 目标机：`bash scripts/offline-load.sh <离线包>`

---

## 2. 文档索引（按顺序读）

| 文档 | 内容 | 什么时候看 |
|---|---|---|
| **docs/architecture.html** | 架构图 + 部署拓扑图（浏览器直接打开，图形版） | 先看，建立全局认识 |
| [01-架构设计.md](docs/01-architecture.md) | 分层架构、组件职责、关联关系、任务时序 | 理解为什么这么拆 |
| [02-部署拓扑.md](docs/02-deployment.md) | 容器/网络/端口/卷/数据流向部署图 | 部署、画交付架构图 |
| [03-目录规范.md](docs/03-directory-standard.md) | 每个目录放什么、标准安装路径 | 找文件、交接 |
| [04-安装部署手册.md](docs/04-install-guide.md) | 在线/离线/GPU/多机/开机自启全流程 | 正式部署 |
| [05-配置详解.md](docs/05-config-reference.md) | .env 每项含义 + 最优默认值 + 按机器规格调优 | 改配置 |
| [06-运维手册.md](docs/06-operations.md) | 启停、备份恢复、扩容、升级、日志、巡检 | 日常运维 |
| [07-故障排查手册.md](docs/07-troubleshooting.md) | 90% 常见问题的现象-原因-解决 | 出问题 |
| [08-信创国产化适配.md](docs/08-localization-xinchuang.md) | 麒麟/统信/鲲鹏/飞腾/海光/龙芯、国产库替代 | 信创项目 |
| [09-安全加固手册.md](docs/09-security.md) | 端口、密码、HTTPS、网络隔离、审计 | 上线前 |

---

## 3. 兼容性矩阵

| 维度 | 兼容范围 | 说明 |
|---|---|---|
| 操作系统 | Ubuntu 20.04/22.04/24.04、Debian 11/12、CentOS 7/8、RHEL、openEuler 22.03+、麒麟 V10、统信 UOS V20、Windows 10/11、Server 2019+ | install 脚本自动识别包管理器 |
| CPU 架构 | **x86_64(amd64)**、**ARM64(aarch64：鲲鹏 920、飞腾 S2500/腾云 S5000、AWS Graviton、Apple 芯片)** | 官方镜像双架构原生支持 |
| 信创架构 | 海光/兆芯(x86)、鲲鹏/飞腾(arm64) 全支持；**龙芯 LoongArch 需换信创镜像源**，见 docs/08 | 不硬骗，方案写实 |
| OCR 引擎 | x86 默认 **PaddleOCR 飞桨**（精度高、可 GPU）；ARM/信创默认 **RapidOCR(ONNX)**（跨架构、轻量稳定） | `.env` 一行切换 |
| GPU | NVIDIA + nvidia-container-toolkit，`USE_GPU=1` 叠加 compose 文件 | 仅 Linux |
| 部署形态 | 单机一体化 / 离线内网 / 多机分离 / 私有镜像仓库 | docs/04、06 |

---

## 4. 常用命令速查

```bash
bash scripts/control.sh status      # 查看全部容器状态
bash scripts/control.sh logs -f worker   # 跟踪 worker 日志
bash scripts/control.sh restart ocr # 只重启 OCR
bash scripts/control.sh stop        # 停全部(数据不丢)
bash scripts/control.sh start       # 再启动
bash scripts/control.sh shell mysql # 进容器
bash scripts/backup.sh              # 一键备份到 backup/
bash scripts/restore.sh backup/backup-xxxx.tar.gz  # 恢复
```
Windows 把 `bash scripts/control.sh` 换成 `.\scripts\control.ps1`。

## 5. 投递一个自动化任务（验证全链路）
```bash
source .env
docker exec -i ent-redis redis-cli -a "$REDIS_PASSWORD" --no-auth-warning \
  LPUSH rpa:tasks "$(cat worker/app/task_example.json)"
bash scripts/control.sh logs -f worker   # 观察 Worker: 开页面->截图->OCR->落库
```

## 6. 工程目录总览
```
ent-platform/
├── docker-compose.yml        # 唯一编排入口
├── .env.example              # 配置样板(install 自动生成 .env)
├── mysql/ redis/ nginx/      # 中间件配置(已调优)
├── ocr/ browser/ worker/     # Python 自动化三服务
├── backend/                  # Java 后端(放 app.jar)
├── scripts/                  # 一键部署/运维/离线脚本(Win+Linux)
├── data/                     # 所有持久化数据(挂载点, 备份就备它)
├── logs/ backup/ packages/   # 日志 / 备份 / 离线包输出
└── docs/                     # 全套文档
```
