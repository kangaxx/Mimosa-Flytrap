# Swagger API 调试与使用指南

本项目（Mimosa Flytrap Server）已经为您集成了最新的 **Springdoc OpenAPI 3 (Swagger UI)**。

这可以让开发者直接在浏览器中查看所有可用的 API 接口、数据结构，并且无需依赖 Postman 或编写客户端代码，就能在这个页面上直接模拟微信小程序发送真实的网络请求。

## 一、如何访问 API 可视化面板

1. 确保您的 Spring Boot 项目已经启动（默认端口 8080）。
2. 在您的浏览器中访问以下地址：
   - 本地开发环境：[http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
   - 生产/服务器环境：`http://<您的服务器IP>:8080/swagger-ui/index.html`

打开后，您将看到一个按模块分类的 RESTful API 交互界面。

## 二、测试完整的业务流程 (以账号交互为例)

在我们的系统中，小程序与服务端的交互有一套极简的鉴权（Auth）体系。在 Swagger 中，您可以按照以下步骤模拟小程序的行为：

### 第一步：注册一个测试账号
1. 找到并展开 `POST /api/v1/auth/register` 面板。
2. 点击右上角的 **Try it out** (尝试一下) 按钮。
3. 在请求体 (Request body) 的 JSON 框中输入测试用的账号密码，例如：
   ```json
   {
     "account": "test_mina",
     "password": "123"
   }
   ```
4. 点击 **Execute** 执行请求。如果在下面看到 `200` 响应码且返回 `账号注册成功`，说明注册完成。

### 第二步：登录并获取 Token (凭据)
1. 展开 `POST /api/v1/auth/login` 面板，点击 **Try it out**。
2. 输入刚刚注册的账号和密码：
   ```json
   {
     "account": "test_mina",
     "password": "123"
   }
   ```
3. 点击 **Execute**。
4. 查看下方的 **Server response**，您会收到类似这样的 JSON：
   ```json
   {
     "token": "d74a4d6f-2b3a-4c12-9e8d-8a9f0b1c2d3e",
     "message": "登录成功"
   }
   ```
   **【注意】: 请将双引号里面的这串 token 字符串复制到剪贴板。**

### 第三步：配置全局鉴权头 (Authorize)
服务端要求除了注册登录外的接口，都要在请求头带上 Token。我们在 Swagger 中已经配置好了全局注入模式。

1. 划到 Swagger 页面的最顶端，找到右侧带有一把绿色锁图标的 **Authorize** 按钮并点击。
2. 在弹出的 `bearerAuth (http, Bearer)` 对话框内的 `Value` 输入框中，**粘贴您刚刚复制的 token 字符串**。（注意：直接粘贴值即可，系统会自动帮您加上 `Bearer ` 前缀并放入 Header 中）。
3. 点击绿色的 **Authorize** 按钮保存，然后点击 Close 关闭弹窗。

### 第四步：测试核心业务接口（发送与回显）
目前全局都已经带上了合法的 Token，我们可以去呼叫那些需要权限验证的接口了：

1. 展开 `POST /api/v1/message/send` 面板，点击 **Try it out**。
2. 编辑要发给 Agent 的信息体：
   ```json
   {
     "message": "你好！请帮我查一下今天的天气。"
   }
   ```
3. 点击 **Execute** 执行请求。
4. 系统将验证您的 Token 是否合法，并将信息透传，您会收到成功回显的响应：
   ```json
   {
     "reply": "Server Received: 【你好！请帮我查一下今天的天气。】 - 消息已被 Agent 接收并处理。"
   }
   ```

## 三、相关代码说明 (仅供开发者查阅)
Swagger 面板得以生成，是依赖于项目中添加的两处配置，若后续需要定制化说明可修改以下文件：
1. **依赖库**: `build.gradle` 中引入的 `springdoc-openapi-starter-webmvc-ui`。
2. **全局配置和鉴权头配置类**: 位于 `src/main/java/com/mimosa/server/config/SwaggerConfig.java`，定义了 API 的标题和 `Bearer Auth` 的注入策略。