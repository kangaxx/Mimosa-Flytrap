package com.mimosa.server.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mimosa.server.model.LoginRecord;
import com.mimosa.server.model.UpdateUserRequest;
import com.mimosa.server.model.UserData;
import com.mimosa.server.utils.WechatUtil;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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

    private static final Logger log = LoggerFactory.getLogger(AuthService.class);

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

    @Value("${wechat.appid:}")
    private String wechatAppid;

    @Value("${wechat.secret:}")
    private String wechatSecret;

    public AuthService() {
        loadUsersFromJson();
    }

    private void loadUsersFromJson() {
        if (usersFile.exists()) {
            try {
                Map<String, UserData> loadedUsers = objectMapper.readValue(usersFile, new TypeReference<Map<String, UserData>>() {});
                users.putAll(loadedUsers);
                log.info("成功从 users.json 载入 {} 个用户", loadedUsers.size());
            } catch (IOException e) {
                log.error("无法读取 users.json 文件: {}", e.getMessage(), e);
            }
        } else {
            log.info("未找到 users.json，如果是首次启动，这很正常。");
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
            log.debug("成功保存配置至 users.json，共 {} 条记录", users.size());
        } catch (IOException e) {
            log.error("无法写入 users.json 文件: {}", e.getMessage(), e);
        }
    }

    // 微信小程序登录（通过 code 获取 openid）
    public Map<String, Object> wechatLogin(String code) {
        log.info("收到微信登录请求：code={}", code);
        if (code == null || code.isBlank()) {
            loginHistory.add(new LoginAttempt("unknown", LocalDateTime.now(), false, "登录失败：code 为空"));
            log.warn("登录失败：code 为空或空字符串");
            return null;
        }

        // 调用微信 code2Session 接口
        WechatUtil.WechatSession session = WechatUtil.getSession(wechatAppid, wechatSecret, code);
        if (session == null) {
            loginHistory.add(new LoginAttempt("unknown", LocalDateTime.now(), false, "登录失败：微信 code2Session 失败"));
            log.error("微信 code2Session 失败");
            return null;
        }

        String openid = session.getOpenid();
        log.info("微信 code2Session 成功：openid={}", openid);

        // 新用户注册或老用户登录
        UserData existingUser = users.get(openid);
        if (existingUser == null) {
            String userid = UUID.randomUUID().toString();
            UserData newUser = new UserData(openid, "微信用户", userid, null, null, System.currentTimeMillis(), System.currentTimeMillis());
            users.put(openid, newUser);
            log.info("新用户注册成功：openid={}, userid={}", openid, userid);
            saveUsersToJson();
            existingUser = newUser;
        } else {
            log.debug("老用户登录：openid={}", openid);
        }

        // 生成 Token
        String token = UUID.randomUUID().toString();
        tokens.put(token, openid);
        loginHistory.add(new LoginAttempt(openid, LocalDateTime.now(), true, "登录成功"));
        log.info("用户 {} 登录成功并颁发 Token: {}", openid, token);
        
        // 构建返回数据
        Map<String, Object> result = new java.util.HashMap<>();
        result.put("token", token);
        result.put("openid", openid);
        result.put("nickName", existingUser.nickname());
        result.put("avatarUrl", existingUser.avatarUrl());
        
        return result;
    }

    // 更新用户信息
    public boolean updateUser(String appid, UpdateUserRequest request) {
        if (!users.containsKey(appid)) {
            log.warn("用户不存在：{}", appid);
            return false;
        }

        UserData user = users.get(appid);
        String newNickname = request.nickname() != null ? request.nickname() : user.nickname();
        String newAvatar = request.avatarUrl() != null ? request.avatarUrl() : user.avatarUrl();
        Integer newGender = request.gender() != null ? request.gender() : user.gender();

        users.put(appid, new UserData(
            appid, newNickname, user.userid(), newAvatar, newGender,
            user.createTime(), System.currentTimeMillis()
        ));

        saveUsersToJson();
        log.info("用户信息更新成功：appid={}", appid);
        return true;
    }

    // 根据 Token 获取 appid
    public String getAppidByToken(String token) {
        return tokens.get(token);
    }

    // 根据 appid 获取用户信息
    public UserData getUserByAppid(String appid) {
        return users.get(appid);
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