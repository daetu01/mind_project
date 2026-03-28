package com.dais.what.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/api/check")
    public String check() {
        return "백엔드 서버가 살아있습니다! DB 연결 대기 중.... 수정해볼게요";
    }
}
