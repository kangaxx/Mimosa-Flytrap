package com.mimosa.server.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;

@RestController
@RequestMapping("/api/v1")
public class AgentController {

    @GetMapping("/status")
    public String getStatus() {
        return "Agent connection is active";
    }
}
