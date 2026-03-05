package com.mimosa.server.controller;

import com.mimosa.server.model.MessageRequest;
import com.mimosa.server.model.MessageResponse;
import com.mimosa.server.service.AuthService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/message")
public class MessageController {

    private final AuthService authService;

    public MessageController(AuthService authService) {
        this.authService = authService;
    }

    // 4. 客户端主动向服务端发送信息，并等待回显服务端信息
    @PostMapping("/send")
    public ResponseEntity<MessageResponse> sendMessage(
            @RequestHeader(value = "Authorization", required = false) String token,
            @RequestBody MessageRequest request) {
            
        // 校验 Token（鉴权）
        if (token == null || !token.startsWith("Bearer ")) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        String cleanToken = token.replace("Bearer ", "");
        if (!authService.validateToken(cleanToken)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        // TODO: 这里未来可以修改为调用本地 Python Agent 的代码或者 HTTP 接口。
        // 现在作为演示，直接拼接字符串并回显给微信小程序客户端。
        String replyMessage = "Server Received: 【" + request.message() + "】 - 消息已被 Agent 接收并处理。";
        
        return ResponseEntity.ok(new MessageResponse(replyMessage));
    }
}