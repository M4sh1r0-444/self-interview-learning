# 工作区说明：InterviewGuide 项目学习

> 本文件是 ZCode 工作区指令文件，**每次新会话自动加载**。用途：让任何新会话立即了解学习背景与当前进度，按既定方案继续辅导。

## 1. 工作区背景（每个会话必读）

- **学习者画像**：Java 后端初学者，**对项目中用到的框架和中间件（Redis、PostgreSQL、pgvector、Spring AI 等）默认零基础**，有 Java 基础语法；**有基础 SQL 能力（学过 MySQL 和 GaussDB）**——涉及 SQL 教学时跳过基础 CRUD/JOIN，聚焦 PG 特性与项目实战。学过原生 Servlet 写法（doGet/doPost），讲 Spring MVC 可用它做类比。
- **学习目标**：以 InterviewGuide 项目为主线，先补技术地基、再看项目落地，最终掌握：Spring Boot 工程体系、JPA/Flyway、Redis 全家桶（缓存/Stream/Lua）、AOP、异步任务、Spring AI、RAG、SSE、WebSocket 等。
- **方案设计原则**（新会话辅导时必须遵守）：
  1. **技术补课先行**：每项技术在项目里首次登场前，先完成对应的「技术补课块」（T 块）——只学到"够看懂项目"的深度，不做全面课程；
  2. **先黑盒后拆**：暂时用不到的机制（如阶段 4 的 Redis Stream）先当黑盒；
  3. **每阶段必须动手**：改配置/Prompt/加字段，跑通才算学会；
  4. **入口永远是 Controller**，沿 Controller → Service → Repository 追代码。
- **关键路径**：
  - 项目源码（已本地部署）：`D:\aiface\interview-guide`（Spring Boot 4.1 + Java 25 + Spring AI 2.0；后端 `app/`、前端 `frontend/`）
  - 配套教程（30 篇）：`D:\aiface\yuque-springai`（01 环境 / 02 核心功能 12 篇 / 03 进阶 5 篇 / 04 面试 9 篇）
  - 学习方案人读版（详细自检清单）：`D:\aiface\InterviewGuide学习方案.md`
- **部署状态**（2026-09-29 由 ZCode 完成）：

| 服务 | 地址 / 凭证 |
|---|---|
| 前端 | http://localhost:5173 |
| 后端 API | http://localhost:8080（Swagger: /swagger-ui.html） |
| PostgreSQL | localhost:5432，postgres / 123456，库 interview_guide |
| Redis | localhost:6379 |
| RustFS 控制台 | http://localhost:9001，rustfsadmin / rustfsadmin |

- `.env` 在项目根目录已建好（`AI_BAILIAN_API_KEY` 已填真实 Key；`RUSTFS_RPC_SECRET`、`APP_AI_CONFIG_ENCRYPTION_KEY` 已生成——注意 `.env.example` 缺前者，照抄会启动失败）。
- Docker Hub 直连不通，拉镜像走 `docker.m.daocloud.io/<image>` 再 `docker tag`。
- 启停：`docker compose -f docker-compose.dev.yml up -d`（项目根）；后端 `./gradlew :app:bootRun`；前端 `cd frontend && pnpm dev`。

## 2. 对本工作区 AI 会话的行为要求

1. 学习辅导任务：先读「学习进度」，从当前阶段接续；讲解任何技术前先确认对应 T 块是否已学完，没学就先补课再进项目代码。
2. 讲解代码精确到类名与文件路径；补课讲解要配可独立运行的小实验（脱离项目）。
3. 用户完成一个阶段/实验后，**更新本文件末尾「学习进度」**。
4. 修改学习方案时：本文件与 `InterviewGuide学习方案.md` **同步修改**，以本文件为准。
5. 端口注意：用户要用 IDEA Debug 启动后端前，先停掉后台 8080 的 bootRun 任务。
6. 全程中文；多讲"为什么这么设计"。

## 3. 技术栈覆盖矩阵（技术 → 补课块 → 项目落点）

