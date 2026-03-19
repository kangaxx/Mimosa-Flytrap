# Ubuntu 服务器部署说明文档

这是一份关于如何在纯洁的 Ubuntu 环境上部署 Spring Boot 项目到生产环境（或测试服务器）指南。

由于该服务端项目专门设计用作前端手机设备（如微信小程序）与后台各种 AI 智能体 (Agents, 位于 AgentS+LocalLLM 下) 交互的中心枢纽桥梁，只处理路由转发、业务鉴权以及请求分发等动作，因此占用的硬件资源极低，最低 `1核1GB` 即可满足初期需要。

- **服务器建议使用版本：** Ubuntu 20.04 LTS 或 22.04 LTS 及以上
- **基础依赖：** JRE/JDK 17 运行环境

## 一、一键初始化服务器环境

如果您的 Ubuntu 上尚未安装 JDK（Java 运行环境），可使用仓库中提供的脚本一键安装 OpenJDK 17：

在 `server` 根目录下执行以下命令：

```bash
chmod +x setup_ubuntu_env.sh
./setup_ubuntu_env.sh
```

如网络良好，它将自动通过 `apt-get` 获取 Java 依赖，随后会自动给 `gradlew` 赋予执行权限。

## 二、编译打包项目

这套基于 Gradle 的 Spring Boot 系统不需要在服务器单独安装 Maven 或 Gradle 客户端。

直接使用已有的 `gradlew` 进行编译，并**跳过单元测试快速打包**：

```shell
./gradlew clean build -x test
```

> 第一次构建时因为要拉取各种依赖包和 Gradle 本体，可能需要几分钟，后面再次打包会在数秒内完成。
最终的独立可执行 `jar` 文件会生成在 `build/libs/` 下，名字如 `server-0.0.1-SNAPSHOT.jar`。

## 三、部署和启动应用

我们提供多种在 Ubuntu 下运行应用的方式，您可以按照您机器的内存大小进行选择：

### 1️⃣ 前台高亮带日志运行（测试/排查问题专用）

```bash
下面这段代码务必在至少8核的服务器上运行，目前99元的服务器跑不了
java -jar build/libs/server-0.0.1-SNAPSHOT.jar
```

关闭控制台或按下 `Ctrl+C` 将结束进程。

### 2️⃣ 开启后台进程运行（最低限度部署必备）

如果你直接关闭通过 SSH 连接的 Ubuntu 会话终端应用将会中止。可执行下列后台常驻指令启动：

```bash
nohup java -jar build/libs/server-0.0.1-SNAPSHOT.jar > app.log 2>&1 &
```

可以通过 `tail -f app.log` 动态查看启动和运行中的请求日志。

### 3️⃣ 指定内存界限的小内存云服务器运行方案（1核1G / 1核2G机器推荐）

如果没有为小内存服务器定义 JVM 的内存阈值，Spring Boot 在运行高负荷任务时可能会因触发 OS 的回收机制 (OOM Killer) 被进程强杀。强烈建议限制最大堆内存 (`-Xmx`)。

```bash
nohup java -Xms256m -Xmx512m -jar build/libs/server-0.0.1-SNAPSHOT.jar > app.log 2>&1 &
```

> JVM 会限制其在 256m~512m 的内存范围内浮动，保证系统稳定运行。

## 四、关闭服务和维护进程
找到运行中 java 进程的 PID：
```bash
ps -ef | grep java
```
之后再直接干掉对应的进程 (假设 PID 为 12345)：
```bash
kill -9 12345
```