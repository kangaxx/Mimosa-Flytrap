package com.mimosa.server.service;

import com.mimosa.server.model.LoginRecord;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.stream.Collectors;

@Service
public class AuthService {

    // 内部登录尝试记录类
    private record LoginAttempt(String account, LocalDateTime timestamp, boolean success, String message) {}

    // 模拟数据库：保存用户 账号 -> 密码映射
    private final Map<String, String> users = new ConcurrentHashMap<>();
    
    // 模拟 Redis/内存 Token 存储：保存 Token -> 账号映射
    private final Map<String, String> tokens = new ConcurrentHashMap<>();

    // 保存所有登录尝试的记录
    private final List<LoginAttempt> loginHistory = new CopyOnWriteArrayList<>();

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
            loginHistory.add(new LoginAttempt(account, LocalDateTime.now(), true, "登录成功"));
            return token;
        }
        loginHistory.add(new LoginAttempt(account, LocalDateTime.now(), false, "登录失败：密码或账号错误"));
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

    // 5. 检查账号当前是否有活跃的 Token (是否处于登录且及时刷新状态)
    public boolean isAccountActive(String account) {
        return tokens.containsValue(account);
    }

    // 6. 获取最近24小时的登录历史记录
    public List<LoginRecord> getRecentLoginHistory() {
        LocalDateTime twentyFourHoursAgo = LocalDateTime.now().minusHours(24);
        return loginHistory.stream()
                .filter(attempt -> attempt.timestamp().isAfter(twentyFourHoursAgo))
                .sorted((a, b) -> b.timestamp().compareTo(a.timestamp())) // 按时间倒序（最近的一条在最上面）
                .map(attempt -> new LoginRecord(
                        attempt.account(),
                        attempt.timestamp(),
                        attempt.success(),
                        attempt.message(),
                        isAccountActive(attempt.account())
                ))
                .collect(Collectors.toList());
    }
}