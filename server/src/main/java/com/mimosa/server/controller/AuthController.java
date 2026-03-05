package com.mimosa.server.controller;

import com.mimosa.server.model.AuthRequest;
import com.mimosa.server.model.TokenResponse;
import com.mimosa.server.service.AuthService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    // 1. 微信小程序注册账号
    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody AuthRequest request) {
        boolean success = authService.register(request.account(), request.password());
        if (success) {
            return ResponseEntity.ok("账号注册成功");
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("注册失败：此账号已存在");
    }

    // 2. 账号登录，换取 Token
    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(@RequestBody AuthRequest request) {
        String token = authService.login(request.account(), request.password());
        if (token != null) {
            return ResponseEntity.ok(new TokenResponse(token, "登录成功"));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new TokenResponse(null, "登录失败：账号或密码错误"));
    }

    // 3. 每 30 秒无感刷新换取新 Token
    @PostMapping("/refresh")
    public ResponseEntity<TokenResponse> refresh(@RequestHeader(value = "Authorization", required = false) String token) {
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
}