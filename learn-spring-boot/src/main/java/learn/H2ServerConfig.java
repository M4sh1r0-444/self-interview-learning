package learn;

import org.h2.tools.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.sql.SQLException;

/**
 * 把 H2 内存库通过 TCP 端口暴露出去，让 IDEA 等外部工具能直连。
 *
 * 背景：Spring Boot 4 移除了 h2-console 的自动配置（spring.h2.console.enabled 已失效），
 * 且 learn 工程用的是 H2 内存模式——默认只在本 JVM 内可见，外部进程连不进来。
 * 解法：手动启动 H2 自带的 TCP Server，IDEA 通过 jdbc:h2:tcp://localhost:9092/mem:learn 连入。
 *
 * 这也是 T1-1 理论的第一次实战：org.h2.tools.Server 是第三方 jar 里的类，
 * 你没法在它源码上加 @Service —— 只能用 @Configuration + @Bean 手动注册进容器。
 */
@Configuration
public class H2ServerConfig {

    @Bean(initMethod = "start", destroyMethod = "stop")
    public Server h2TcpServer() throws SQLException {
        // -tcpPort 9092    监听端口
        // -tcpAllowOthers  允许本机之外访问（开发机无碍）
        return Server.createTcpServer("-tcpPort", "9092", "-tcpAllowOthers");
    }
}
