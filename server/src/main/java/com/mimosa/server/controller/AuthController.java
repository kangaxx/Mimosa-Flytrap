package com.mimosa.server.controller;

import com.mimosa.server.model.AuthRequest;
import com.mimosa.server.model.LoginRecord;
import com.mimosa.server.model.TokenResponse;
import com.mimosa.server.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Auth API", description = "用户认证与登录相关接口")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @Operation(summary = "账号登录", description = "使用 appid 和 nickname 进行登录（新账号自动注册），并返回访问 Token")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "登录成功，返回 Token"),
        @ApiResponse(responseCode = "401", description = "登录失败")
    })
    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(
            @Parameter(description = "包含 appid 和 nickname 的登录请求体", required = true) 
            @RequestBody AuthRequest request) {
        String token = authService.login(request.appid(), request.nickname());
        if (token != null) {
            return ResponseEntity.ok(new TokenResponse(token, "登录成功"));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new TokenResponse(null, "登录失败"));
    }

    @Operation(summary = "刷新 Token", description = "使用现有的 Token 刷新并换取一个新的 Token")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Token 刷新成功"),
        @ApiResponse(responseCode = "400", description = "请求头中缺少 Token 或格式不正确"),
        @ApiResponse(responseCode = "401", description = "刷新失败：Token无效或已过期")
    })
    @PostMapping("/refresh")
    public ResponseEntity<TokenResponse> refresh(
            @Parameter(description = "携带现有 Token 的 Authorization 头部, 格式为 'Bearer <token>'", required = false) 
            @RequestHeader(value = "Authorization", required = false) String token) {
        if (token == null || !token.startsWith("Bearer ")) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new TokenResponse(null, "请求头需要传 Authorization: Bearer <token>"));
        }
        
        String cleanToken = token.replace("Bearer ", "");
        String newToken = authService.refreshToken(cleanToken);
        
        if (newToken != null) {
            return ResponseEntity.ok(new TokenResponse(newToken, "Token 刷新成功"));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new TokenResponse(null, "刷新失败：Token无效或已过期"));
    }

    @Operation(summary = "查看登录历史", description = "获取最近 24 小时的登录尝试记录及当前登录活跃状态")
    @ApiResponse(responseCode = "200", description = "成功获取历史记录列表")
    @GetMapping("/history")
    public ResponseEntity<List<LoginRecord>> getLoginHistory() {
        return ResponseEntity.ok(authService.getRecentLoginHistory());
    }
}
