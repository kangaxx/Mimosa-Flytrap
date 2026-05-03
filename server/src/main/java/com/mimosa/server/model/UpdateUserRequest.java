package com.mimosa.server.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "用户信息更新请求参数")
public record UpdateUserRequest(
    @Schema(description = "用户昵称", example = "微信用户")
    String nickname,
    
    @Schema(description = "头像 URL", example = "https://wx.qlogo.cn/mmopen/...")
    String avatarUrl,
    
    @Schema(description = "性别 (0:未知 1:男 2:女)", example = "1")
    Integer gender
) {}
