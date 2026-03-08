package com.mimosa.server.model;

import java.time.LocalDateTime;

public record LoginRecord(
        String account,
        LocalDateTime attemptTime,
        boolean success,
        String message,
        boolean isCurrentlyActive
) {
}
