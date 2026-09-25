# 08 · 信创国产化适配手册

## 1. 国产 CPU / OS 适配矩阵（如实标注，不夸大）

| 国产平台 | 指令集 | Docker 支持 | 本工程适配方式 |
|---|---|---|---|
| 海光 C86、兆芯 KX-6000/7000 | x86_64 | 完整 | **等同 amd64，全组件直接跑，OCR 默认 paddle** |
| 华为鲲鹏 920 | aarch64 | 完整 | **arm64 原生**，官方 mysql/redis/nginx/temurin/playwright 均有 arm64 镜像；OCR 默认 rapid |
| 飞腾 S2500 / 腾云 S5000C | aarch64 | 完整 | 同鲲鹏，arm64 |
| 阿里云倚天、AWS Graviton | aarch64 | 完整 | 同 arm64 |
| 龙芯 3C5000/3A6000 | loongarch64 | 支持但生态有限 | DockerHub 官方镜像**大多没有 loong64**，需用龙芯/统信/麒麟自带仓库的镜像或源码构建，见第 4 节 |
| 申威 SW64 | sw_64 | 很有限 | 不建议容器化路线，建议换 arm/x86 信创平台 |

| 国产 OS | 版本 | 包管理 | install.sh 支持 |
|---|---|---|---|
| 麒麟 Kylin V10 SP1/SP2/SP3 | — | apt/yum（看桌面版/服务器版） | 自动识别，优先系统源装 docker.io |
| 统信 UOS V20（服务器/专业版） | 1050/1070 | apt | 自动识别 |
| 华为 openEuler | 22.03 LTS/24.03 | dnf/yum | 自动识别 |
| 中科方德、普华、凝思 | — | apt/yum | 手动装 docker 后脚本同样可用 |

## 2. 信创环境推荐配置组合（最稳落地配方）

- **OS**：麒麟 V10 SP3 / 统信 UOS V20 / openEuler 22.03
- **CPU**：鲲鹏 920 或 海光（风险最低）
- **OCR**：`OCR_ENGINE=rapid`（ONNX Runtime 有 aarch64 官方 wheel，纯 CPU 稳定；飞桨 aarch64 视版本而定）
- **JDK**：容器内 eclipse-temurin arm64 可直接用；若合规要求国产 JDK，换 **毕昇 JDK（BiSheng，鲲鹏最优）/ 阿里 Kona / 华为龙井**，把 backend/Dockerfile 基础镜像换成对应 arm64 JRE 镜像即可，业务 jar 不动。
- **数据库替代**：要求纯国产数据库时（达梦 DM8、人大金仓 KingbaseES、openGauss、GaussDB），把 mysql 服务替换为对应数据库容器/实例，Java 侧换驱动与方言；Worker 的 `rpa_task` 用标准 SQL，迁移成本低。本工程默认 MySQL 是为了通用性。
- **缓存替代**：Redis 可换 TongRDS/阿里 Tair/龙蜥 kvrocks，协议兼容，Worker/Java 基本无感。

## 3. ARM64（鲲鹏/飞腾）标准部署步骤

```bash
# 1) 确认架构
uname -m    # 期望 aarch64

# 2) 装 docker(以 openEuler/麒麟服务器版为例)
sudo yum install -y docker docker-compose-plugin   # apt 系用 apt install docker.io
sudo systemctl enable --now docker

# 3) 部署(脚本识别 arm64 后自动 OCR_ENGINE=rapid)
sudo bash scripts/install.sh
bash scripts/control.sh status
```
### 在 x86 构建机上交叉构建 arm64 镜像（给鲲鹏出包）
```bash
# 一次性初始化(需要 qemu-user 支持 binfmt)
docker run --privileged --rm tonistiigi/binfmt --install arm64
docker buildx create --name ent-builder --use
bash scripts/build-multiarch.sh 仓库地址/ent      # 同时出 amd64+arm64 并推送
# 不能推仓库时, 最稳妥仍是在一台真实 arm64 机器上 offline-save 出 arm 离线包
```

## 4. 龙芯 LoongArch64 落地方案（重点，避免踩空）

现实情况：Docker Hub 上 `mysql:8.0`、`nginx`、`python:3.10-slim`、`playwright` 官方镜像**基本不提供 linux/loong64**，不能直接 `docker pull`。三条可行路线，按优先级：

1. **【推荐】用龙芯/统信/麒麟官方仓库里的 loong64 镜像**
   - 龙芯 LCRX、统信 UOS 应用商店、麒麟软件源均提供 loong64 版 nginx/redis/mysql 兼容实现（如基于统信基础镜像打包）。
   - 做法：把 compose 里 `image: mysql:8.0` 换成 `<信创仓库>/mysql-loong64:标签`，其余配置不变。
2. **以 loong64 国产 OS 基础镜像自建**
   - 基础镜像用 `loongson/debian:loong64` 或麒麟/统信 loong64 base；
   - Python：龙芯提供 loongarch64 的 Python 与部分 wheel；OCR 一律走 RapidOCR/ONNX（飞桨无 loong 官方 wheel，不建议硬上）；
   - Chromium：龙芯浏览器/Lbrowsers 提供 loong64 构建，Playwright 官方不支持 loong64，需要用龙芯浏览器 + CDP 自行对接（Worker 连接逻辑不变，换浏览器镜像与可执行路径）。
3. **【最省事】业务层跑在 x86/arm 信创节点**，龙芯机器只做国产数据库/中间件。
> 结论：海光/鲲鹏/飞腾可以承诺“一键全跑”；龙芯需要替换镜像源、OCR 用 rapid、浏览器走龙芯构建，已在本工程预留替换点（全部参数化）。

## 5. 内网镜像仓库（信创交付标配）

```bash
# 起一个私有 registry(离线环境也可用)
docker run -d --restart=always --name registry -p 5000:5000 -v /data/registry:/var/lib/registry registry:2
# 镜像打 tag 推送
docker tag ent/worker:paddle 仓库IP:5000/ent/worker:v1
docker push 仓库IP:5000/ent/worker:v1
# 目标机 /etc/docker/daemon.json 加 insecure-registries 后 pull
```
`build-multiarch.sh 仓库地址/ent` 一条命令完成多架构构建+推送。

## 6. 等保/合规相关默认项（配合 09 安全手册）
- 中间件不暴露公网，只经 Nginx；密码随机化、`.env` 600 权限。
- 全部镜像固定版本 tag，离线交付可做镜像漏洞扫描（Trivy 支持 arm64）。
- 审计：MySQL 开审计可用企业版/插件；Nginx 日志已带全字段；操作命令走堡垒机。
- 国密 HTTPS：Nginx 配合国密版 OpenSSL（铜锁/Tongsuo）或国密网关，证书替换位置不变。