| 技术 | 补课块 | 项目中的落点 |
|---|---|---|
| Docker / Compose | T0 | 依赖容器、docker-compose.dev.yml |
| Gradle | T0 | build.gradle、bootRun |
| HTTP / REST / JSON | T1 | 全部 Controller |
| Spring Boot 核心（IoC/DI/自动配置） | T1 | 全项目 Bean 装配、App.java |
| Spring MVC + Validation | T1 | Controller、@Valid、全局异常 |
| Lombok | T1 | @Data/@Slf4j |
| SpringDoc / Swagger | T1 | OpenApiConfig、接口文档 |
| SQL / PostgreSQL | T1 | 全部 Repository、迁移脚本 |
| Spring Data JPA / Hibernate | T1 | Entity、Repository、ddl-auto: validate |
| Flyway | T1 | db/migration/ |
| MapStruct | T1 | infrastructure/mapper/ |
| Apache Tika | T2 | DocumentParseService |
| 对象存储 / S3 协议 | T2 | FileStorageService、RustFS |
| 内容哈希（SHA-256） | T2 | FileHashService |
| LLM 基础（Token/温度/Prompt/结构化输出/Embedding） | T3（教程02-02） | 全部 AI 功能 |
| Spring AI（ChatClient/Advisor/VectorStore） | T3 | common/ai |
| OpenAI 兼容 API 生态 | T3/T7 | LlmProviderRegistry |
| Jackson（JSON↔对象） | T4 | 结构化输出解析、JacksonConfig |
| Prompt 工程 | T4 | resources/prompts/ |
| iText 8 / PDF | T4 | PdfExportService |
| Java 并发（线程池/守护线程/Atomic/优雅关闭） | T5 | AbstractStreamConsumer |
| Redis 核心（类型/过期/持久化/为什么快） | T5 | RedisService、各类缓存 |
| Redis Stream（消费者组/ACK/pending） | T5 | common/async、各 listener |
| Redisson | T5 | 连接与 Stream API |
| 设计模式（模板方法/策略/注册表） | T5/T7/T8 | async 模板、路由、出题策略 |
| pgvector（向量/相似度/索引） | T6 | VectorRepository、vector_store 表 |
| SSE | T6 | RagChatController |
| Micrometer 埋点 | T6/10C | RagMetrics |
| AES-GCM 加密 | T7 | ApiKeyEncryptionService |
| 状态机（FSM） | T8 | InterviewSessionService |
| 缓存模式（cache-aside/一致性） | T8 | InterviewSessionCache |
| AOP / 动态代理 | T10A | RateLimitAspect |
| Lua 脚本 + 限流算法 | T10A | rate_limit_single.lua |
| Prompt 注入防御 | T10B | PromptSanitizer |
| WebSocket | T10C | VoiceInterviewWebSocketHandler |
| DashScope SDK（ASR/TTS） | T10C | QwenAsrService/QwenTtsService |
| 虚拟线程（Java 21+） | T10C | 线程模型配置 |
| React/TS/Vite（了解即可） | 附录 | frontend/ |

## 4. 学习方案总纲（11 阶段 + 技术补课块，约 16 周）

每阶段结构：**T 块（技术补课，脱离项目的小实验）→ 教程阅读 → 项目代码阅读 → 动手实验 → 自检**。
⭐ = 教程核心必读；📍 = 建议打断点的代码入口；T 块时长为纯补课时间，已计入各阶段总时长。

