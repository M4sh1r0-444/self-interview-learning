package learn;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {
    public String greet(String name) {
        return "你好, " + name + "!";
    }
}