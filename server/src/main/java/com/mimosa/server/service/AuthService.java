package com.mimosa.server.service;

import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AuthService {

    // 模拟数据库：保存用户 账号 -> 密码映射
    private final Map<String, String> users = new ConcurrentHashMap<>();
    
    // 模拟 Redis/内存 Token 存储：保存 Token -> 账号映射
    private final Map<String, String> tokens = new ConcurrentHashMap<>();

    // 1. 注册账号
    public boolean register(String account, String password) {
        if (users.containsKey(account)) {
            return false; // 用户已存在
        }
        users.put(account, password);
        return true;
    }

    // 2. 账号登录
    public String login(String account, String password) {
        if (password.equals(users.get(account))) {
            // 验证成功，生成唯一的 Token（UUID）
            String token = UUID.randomUUID().toString();
            tokens.put(token, account);
            return token;
        }
        return null; // 验证失败
    }

    // 3. 刷新 Token
    public String refreshToken(String oldToken) {
        String account = tokens.get(oldToken);
        if (account != null) {
            // 删除旧的 Token
            tokens.remove(oldToken);
            // 生成新 Token
            String newToken = UUID.randomUUID().toString();
            tokens.put(newToken, account);
            return newToken;
        }
        return null; // 原 Token 不存在或已过期
    }

    // 4. 验证 Token 有效性
    public boolean validateToken(String token) {
        return tokens.containsKey(token);
    }
}