| 阶段 | 周次 | 主题 | 技术补课块（T） | 项目实战产出 |
|---|---|---|---|---|
| 0 | 1 前半 | 环境与项目全景 | T0 Docker/Gradle | 功能↔接口地图 |
| 1 | 1-2 | 一次 Web 请求的生命周期 | T1 Spring Boot/JPA/SQL/Flyway/Lombok/MapStruct | 加字段全链路 |
| 2 | 3 前半 | 文件上传与解析 | T2 Tika/对象存储/哈希 | 八步流水线 |
| 3 | 3-4 | 大模型基础与 Spring AI | T3 LLM 概念/Spring AI/OpenAI 生态 | 能调通并解释 AI 接口 |
| 4 | 4-5 | 简历分析闭环 | T4 Jackson/Prompt/iText | 改 Prompt 加评分维度 |
| 5 | 5-6 | Redis Stream 异步 | T5 Redis 核心/Java 并发/Stream 命令 | 消费者组/重试/恢复 |
| 6 | 7-8 | RAG 全链路 | T6 pgvector/SSE | 向量入库→检索→流式问答 |
| 7 | 9 前半 | 多模型路由 | T7 AES-GCM/配置体系 | 热更新与 Key 加密 |
| 8 | 9-10 | 模拟面试 | T8 状态机/缓存模式 | FSM + 评估引擎 + 自建 SKILL |
| 9 | 11 | 知识库题库面试 | （复用 T3-T8 全部） | 综合闭环检验 |
| 10 | 12-13 | 进阶主题 | T10 AOP/Lua/限流算法/WebSocket/虚拟线程 | 限流+注入防御（语音选学） |
| 11 | 14+ | 面试冲刺 | — | 简历 + 9 篇面试题 |

快速模式（6 周）：T 块只做加粗核心概念、跳过选学项，阶段 2/7/9 泛读，语音放弃。

## 5. 各阶段详情

### 阶段 0：环境与项目全景（第 1 周前半）
**T0 补课**（Docker 1.5h + Gradle 0.5h）：
- Docker：镜像 vs 容器、端口映射、数据卷、`docker run/ps/exec/logs`；实验：`docker run -d -p 6380:6379 redis:7` 再 `docker exec` 进去 `redis-cli ping`，理解 compose 只是把这些声明成文件
- Gradle：只需"build.gradle=pom、依赖/任务/插件"三层认知；实验：看懂 `app/build.gradle` 里的依赖块
**教程**：`00-项目介绍.md`；`01-环境搭建/` 4 篇（跳过实操读原理；01-01 "PGvector 向量功能"节精读）
**代码**：README 项目结构；`App.java`（为何排除 Spring AI 自动配置→阶段 7 揭晓）；`docker-compose.dev.yml`；`application.yml` 通读
**实验**：F12+Swagger 操作 6 大功能，记接口路径
**自检**：三层结构职责？PG/Redis/RustFS 角色？容器和镜像的区别？

### 阶段 1：一次 Web 请求的生命周期（第 1-2 周）
**T1 补课**（约 8h，本阶段最大地基）：
- **Spring Boot 核心**（3h）：IoC/DI 是什么、Bean 与容器、`@Component/@Service/@Configuration` 三件套、自动配置概念；实验：新建一个最小 boot 工程写两个 Bean 互相注入，用 `/actuator/beans` 观察项目里的 Bean
- **Spring MVC**（1h）：@RestController/@GetMapping/@RequestBody/@PathVariable、@Valid 校验；对照 F12 看请求
- **SQL/PostgreSQL**（2h）：建表/主外键/索引作用/基本 CRUD 与 JOIN；实验：IDEA Database 连库，手写 SQL 查 interview_schedule 全部字段，再 JOIN 查某会话的题目
- **JPA**（1.5h）：Entity↔表映射、Repository 方法名派生查询、JPQL 与原生 SQL 区别；实验：给 Repository 临时加一个派生方法并调用
- **Flyway/Lombok/MapStruct/Swagger**（1.5h）：版本化迁移为什么必要；Lombok 编译期生成 getter；MapStruct 编译期生成映射；Swagger 注解一瞥
**教程**：`03-01 MapStruct` 前半
**代码**：`common/result/Result` → `common/exception/` 三类 → 📍`interviewschedule/InterviewScheduleController` → Service → Repository → model/（对照 V1__init_schema.sql）→ `ScheduleStatusUpdater`（@Scheduled）→ `common/config/`（Cors/Jackson/OpenApi）→ `infrastructure/mapper/`
**实验**：① 停后台后端→IDEA Debug→Controller 断点→页面创建日程→单步全链路；② 加 remark 字段（Entity+Flyway 迁移+DTO+Mapper+前端）
**自检**：请求经过哪几层？DI 让代码好在哪？Entity/DTO 为何分离？validate+Flyway 分工？全局异常如何兜底？

