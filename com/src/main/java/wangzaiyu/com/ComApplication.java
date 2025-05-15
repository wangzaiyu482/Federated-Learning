package wangzaiyu.com;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan("wangzaiyu.com.mapper")
@SpringBootApplication
public class ComApplication {

    public static void main(String[] args) {
        SpringApplication.run(ComApplication.class, args);
    }

}
