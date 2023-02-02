package com.ssafy.plant.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ssafy.plant.config.oauth.OauthToken;
import com.ssafy.plant.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/oauth/token") // 프론트에서 인가코드 받아오는 url
    public OauthToken getLogin(@RequestParam("code") String code) throws JsonProcessingException {

        // 넘어온 인가코드로 accesstoken
        OauthToken oauthToken = userService.getAccessToken(code);

        // 발급 받은 accessToken으로 카카오 회원 정보 저장
        String User = userService.saveUser(oauthToken.getAccess_token());

        System.out.println("==========================================");
        System.out.println("==========================================");
        System.out.println("==========================================");
        System.out.println(oauthToken);
        System.out.println(User);
        System.out.println("==========================================");
        System.out.println("==========================================");
        System.out.println("==========================================");

        return oauthToken;
    }
}