### 阶段 2：文件上传与解析（第 3 周前半）
**T2 补课**（约 3h）：
- Tika（1h）：它是"格式探测器+内容提取器"，支持 PDF/DOCX/TXT 等；实验：建临时 main 调 Tika facade 解析本机 PDF
- 对象存储/S3（1.5h）：bucket/key/PUT/GET 概念，与文件系统区别（为什么简历存 S3 而不是服务器磁盘/数据库）；实验：RustFS 控制台手动上传下载一个文件
- 内容哈希（0.5h）：SHA-256 是什么、为何能判重、彩虹表一句话
**教程**：⭐`02-01 Tika`（八步流水线/解析优化/文本清洗精读；"异步分析"节当黑盒）
**代码**：`infrastructure/file/` 7 类：📍`FileValidationService`→`DocumentParseService`→`TextCleaningService`→`FileHashService`→`FileStorageService`；组装层 `ResumeUploadService`
**实验**：T2 的 Tika main 复用；传改名 exe 看校验拦截；RustFS 找到上传的简历原件
**自检**：为何靠内容魔数而非扩展名判型？哈希去重在流水线哪一步？清洗过滤什么？

### 阶段 3：大模型基础与 Spring AI 集成（第 3-4 周）
**T3 补课**（教程 02-02 本身就是系统补课，另加 1.5h OpenAI 生态）：
- OpenAI 兼容 API（1.5h）：`/chat/completions` 与 `/embeddings` 请求长什么样、base_url/api_key/model 三要素、为什么国内模型都兼容它；实验：用 curl 直接调 DashScope 的 OpenAI 兼容端点发一条消息（Key 在 .env）
**教程**：⭐`02-02 大模型核心概念`（Embedding/RAG 节只求印象，阶段 6 精读）；⭐`02-03 Spring AI 集成`（"别让 Service 直接依赖 ChatClient"、Advisor 链、结构化输出可靠性）
**代码**：📍`common/ai/StructuredOutputInvoker`；`resources/prompts/resume-analysis-*.st`；`PromptSanitizer` 粗读；`LlmEmbeddingConfig`
**实验**：Swagger 调 JD 解析接口；改 Temperature 对比两次输出稳定性；T3 的 curl 实验
**自检**：温度高/低适合什么场景？结构化输出不合法怎么兜底？为何隔一层不直接持有 ChatClient？chat 模型和 embedding 模型区别？

### 阶段 4：第一个 AI 业务闭环——简历分析（第 4-5 周）
**T4 补课**（约 3h）：
- Jackson（1h）：JSON↔Java 对象互转、@JsonProperty/忽略未知字段；实验：把一段 JSON 字符串转对象再转回去
- Prompt 工程方法论（教程 02-05 即补课）；iText（1h）：PDF 结构与字体嵌入概念
- 教程即补课：⭐`02-05 结构化 Prompt`；`02-11 iText PDF`
**代码**：📍`ResumeGradingService`（Prompt 组装→结构化输出）；`ResumePersistenceService`；`ResumeAnalysisEntity`；`ResumeHistoryService`；`PdfExportService`；`AnalyzeStreamConsumer`（只看调用关系）
**实验**：断点跟踪分析全程；给 system.st 加"沟通表达"维度验证；导出 PDF；故意改错 API Key 观察失败（铺垫阶段 5）
**自检**：system/user prompt 分工？AI 的 JSON 怎么变成 Entity？PDF 为何内嵌中文字体？

