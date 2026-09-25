# 04 · 安装部署手册

## 1. 部署前要求

| 项 | 最低 | 推荐 |
|---|---|---|
| 操作系统 | Ubuntu20/CentOS7/麒麟V10/UOS V20/Win10 | Ubuntu22.04 / 麒麟V10 SP3 |
| CPU | x86_64 或 aarch64，2 核 | 4 核+ |
| 内存 | 2G（rapid 引擎精简跑） | 8G |
| 磁盘 | 20G | 50G SSD（镜像约 5G，数据另算） |
| 网络 | 在线安装需能访问镜像源；离线见第 5 节 | 配置内网镜像仓库 |
| 权限 | Linux 安装 Docker 需 root/sudo；运行阶段 docker 用户组即可 | — |

## 2. Linux 在线部署（标准流程）

```bash
# ① 解压到标准目录
sudo tar -xzf ent-platform.tar.gz -C /opt/
cd /opt/ent-platform

# ② 自检（会报告架构、内存、磁盘、端口、Docker 情况）
bash scripts/check-env.sh

# ③ 一键安装（自动: 装docker -> 生成.env与密码 -> 内存调优 -> 拉镜像 -> 构建 -> 启动 -> 健康检查）
sudo bash scripts/install.sh

# ④ 看状态
bash scripts/control.sh status
```
安装脚本是**幂等**的：重复执行不会覆盖已有 `.env` 和数据，可反复跑。

### systemd 开机自启（推荐，替代容器 restart 策略的双保险）
```bash
sudo tee /etc/systemd/system/ent-platform.service >/dev/null <<'EOF'
[Unit]
Description=Ent Platform Compose Stack
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/ent-platform
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ent-platform
```

## 3. Windows 部署

1. 启用 WSL2：管理员 PowerShell 执行 `wsl --install`，重启。
2. 安装 Docker Desktop（Settings → Resources → WSL2 Integration 开启），Settings → Docker Engine 可加国内 `registry-mirrors`。
3. 解压到 `D:\ent-platform`，执行：
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
cd D:\ent-platform
.\scripts\check-env.ps1
.\scripts\install.ps1
.\scripts\control.ps1 status
```
> Windows 仅建议用于开发/演示；生产统一用 Linux。Windows 上数据落 WSL2 虚拟磁盘，性能与备份策略见 07。

## 4. GPU 部署（NVIDIA，仅 Linux）

```bash
# ① 宿主机装 NVIDIA 驱动（不需要装 CUDA Toolkit，镜像自带）
# ② 装容器运行时
Ubuntu/Debian:
  sudo apt-get install -y nvidia-container-toolkit && sudo systemctl restart docker
CentOS/openEuler:
  sudo yum install -y nvidia-container-toolkit && sudo systemctl restart docker
# ③ 验证
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
# ④ 用 GPU 覆盖文件启动
USE_GPU=1 bash scripts/install.sh           # 首次会构建 Dockerfile.gpu
# 或日常:
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
```
`.env` 保持 `OCR_ENGINE=paddle`；OCR 吞吐提升明显时，配合 `/ocr/batch` 批量接口。

## 5. 离线/信创内网部署（政务专网）

**核心原则：在与目标机相同 CPU 架构的联网机器上制作离线包。**

```bash
# ---- 联网机(架构必须和目标一致: x86 对 x86, arm 对 arm) ----
cd ent-platform
bash scripts/install.sh           # 先本机跑通, 镜像全部拉到本地
bash scripts/offline-save.sh      # 产出 packages/ent-offline-<arch>-日期.tar.gz

# ---- 目标内网机 ----
tar -xzf ent-offline-<arch>-日期.tar.gz   # 或直接用 offline-load
bash scripts/offline-load.sh ent-offline-<arch>-日期.tar.gz
```
离线包内容：全部容器镜像 `images.tar` + 工程/配置/脚本 + 安装说明。目标机只需**预装 Docker**，全程不联网。龙芯等无官方镜像的架构见 `08`。

## 6. 多机/集群部署顺序
1. 数据机先起：`docker compose up -d mysql redis`，改 bind 地址与防火墙。
2. 自动化机：`docker compose up -d browser ocr worker`，环境变量指向数据机。
3. 应用机：放入 `backend/app.jar`，`docker compose --profile backend up -d backend nginx`。
4. 前面挂 SLB/F5；Nginx 可多机，Java 无状态水平扩。

## 7. 部署验收清单

- [ ] `control.sh status` 7 个容器（无 jar 时 6 个）全部 Up/healthy
- [ ] `curl http://127.0.0.1/healthz` 返回 ok
- [ ] 投递 `task_example.json`，Worker 日志出现 done，MySQL `rpa_task` 有 status=2 记录
- [ ] `127.0.0.1:3306/6379` 仅本机可连，外网 telnet 不通
- [ ] `.env` 密码已非 CHANGE_ME，权限 600
- [ ] `backup.sh` 能产出备份包并试恢复一次
- [ ] 重启服务器后服务自动拉起
