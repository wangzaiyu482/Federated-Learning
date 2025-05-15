package wangzaiyu.com.pojo;

import lombok.Data;

@Data
public class Matrix {
    private double accuracy;      // 准确率
    private double loss;          // 损失值
    private double recall;        // 召回率
    private double precision;     // 精确率
    private double F1;            // F1分数
    private String matrix;        // 混淆矩阵（JSON字符串形式）
}