### 阶段 5：异步任务——Redis Stream（第 5-6 周）
**T5 补课**（约 7.5h，本项目最重要的中间件地基）：
- **Redis 核心**（3h）：是什么(内存 KV)、五大类型 string/hash/list/set/zset、EXPIRE、为什么快(内存+单线程模型+IO 多路复用一句话)、持久化 RDB/AOF 概念；实验：redis-cli 对每种类型做 set/get/hset/lpush/zadd，SETEX 后 TTL 观察
- **Java 并发**（2h）：线程池七参数、守护线程、AtomicBoolean、shutdown 优雅关闭；实验：写 main 用 ThreadPoolExecutor 提交 3 个任务再 shutdown，观察队列行为
- **Redis Stream 命令**（1.5h）：XADD/XLEN/XRANGE/XGROUP/XREADGROUP/XACK/XPENDING；实验：redis-cli 裸敲一遍完整"生产-消费-ACK-pending-再认领"流程
- Redisson（1h）：它只是"更好用的 Redis 客户端+分布式数据结构"，项目里 Stream 操作经它封装
**教程**：⭐`03-02 Redis Stream 异步任务`（为何选 Stream vs MQ、整体流程、为何提取抽象类、重试）
**代码**：`AsyncTaskStatus`+`AsyncTaskStreamConstants` → 📍`AbstractStreamProducer` → 📍`AbstractStreamConsumer`（对照 T5 线程池实验理解 init()）→ `AnalyzeStream*` → `ResumeAnalysisRecoveryScheduler` → 对照 `VectorizeStream*` 验证模板理解
**实验**：`XINFO GROUPS`/`XPENDING` 观察真实任务；改错 Key 看重试 3 次；改回后手动重析成功
**自检**：为何不用 Kafka/PG 轮询？消费者组/pending/ACK 关系？重启怎么找回半途任务？模板方法：子类实现什么基类管什么？

### 阶段 6：RAG 知识库全链路（第 7-8 周）
**T6 补课**（约 3.5h）：
- **pgvector**（2.5h）：向量=数字数组、余弦相似度(`<=>`)/内积/欧氏距离、维度、ivfflat vs hnsw 索引一句话、`CREATE EXTENSION vector` 与 vector 列建表；实验：直接在 PG 里 `CREATE TABLE t(v vector(3))` 插 3 行手写 `ORDER BY v <=> '[1,0,0]'` 感受语义检索
- **SSE**（1h）：轮询/长轮询/SSE/WebSocket 四种实时方案对比、`text/event-stream` 格式（event/data 字段）；实验：`curl -N` 看任一 SSE 接口的原始流
**教程**：回头精读 02-02 的 Embedding/RAG 节；⭐`02-08 SpringAI+pgvector RAG`；`02-09 RAG 优化`；`02-10 SSE`
**代码**（`modules/knowledgebase/`）：入库：📍`KnowledgeBaseUploadService`→`KnowledgeBaseVectorService`→`VectorizeStream*`（复用 T5）→`VectorRepository`+查 vector_store 表（对照 T6 实验）；问答：📍`KnowledgeBaseQueryService`（改写→TopK→拼上下文）→`KnowledgeBaseQueryProperties`→`RagChatController`（SSE）→`RagChatSessionService`/`RagQueryExecution`→`RagMetrics`（Micrometer 一瞥）
**实验**：上传→查向量表→提问→断点看改写与 TopK→curl -N 看 SSE；短查询追问实验；TopK 调 1 vs 10 对比
**自检**：文档到可检索的数据形态变化？阈值/TopK 作用？为何查询改写？SSE vs WebSocket 怎么选？

### 阶段 7：多模型路由与运行时配置（第 9 周前半）
**T7 补课**（约 2h）：
- AES-GCM（1h）：对称加密、GCM 相比 CBC 多了"认证"（防篡改）、nonce 为什么绝不能复用；实验：Java `Cipher` 加解密一段文本
- @ConfigurationProperties 配置体系（1h）：配置如何绑定成类型化对象、yaml 覆盖顺序
**教程**：`02-04 多 LLM 路由`（一台 Registry 三种 ChatClient；DB+YAML 双写；reload 热更新）
**代码**：📍`common/ai/LlmProviderRegistry`；`ApiPathResolver`；`llmprovider/service/`（Config/ApiKeyEncryption/Bootstrap）；`LlmProviderProperties`；`~/.interview-guide/llm-providers.yml` 实物
**实验**：设置页加 Provider 测连通/失败路径；设默认；调 `/api/llm-provider/reload`；验证 Key 落盘非明文
**自检**：DB+YAML 兜底解决什么？切换模型为何不用重启？GCM 的 G 是什么好处？

