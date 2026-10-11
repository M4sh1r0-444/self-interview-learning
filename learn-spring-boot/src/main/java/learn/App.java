package learn;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/*
 * T1-1 实验工程启动类。
 * 注意包名是 learn —— @SpringBootApplication 默认只扫描"启动类所在包及其子包"。
 */

@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
