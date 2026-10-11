# InterviewGuide 项目学习仓库

以 [InterviewGuide](interview-guide/)（Spring Boot 4.1 + Java 25 + Spring AI 2.0 的 AI 面试平台）为主线的手把手学习仓库，含自建实验工程与配套教程。

## 快速导航

- 🚀 **换新机器？** 先读 [交接文档.md](交接文档.md) —— 十分钟恢复全部环境与进度
- 📈 **看进度？** [AGENTS.md](AGENTS.md) 末尾「学习进度」是唯一权威（AI 会话自动读取接续辅导）
- 📚 **看学习路线？** [InterviewGuide学习方案.md](InterviewGuide学习方案.md)（11 阶段 / 16 周 / T 补课块体系）

## 目录

```
interview-guide/          # 主项目源码（Boot 4.1 后端 app/ + React 前端 frontend/）
learn-spring-boot/        # T1 补课自建实验工程（迷你 Spring Boot + H2）
yuque-springai/           # 配套教程 30 篇
AGENTS.md                 # 工作区指令 + 学习进度（权威）
InterviewGuide学习方案.md  # 学习方案人读版
交接文档.md                # 新机器恢复手册 + 已知坑速查表
```

## 本地开发一句话

```bash
cd interview-guide
docker compose -f docker-compose.dev.yml up -d   # PG + Redis + RustFS
./gradlew :app:bootRun                            # 后端 :8080
cd frontend && pnpm dev                           # 前端 :5173
```

> `.env` 不在仓库中（密钥安全），恢复方法见交接文档第四节。
