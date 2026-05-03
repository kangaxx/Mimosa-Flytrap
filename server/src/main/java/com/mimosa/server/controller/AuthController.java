package com.mimosa.server.controller;

import com.mimosa.server.model.LoginRecord;
import com.mimosa.server.model.TokenResponse;
import com.mimosa.server.model.UpdateUserRequest;
import com.mimosa.server.model.UserData;
import com.mimosa.server.model.WechatLoginRequest;
import com.mimosa.server.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Auth API", description = "用户认证与登录相关接口")
public class AuthController {

    private static final Logger log = LoggerFactory.getLogger(AuthController.class);

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @Operation(summary = "刷新 Token", description = "使用现有的 Token 刷新并换取一个新的 Token")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Token 刷新成功"),
        @ApiResponse(responseCode = "400", description = "请求头中缺少 Token 或格式不正确"),
        @ApiResponse(responseCode = "401", description = "刷新失败：Token 无效或已过期")
    })
    @PostMapping("/refresh")
    public ResponseEntity<TokenResponse> refresh(
            @Parameter(description = "携带现有 Token 的 Authorization 头部，格式为 'Bearer <token>'", required = false) 
            @RequestHeader(value = "Authorization", required = false) String token) {
        log.info("接收到 /refresh 请求");
        if (token == null || !token.startsWith("Bearer ")) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new TokenResponse(null, "请求头需要传 Authorization: Bearer <token>"));
        }
            
        String cleanToken = token.replace("Bearer ", "");
        String newToken = authService.refreshToken(cleanToken);
            
        if (newToken != null) {
            return ResponseEntity.ok(new TokenResponse(newToken, "Token 刷新成功"));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new TokenResponse(null, "刷新失败：Token 无效或已过期"));
    }
    
    @Operation(summary = "微信小程序登录", description = "使用微信 code 进行登录（自动注册），并返回访问 Token")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "登录成功，返回 Token"),
        @ApiResponse(responseCode = "401", description = "登录失败：code 无效或微信接口调用失败")
    })
    @PostMapping("/wechat/login")
    public ResponseEntity<Map<String, Object>> wechatLogin(
            @Parameter(description = "包含微信 code 的登录请求体", required = true) 
            @RequestBody WechatLoginRequest request) {
        log.info("接收到 /wechat/login 请求：code={}", request.code());
        Map<String, Object> result = authService.wechatLogin(request.code());
        if (result != null) {
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "data", result,
                "message", "登录成功"
            ));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
            "code", 401,
            "msg", "登录失败",
            "data", null
        ));
    }

    @Operation(summary = "更新用户信息", description = "更新用户的昵称、头像、性别等信息")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "更新成功"),
        @ApiResponse(responseCode = "401", description = "未授权"),
        @ApiResponse(responseCode = "404", description = "用户不存在")
    })
    @PostMapping("/update")
    public ResponseEntity<Map<String, Object>> updateUser(
            @Parameter(description = "Authorization 头部", required = true) 
            @RequestHeader("Authorization") String token,
            @Parameter(description = "用户信息更新请求体", required = true) 
            @RequestBody UpdateUserRequest request) {
        
        log.info("接收到 /update 请求");
        
        if (token == null || !token.startsWith("Bearer ")) {
            Map<String, Object> error = Map.of("success", false, "message", "缺少 Authorization 头部");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
        
        String cleanToken = token.replace("Bearer ", "");
        String appid = authService.getAppidByToken(cleanToken);
        
        if (appid == null) {
            Map<String, Object> error = Map.of("success", false, "message", "Token 无效或已过期");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
        
        boolean success = authService.updateUser(appid, request);
        
        Map<String, Object> response;
        if (success) {
            response = Map.of("success", true, "message", "更新成功");
            return ResponseEntity.ok(response);
        } else {
            response = Map.of("success", false, "message", "更新失败：用户不存在");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
        }
    }

    @Operation(summary = "获取当前用户信息", description = "获取登录用户的详细信息")
    @GetMapping("/me")
    public ResponseEntity<UserData> getCurrentUser(
            @RequestHeader("Authorization") String token) {
        
        log.info("接收到 /me 请求");
        
        if (token == null || !token.startsWith("Bearer ")) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        String cleanToken = token.replace("Bearer ", "");
        String appid = authService.getAppidByToken(cleanToken);
        
        if (appid == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        UserData user = authService.getUserByAppid(appid);
        return ResponseEntity.ok(user);
    }

    @Operation(summary = "查看登录历史", description = "获取最近 24 小时的登录尝试记录及当前登录活跃状态")
    @ApiResponse(responseCode = "200", description = "成功获取历史记录列表")
    @GetMapping("/history")
    public ResponseEntity<List<LoginRecord>> getLoginHistory() {
        log.info("接收到 /history 请求，查询最近登录历史");
        return ResponseEntity.ok(authService.getRecentLoginHistory());
    }
}
