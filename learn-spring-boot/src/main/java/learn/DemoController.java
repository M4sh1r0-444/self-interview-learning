package learn;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class DemoController {
    private final WelcomeService welcomeService;
    private final UserRepository userRepository;

    public DemoController (WelcomeService welcomeService, UserRepository userRepository) {
        this.welcomeService = welcomeService;
        this.userRepository = userRepository;
    }

    @GetMapping("/demo")
    public String demo (@RequestParam String name) {
        return welcomeService.welcome(name);
    }

    @PostMapping("/echo")
    public String echo (@Valid @RequestBody EchoRequest request) {
        return "收到：" + request.getName();
    }

    @PostMapping("/users")
    public UserEntity save (@Valid @RequestBody UserRequest request) {
        UserEntity userEntity = new UserEntity();
        userEntity.setName(request.getName());
        userEntity.setAge(request.getAge());
        return userRepository.save(userEntity);
    }

    @GetMapping("/users/older-than")
    public List<UserEntity> olderThan (@RequestParam Integer age) {
        return userRepository.findByAgeGreaterThan(age);
    }

}
