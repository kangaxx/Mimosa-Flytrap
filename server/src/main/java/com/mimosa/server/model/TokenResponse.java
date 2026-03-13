package com.mimosa.server.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Token 返回实体")
public record TokenResponse(
    @Schema(description = "认证使用的 Token", example = "550e8400-e29b-41d4-a716-446655440000")
    String token, 
    
    @Schema(description = "响应提示信息", example = "登录成功")
    String message
) {
}
