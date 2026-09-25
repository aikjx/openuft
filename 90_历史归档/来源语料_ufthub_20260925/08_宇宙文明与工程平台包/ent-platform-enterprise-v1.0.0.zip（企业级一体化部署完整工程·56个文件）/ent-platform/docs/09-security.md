# 09 · 安全加固手册（上线前逐项过）

## 1. 网络暴露面（默认已收敛）
- 只有 Nginx 暴露 80；MySQL/Redis 绑定 `127.0.0.1`；OCR/Browser 不映射宿主机端口。
- 云安全组/防火墙只放行 80/443（必要时 22 限源 IP），**绝不对公网开 3306/6379/9222/8000**。
- 管理操作走 VPN/堡垒机，不把 Docker 2375 远程端口暴露出去。

## 2. 账号与密码
- install 已为三个密码生成 20 位随机值；`.env` 权限 600，属主为部署账号。
- 业务使用 `appuser`，只授业务库权限，不用 root：
```sql
-- init 脚本已建账号; 最小权限回收示例
REVOKE ALL PRIVILEGES ON *.* FROM 'appuser'@'%';
GRANT SELECT,INSERT,UPDATE,DELETE ON appdb.* TO 'appuser'@'%';
```
- 定期改密：改 `.env` + 库内 `ALTER USER`，然后 restart；Redis 改密后同步 `.env` 并 restart。

## 3. HTTPS（生产必开）
1. 证书放 `nginx/certs/`（server.crt / server.key）。
2. compose 中 nginx 取消 443 端口注释，挂载 certs。
3. `conf.d/backend.conf` 末尾 HTTPS 模板取消注释，开启 TLS1.2/1.3、HTTP 跳 HTTPS。
4. 国密场景换 Tongsuo/国密网关，见 docs/08。

## 4. Nginx 加固（已默认开启的项）
- `server_tokens off` 隐藏版本
- `X-Content-Type-Options/X-Frame-Options/Referrer-Policy` 安全头
- `limit_req` 限流，防刷；按需加 `limit_conn` 限并发
- 建议再加 WAF（ModSecurity / 云 WAF）、只允许必要 UA、管理路径 IP 白名单

## 5. 容器安全
- 容器全部以非 root 运行（官方 mysql/redis/nginx/nginx 镜像内置非 root 用户；自建 Python 服务如需进一步降权，加 `USER nobody` 并调整卷属主）。
- 不给容器 `privileged`；不挂 docker.sock；capabilities 默认最小集。
- 镜像固定版本 tag，禁止生产用 latest；上线前用 Trivy/Grype 扫 CVE：
```bash
trivy image --severity HIGH,CRITICAL ent/ocr:paddle
```
- 镜像源用私有仓库+签名校验（Docker Content Trust / Harbor 漏洞扫描）。

## 6. 数据安全
- 备份包含 `.env` 快照（有密码），`backup/` 目录权限 700，异地加密存储。
- 截图可能含个人信息：`data/shared` 设定期清理、访问权限收敛，必要时 OCR 后即删。
- 敏感字段（身份证/手机号）入库前应用层加密或 MySQL 加密函数，密钥不进镜像。
- 等保要求：操作审计（MySQL audit 插件/Nginx 日志留存≥6 个月，调整 logrotate 与备份周期）。

## 7. 自动化/爬虫侧合规与风控
- 出口代理凭据只放 `.env`，不写进代码/镜像。
- 控制访问频率（WORKER_CONCURRENCY + 页面延时），遵守目标站点 robots 与服务条款。
- 登录态/Cookie 不落明文：建议放 Redis（带密码、内网）或内存，用完即弃。
- ignore_https_errors 仅在内网可信站点开启，公网站点保持证书校验。

## 8. 上线前安全 Checklist
- [ ] 三个随机密码已生效，无 CHANGE_ME/弱口令
- [ ] 公网仅 80/443，3306/6379 外部不可达
- [ ] HTTPS 已启用，HTTP 跳转
- [ ] `.env`、`backup/` 权限 600/700
- [ ] 镜像无 HIGH/CRITICAL 未处理漏洞
- [ ] 日志留存周期满足合规
- [ ] 备份已做并成功试恢复
- [ ] 宿主机已打补丁、Docker 为受支持版本、禁掉无用服务
