# =============================================================================
# Java(Spring Boot) 后端镜像
# 用法:
#   1) mvn clean package 后, 把可执行 jar 放到本目录并命名为 app.jar
#   2) scripts/install.sh 检测到 backend/app.jar 才会带 --profile backend 构建启动
#      (没有业务 jar 时, 中间件 + 自动化 + OCR 整套照常一键启动)
# 多架构: eclipse-temurin 官方镜像支持 linux/amd64 与 linux/arm64
#   信创 JDK(毕晟 BiSheng / 阿里 Kona / 龙井) 替换见 docs/08-信创国产化适配.md
# =============================================================================
FROM eclipse-temurin:17-jre

ENV TZ=Asia/Shanghai JAVA_OPTS="" SPRING_PROFILES_ACTIVE=prod
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends tzdata curl \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && rm -rf /var/lib/apt/lists/*

# 构建前必须存在 app.jar (install 脚本会做检测并给出明确提示)
COPY app.jar ./app.jar

EXPOSE 8080
STOPSIGNAL SIGTERM   # Spring Boot 优雅停机
# JAVA_OPTS / 数据库与 Redis 连接参数由 compose 环境变量注入
ENTRYPOINT ["sh","-c","java $JAVA_OPTS -Dspring.profiles.active=$SPRING_PROFILES_ACTIVE -jar /app/app.jar"]
