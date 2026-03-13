package com.mimosa.server.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "登录请求参数实体")
public record AuthRequest(
    @Schema(description = "应用/用户唯一标识符(appid)", example = "app_123456")
    String appid, 
    
    @Schema(description = "用户昵称", example = "微信用户")
    String nickname
) {
}
