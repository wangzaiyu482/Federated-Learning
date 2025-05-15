package wangzaiyu.com.pojo;

import lombok.Data;

@Data
public class FedResult {
    private String algorithm;       // 算法类型（如 FedAvg）
    private String aggregationType; // 聚合类型（Training/Validation）
    private String type;          // 类型，如 "Training" 或 "Validation"
    private int round;            // 轮次
    private Matrix matrix;
}