package learn;

import org.springframework.stereotype.Service;

@Service
public class WelcomeService {
    private final GreetingService greetingService;

    public WelcomeService (GreetingService greetingService) {
        this.greetingService = greetingService;
    }
    public String welcome(String user) {
        return greetingService.greet(user) + " 欢迎学习 Spring";
    }
}