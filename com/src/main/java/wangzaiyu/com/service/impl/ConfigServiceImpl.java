package wangzaiyu.com.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import wangzaiyu.com.mapper.ConfigMapper;
import wangzaiyu.com.pojo.FederatedConfig;
import wangzaiyu.com.service.IConfigService;

@Service
public class ConfigServiceImpl extends ServiceImpl<ConfigMapper, FederatedConfig> implements IConfigService {
}
