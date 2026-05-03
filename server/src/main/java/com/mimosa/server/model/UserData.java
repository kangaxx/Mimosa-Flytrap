package com.mimosa.server.model;

public record UserData(
    String appid, 
    String nickname, 
    String userid,
    String avatarUrl,
    Integer gender,
    Long createTime,
    Long updateTime
) {
    // 简化构造方法（兼容旧代码）
    public UserData(String appid, String nickname, String userid) {
        this(appid, nickname, userid, null, null, System.currentTimeMillis(), System.currentTimeMillis());
    }
}
