# Java 后端接入说明

1. 执行 `mvn clean package -DskipTests`，把产物复制到本目录并命名为 **app.jar**：
   ```bash
   cp target/xxx.jar backend/app.jar
   ```
2. `install.sh` / `install.ps1` 检测到 `backend/app.jar` 后，会自动追加 `--profile backend` 构建并启动；没有 jar 时该服务不启动，其余组件不受影响。
3. 配置不要写死在 jar 里，全部走环境变量（compose 已注入）：

   | 环境变量 | Spring 取值示例 |
   |---|---|
   | MYSQL_HOST / MYSQL_PORT / MYSQL_DATABASE | `jdbc:mysql://${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}?useUnicode=true&characterEncoding=utf8mb4&serverTimezone=Asia/Shanghai` |
   | MYSQL_USER / MYSQL_PASSWORD | 数据源账号密码 |
   | REDIS_HOST / REDIS_PORT / REDIS_PASSWORD | spring.data.redis.* |

4. 健康检查建议开放 `GET /actuator/health`（compose 用 TCP 8080 探测，不强制）。
5. 手动投递一个自动化任务示例：
   ```bash
   docker exec -it ent-redis redis-cli -a "$REDIS_PASSWORD" LPUSH rpa:tasks "$(cat worker/app/task_example.json)"
   ```