### 阶段 8：模拟面试——状态机与统一评估引擎（第 9-10 周）
**T8 补课**（约 2h）：
- 状态机（1h）：状态/事件/迁移/非法迁移拒绝；实验：用 enum+switch 写一个订单状态机小 demo
- 缓存模式（1h）：cache-aside 读写流程、一致性问题的根源、穿透/击穿/雪崩概念级
**教程**：⭐`02-06 模拟面试`（FSM/双层缓存断点续答/双路出题/评估管线）；`02-07 Skills 架构`
**代码**：`resources/skills/java-backend/SKILL.md`+references；📍`skill/InterviewSkillService`；`InterviewQuestionService`（双路+去重）；`InterviewSessionService`（FSM，对照 T8 demo）；`infrastructure/redis/InterviewSessionCache`（对照 T8 缓存模式）；`common/evaluation/UnifiedEvaluationService`（分批→汇总→降级）；`EvaluateStream*`；`InterviewPersistenceService`
**实验**：完整面试一场+redis-cli MONITOR 看会话 key；手绘状态机图（标注状态存 Redis/DB）；复制 skill 为 `my-custom` 改后开一场；交卷跟踪评估分批
**自检**：状态为何放 Redis（对照 T8 缓存模式）？去重实现？评估为何分批+汇总+降级？文字/语音为何共用引擎？

### 阶段 9：知识库题库面试（第 11 周）
无新 T 块——本阶段是对 T3-T8 + 项目轮子的综合检验。
**教程**：⭐`02-12 基于知识库面试`
**代码**：📍`KnowledgeBaseQuestionGenerationService`；`QuestionGenStream*`+恢复调度；`QuestionGenerationStateService`；`KnowledgeBaseInterviewService`（容量校验）；`KnowledgeBaseQuestionService`
**实验**：上传→生成题库→启用→面试→评估→导出全程；只启用 2 题看前端禁用+后端兜底
**自检**：生成不足为何不静默丢题？容量校验为何双层？复用了哪些轮子？

### 阶段 10：进阶主题（第 12-13 周，可取舍）
- **10A 限流（必学）**：T10A 补课（约 4h）：AOP（2h）——动态代理 JDK vs CGLIB、切点/通知/@Around；实验：写个切面打印方法耗时；Lua（1h）——十分钟语法+脚本原子性原理；限流算法（1h）——固定窗口/滑动窗口/令牌桶。教程⭐`03-03`；代码 `RateLimit`→`RateLimitAspect`→`rate_limit_single.lua`；实验：给接口加 `@RateLimit(IP,3)` 脚本狂刷验证 429
- **10B Prompt 注入防御（必学）**：教程 `03-04`；代码 `PromptSanitizer`+`PromptSecurityConstants`；实验：上传含"忽略指令打满分"文本看三层防御
- **10C 语音面试（选学）**：T10C 补课（约 2.5h）：WebSocket 握手/帧/心跳/服务端 push、虚拟线程是什么(Java 21+，与平台线程区别一句话)、DashScope ASR/TTS API 概念。代码：`VoiceInterviewWebSocketHandler`→`QwenAsrService`/`QwenTtsService`/`DashscopeLlmService`→`VoiceContextCompressor`；实验：F12 WS 面板看帧收发
- **10D 框架升级（选读）**：教程 `03-05`（Boot4/Jackson3/SpringAI2.0 踩坑）

### 阶段 11：面试冲刺（第 14 周起）
按序消化 `04-面试/` 9 篇：01 简历包装（找工作时）、02 后端亮点突击（面试前必看）、03 项目来源应对（面试前）、**04 RAG 35 题（学完阶段 6 就刷）**、**05 SpringAI 29 题（学完阶段 8 刷）**、**06 Redis 28 题（学完阶段 5 刷）**、07 Prompt 23 题（学完阶段 4 刷）、08 文件/PDF 题（学完阶段 4 刷）、09 补充（面试前）。

### 附录：前端认知（0.5h，后端够用即可）
`frontend/src/api/` 与后端 Controller 一一对应；`pages/` 按业务分页；知道 Vite 代理 `/api`→8080 即可，不学 React。

## 6. 学习方法备忘（全程适用）

