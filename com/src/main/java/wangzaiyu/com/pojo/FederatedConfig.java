package wangzaiyu.com.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@TableName("federated_learning_configs")
@Data
public class FederatedConfig {
        @TableId(type = IdType.AUTO)
        private int id;
        private int numEpochs;
        private String serverAddress;
        private int numClients;
        private double fractionFit;
        private double fractionEvaluate;
        private int minFitClients;
        private int minEvaluateClients;
        private int minAvailableClients;
        private double proximalMu;
        private double clientLr;
        private int localEpochs;
        private String strategy;
}
