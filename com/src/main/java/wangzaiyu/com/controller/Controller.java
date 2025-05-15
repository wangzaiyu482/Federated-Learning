package wangzaiyu.com.controller;


import cn.hutool.json.JSONUtil;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;
import wangzaiyu.com.pojo.FedResult;
import wangzaiyu.com.pojo.FederatedConfig;
import wangzaiyu.com.pojo.Matrix;
import wangzaiyu.com.pojo.Result;
import wangzaiyu.com.service.IConfigService;

import java.util.*;

@Slf4j
@RestController
@RequestMapping
public class Controller {
    @Autowired
    private IConfigService configService;
    @Resource
    private StringRedisTemplate stringRedisTemplate;
    @Resource
    private ObjectMapper objectMapper;
    @GetMapping("/config")
    public FederatedConfig list(){
        log.debug("获取日志");
        List<FederatedConfig> federatedConfigList = configService.list();
        return federatedConfigList.get(0);
    }

    @PostMapping("/config")
    public Result update(@RequestBody FederatedConfig federatedConfig){
        federatedConfig.setId(1);
        configService.updateById(federatedConfig);
        return Result.success();
    }

    @GetMapping("/result/{algorithmType}")
    public List<FedResult> getFedResults(@PathVariable String algorithmType) throws Exception {
        // 1. 先匹配基础模式（不带括号部分）
        String basePattern = algorithmType +"*";
        Set<String> potentialKeys = stringRedisTemplate.keys(basePattern);
        if (potentialKeys == null || potentialKeys.isEmpty()) {
            return new ArrayList<>();
        }


        List<FedResult> results = new ArrayList<>();

        for (String key : potentialKeys) {
            // 3. 解析数据（同之前逻辑）
            String[] parts = key.split(" ");
            int round = Integer.parseInt(parts[1]);
            String aggType = key.substring(key.indexOf('(') + 1, key.indexOf(')'));

            String jsonValue = stringRedisTemplate.opsForValue().get(key);
            Matrix matrix = JSONUtil.toBean(jsonValue, Matrix.class);
            matrix.setLoss(matrix.getLoss());

            FedResult result = new FedResult();
            result.setAlgorithm(algorithmType);
            result.setAggregationType(aggType);
            result.setRound(round);
            result.setMatrix(matrix);
            // 其他字段设置...

            results.add(result);
        }

        results.sort(Comparator.comparing(FedResult::getRound)
                .thenComparing(FedResult::getAggregationType));
        return results;
    }
}