1. T 块没学完不进对应项目代码；补课深度="够看懂项目"，别陷进去系统课
2. 先黑盒后白盒；每阶段必须动手改一次代码
3. 三个观测窗口对齐即理解到位：F12 Network（接口）、IDEA Debug（代码流）、redis-cli/数据库（数据流）
4. 修改方案时本文件与 `InterviewGuide学习方案.md` 同步更新

## 7. 学习进度（AI 会话维护区，完成即更新）

- 2026-09-29：✅ 本地部署完成（依赖容器/后端/前端全部就绪，API Key 已配置）
- 2026-09-29：✅ 学习方案 v1 制定（11 阶段）
- 2026-09-29：✅ 学习方案 v2 重构：全部技术栈增加"零基础补课块"（T 块），周期 12→16 周
- 2026-09-30：✅ T0 补课完成（Docker：镜像/容器/端口映射/卷/compose 对照 + learn-redis 实验；Gradle：插件/依赖/任务三层认知 + 依赖作用域 + version catalog + bootRun 注入 .env 原理）
- 2026-10-01：✅ T1-1 完成（IoC/DI/容器/构造器注入/自动配置；learn-spring-boot 实验工程全链路跑通：三层 Bean 注入 + /demo 接口 + 删 @Service 启动熔断实验 + 自检四题；附赠踩坑：pluginManagement 仓库、Windows 孤儿进程占端口排查 netstat/taskkill）
- 2026-10-03：✅ T1-2 完成（Spring MVC：请求旅程/DispatcherServlet、@RestController、REST 动词、三种参数来源、@Valid 校验、Result 统一返回、GlobalExceptionHandler、Jackson 消息转换器与 getter 驱动；对照原生 Servlet 讲透"声明式+控制反转的流程层"；实验：/echo POST + @RequestBody + @Valid 两条 curl 验证，观察到默认 400 响应不含校验 message——理解全局异常处理器的必要性；踩坑：starter-validation 需手动引入、Lombok 依赖补齐、无法解析符号=classpath 诊断公式）
- 2026-10-06：✅ T1-3 完成（SQL/PostgreSQL：按"有 MySQL/GaussDB 基础"重新定位——MySQL→PG 差异速查（schema 三层/identity/大小写敏感/CHECK/ILIKE）、pgvector 白话版（语义指纹/意义地图/<=> 余弦距离/HNSW 一句话）、17 张表业务认亲、IDEA Database 连库 + INSERT/查询/JOIN/sessions-answers 外键实验 + 3 维玩具向量检索实验；自检四题通过。附：Docker Desktop 开机不自动启动需手动拉起+compose up）
- 2026-10-09：✅ T1-4 完成（JPA：ORM 映射三分对照、Entity 注解逐个对照表结构、Repository 三种查询姿势（继承/派生/@Query JPQL）、ddl-auto validate vs create、Entity/DTO 分离伏笔；learn 工程 JPA+H2 实战：UserEntity/UserRepository/POST+派生查询、建表与 insert 的 SQL 直播；自检五题通过（@Column 方向、Flyway 管表权、ORDINAL 死穴已补讲）。踩坑四连：Boot4 移除 h2-console（查 beans+依赖树+Maven Central 定位）、H2 runtimeOnly→implementation（作用域实战）、curl.exe 中文 GBK 编码 400（IDEA HTTP Client 替代）、H2 TCP Server @Bean 直连 IDEA）
- 2026-10-11：📦 学习资料交接至 GitHub（M4sh1r0-444/self-interview-learning）：主项目源码（剥离 .git/build/node_modules/.env）+ learn 实验工程 + 教程 30 篇 + 学习方案 + 本文件 + 交接文档（新机器恢复手册/已知坑速查/密钥说明）。安全处理：.env 未上传（本机已换占位符）、SETUP_API_KEYS.md 已脱敏、.env.example 已补 RUSTFS_RPC_SECRET
- **当前位置：阶段 1 · T1-5 Flyway/Lombok/MapStruct/Swagger（课程已讲，实验+自检四题未做）**
- 待办：T1-5 实验+自检 → 教程 03-01 前半 → 项目代码全链路 → 断点+加字段实验
- 进度备注：（无）
