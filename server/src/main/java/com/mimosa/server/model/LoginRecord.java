package com.mimosa.server.model;

import io.swagger.v3.oas.annotations.media.Schema;
import java.time.LocalDateTime;

@Schema(description = "登录尝试记录实体")
public record LoginRecord(
        @Schema(description = "登录账号/appid", example = "app_123456")
        String account,
        
        @Schema(description = "尝试登录的时间")
        LocalDateTime attemptTime,
        
        @Schema(description = "是否成功", example = "true")
        boolean success,
        
        @Schema(description = "相关消息", example = "登录成功")
        String message,
        
        @Schema(description = "该账号当前是否处于活跃登录状态", example = "true")
        boolean isCurrentlyActive
) {
}
