package com.mimosa.server.utils;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * 微信工具类
 */
public class WechatUtil {
    
    private static final Logger log = LoggerFactory.getLogger(WechatUtil.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    // 微信 code2Session 接口地址
    private static final String CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session";
    
    /**
     * 调用微信 code2Session 接口获取 openid 和 session_key
     * @param appid 小程序 AppID
     * @param secret 小程序 AppSecret
     * @param jsCode 小程序登录凭证 code
     * @return 包含 openid、session_key 的 JsonNode
     */
    public static WechatSession getSession(String appid, String secret, String jsCode) {
        try {
            String urlString = String.format(
                "%s?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code",
                CODE2SESSION_URL, appid, secret, jsCode
            );
            
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();
            
            JsonNode jsonNode = objectMapper.readTree(response.toString());
            
            if (jsonNode.has("openid")) {
                String openid = jsonNode.get("openid").asText();
                String sessionKey = jsonNode.has("session_key") ? jsonNode.get("session_key").asText() : "";
                String unionid = jsonNode.has("unionid") ? jsonNode.get("unionid").asText() : "";
                
                log.info("微信 code2Session 成功：openid={}", openid);
                return new WechatSession(openid, sessionKey, unionid);
            } else {
                int errcode = jsonNode.has("errcode") ? jsonNode.get("errcode").asInt() : -1;
                String errmsg = jsonNode.has("errmsg") ? jsonNode.get("errmsg").asText() : "未知错误";
                log.error("微信 code2Session 失败：errcode={}, errmsg={}", errcode, errmsg);
                return null;
            }
            
        } catch (IOException e) {
            log.error("调用微信 code2Session 异常", e);
            return null;
        }
    }
    
    /**
     * 微信会话信息
     */
    public static class WechatSession {
        private final String openid;
        private final String sessionKey;
        private final String unionid;
        
        public WechatSession(String openid, String sessionKey, String unionid) {
            this.openid = openid;
            this.sessionKey = sessionKey;
            this.unionid = unionid;
        }
        
        public String getOpenid() {
            return openid;
        }
        
        public String getSessionKey() {
            return sessionKey;
        }
        
        public String getUnionid() {
            return unionid;
        }
    }
}
