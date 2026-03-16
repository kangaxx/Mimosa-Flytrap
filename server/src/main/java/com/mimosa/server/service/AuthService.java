package com.mimosa.server.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mimosa.server.model.LoginRecord;
import com.mimosa.server.model.UserData;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
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

    // 模拟数据库：保存用户 appid -> UserData 映射
    private final Map<String, UserData> users = new ConcurrentHashMap<>();
    
    // 模拟 Redis/内存 Token 存储：保存 Token -> appid 映射
    private final Map<String, String> tokens = new ConcurrentHashMap<>();

    // 保存所有登录尝试的记录
    private final List<LoginAttempt> loginHistory = new CopyOnWriteArrayList<>();

    private final File usersFile = new File("users.json");
    private final ObjectMapper objectMapper = new ObjectMapper();

    public AuthService() {
        loadUsersFromJson();
    }

    private void loadUsersFromJson() {
        if (usersFile.exists()) {
            try {
                Map<String, UserData> loadedUsers = objectMapper.readValue(usersFile, new TypeReference<Map<String, UserData>>() {});
                users.putAll(loadedUsers);
            } catch (IOException e) {
                System.err.println("无法读取 users.json 文件: " + e.getMessage());
            }
        }
    }

    private void saveUsersToJson() {
        try {
            // 如果文件不存在则直接创建文件
            if (!usersFile.exists()) {
                usersFile.createNewFile();
            }
            // 使用 writerWithDefaultPrettyPrinter() 将 JSON 格式化输出（让数据可读性更好）
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(usersFile, users);
        } catch (IOException e) {
            System.err.println("无法写入 users.json 文件: " + e.getMessage());
        }
    }

    // 账号登录（如果是新账号则隐式注册）
    public String login(String appid, String nickname) {
        if (appid == null || appid.isBlank()) {
            loginHistory.add(new LoginAttempt("unknown", LocalDateTime.now(), false, "登录失败：appid 为空"));
            return null;
        }

        // 隐式注册或更新信息
        if (!users.containsKey(appid)) {
            String userid = UUID.randomUUID().toString();
            users.put(appid, new UserData(appid, nickname, userid));
            saveUsersToJson();
        } else {
            UserData existingUser = users.get(appid);
            // 如果昵称发生变化，更新并保存
            if (nickname != null && !nickname.equals(existingUser.nickname())) {
                users.put(appid, new UserData(appid, nickname, existingUser.userid()));
                saveUsersToJson();
            }
        }

        // 生成唯一的 Token
        String token = UUID.randomUUID().toString();
        tokens.put(token, appid);
        loginHistory.add(new LoginAttempt(appid, LocalDateTime.now(), true, "登录成功"));
        return token;
    }

    // 3. 刷新 Token
    public String refreshToken(String oldToken) {
        String appid = tokens.get(oldToken);
        if (appid != null) {
            // 删除旧的 Token
            tokens.remove(oldToken);
            // 生成新 Token
            String newToken = UUID.randomUUID().toString();
            tokens.put(newToken, appid);
            return newToken;
        }
        return null; // 原 Token 不存在或已过期
    }

    // 4. 验证 Token 有效性
    public boolean validateToken(String token) {
        return tokens.containsKey(token);
    }

    // 5. 检查账号当前是否有活跃的 Token (是否处于登录且及时刷新状态)
    public boolean isAccountActive(String appid) {
        return tokens.containsValue(appid);
    }

    // 6. 获取最近24小时的登录历史记录
    public List<LoginRecord> getRecentLoginHistory() {
        LocalDateTime twentyFourHoursAgo = LocalDateTime.now().minusHours(24);
        return loginHistory.stream()
                .filter(attempt -> attempt.timestamp().isAfter(twentyFourHoursAgo))
                .sorted((a, b) -> b.timestamp().compareTo(a.timestamp())) // 按时间倒序
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