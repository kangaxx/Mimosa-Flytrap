package com.mimosa.server.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "微信登录请求参数")
public record WechatLoginRequest(
    @Schema(description = "小程序登录凭证 code", example = "0a1b2c3d4e5f6g7h8i9j")
    String code
) {}
