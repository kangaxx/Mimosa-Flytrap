# Ubuntu 生产环境部署与开机自启 (Systemd) 配置指南

当您的项目准备长期运行在服务器上时，使用 `nohup` 的方式虽然简单，但无法实现服务器重启后自动拉起服务，也难以进行优雅的进程管理和日志轮转。

在 Ubuntu 等现代 Linux 系统中，最标准的做法是使用 **Systemd** 将 Spring Boot 项目注册为一个系统服务（Service）。本指南将手把手教您如何编译并将服务设置为开机启动。

## 第一步：编译与准备执行文件

1. **进入代码目录并编译项目**，生成最终的 `jar` 包：
   ```bash
   cd ~/Mimosa-Flytrap/server
   ./gradlew clean build -x test
   ```
2. **创建专门的部署目录**（推荐放在 `/opt` 目录下）并将打包好的程序拷贝过去：
   ```bash
   sudo mkdir -p /opt/mimosa-server
   sudo cp build/libs/server-0.0.1-SNAPSHOT.jar /opt/mimosa-server/server.jar
   ```

## 第二步：创建 Systemd 服务配置文件

使用您喜欢的编辑器（如 `nano` 或 `vim`）在 `/etc/systemd/system/` 目录下创建一个名为 `mimosa-server.service` 的服务文件：

```bash
sudo nano /etc/systemd/system/mimosa-server.service
```

将以下配置复制并粘贴到文件中（注意根据您的实际机器内存修改 `-Xms` 和 `-Xmx` 的参数）：

```ini
[Unit]
Description=Mimosa Flytrap Spring Boot Backend Service
After=syslog.target network.target

[Service]
# 这里默认使用 root 用户运行。为了更高的安全性，建议在系统中创建一个专用用户来运行。
User=root
Type=simple

# 启动命令：限制了运行内存。请确保 /usr/bin/java 路径正确（可通过 which java 命令确认）
ExecStart=/usr/bin/java -Xms256m -Xmx512m -jar /opt/mimosa-server/server.jar

# 优雅关闭程序的退出码（Spring Boot 收到 SIGTERM 时正常退出码通常为 143）
SuccessExitStatus=143

# 崩溃或意外退出时自动重启服务
Restart=on-failure
# 重启间隔 10 秒
RestartSec=10

[Install]
# 开机自启的目标级别（命令行多用户模式）
WantedBy=multi-user.target
```
保存并退出编辑器。

## 第三步：重载配置并设置开机启动

1. 通知 systemd 加载我们刚刚新建的服务文件：
   ```bash
   sudo systemctl daemon-reload
   ```

2. **设置开机自启**：
   ```bash
   sudo systemctl enable mimosa-server.service
   ```

3. **立即启动服务**：
   ```bash
   sudo systemctl start mimosa-server.service
   ```

4. **查看服务运行状态**：
   ```bash
   sudo systemctl status mimosa-server.service
   ```
   *（如果看到绿色的 `active (running)`，说明服务已经成功在后台运行起来了！）*

## 常用服务管理命令

系统服务化之后，您就可以像管理 Nginx 或 MySQL 一样来管理这个 Spring Boot 项目了：

- **重启服务**（更新了代码并重新放了 jar 包后执行）：
  ```bash
  sudo systemctl restart mimosa-server.service
  ```
- **停止服务**：
  ```bash
  sudo systemctl stop mimosa-server.service
  ```
- **取消开机自启**：
  ```bash
  sudo systemctl disable mimosa-server.service
  ```

## 查看服务日志 (Journalctl)

Systemd 会自动接管和收集程序的控制台输出（取代了原来的 `app.log`），您可以通过 `journalctl` 命令来查看日志：

- **实时动态查看最新日志**（类似 `tail -f`）：
  ```bash
  sudo journalctl -u mimosa-server.service -f
  ```
- **查看最近 100 行日志**：
  ```bash
  sudo journalctl -u mimosa-server.service -n 100
  ```
- **仅查看今天的日志**：
  ```bash
  sudo journalctl -u mimosa-server.service --since today
  ```