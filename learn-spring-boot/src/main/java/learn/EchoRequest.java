package learn;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;

@Data
public class EchoRequest {
    @NotBlank(message = "name 不能为空")
    private String name;
}