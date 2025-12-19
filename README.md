# 企业级自动化接口测试项目

## 项目概述

这是一个基于pytest的小型企业级自动化接口测试项目，集成了Allure报告和钉钉通知功能。

## 项目结构

```
autotextweb/
├── api/                    # API相关模块
│   ├── __init__.py
│   ├── request_handler.py   # 请求封装
│   └── endpoints.py         # API端点管理
├── config/                  # 配置文件
│   ├── __init__.py
│   └── config.py            # 配置管理
├── data/                    # 测试数据
│   ├── __init__.py
│   └── test_data.py         # 测试数据管理
├── logs/                    # 日志目录
├── photo/                   # 图片资源目录
├── reports/                 # 报告目录
│   ├── allure/              # Allure测试结果数据
│   └── allure-report/       # 生成的Allure报告
├── tests/                   # 测试用例
│   ├── __init__.py
│   └── test_sample_api.py   # 示例测试用例
├── utils/                   # 工具模块
│   ├── __init__.py
│   ├── logger.py            # 日志配置
│   └── dingtalk_notifier.py # 钉钉通知脚本
├── conftest.py              # pytest配置
├── pytest.ini               # pytest配置文件
├── requirements.txt         # 依赖管理
└── run_test_schedule.py     # 定时运行测试脚本
```

## 核心功能

1. **配置管理**：支持dev和prod多环境配置切换，可以通过环境变量或直接修改代码来切换环境
2. **日志管理**：使用loguru库，支持控制台和文件双输出，详细记录测试执行过程
3. **请求封装**：封装了GET、POST、PUT、DELETE等HTTP请求方法，统一处理请求头、超时等配置
4. **API端点管理**：集中管理所有API端点，便于维护和更新
5. **测试数据管理**：支持参数化测试数据，提高测试覆盖率
6. **Allure报告**：生成美观的测试报告，包含详细的测试步骤、断言结果和截图
7. **钉钉通知**：自动发送测试报告URL到钉钉群聊，便于团队及时获取测试结果
8. **定时任务**：支持定时自动运行测试、生成报告并发送通知，提高工作效率

## 技术栈

- **测试框架**：pytest
- **HTTP客户端**：requests
- **报告工具**：Allure
- **日志工具**：loguru
- **配置管理**：pyyaml
- **定时任务**：schedule
- **通知工具**：钉钉机器人

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
pytest
```

### 3. 生成Allure报告

```bash
allure generate reports/allure -o reports/allure-report --clean
```

### 4. 发送钉钉通知

```bash
python utils/dingtalk_notifier.py
```

### 5. 定时发送钉钉通知

修改 `utils/dingtalk_notifier.py` 文件，将最后一行的注释去掉，并设置合适的时间间隔：

```python
# 或者设置定时任务
notifier.schedule_notification(interval=60)  # 每60分钟发送一次
```

然后运行脚本：

```bash
python utils/dingtalk_notifier.py
```

### 6. 定时自动运行测试并发送报告

使用 `run_test_schedule.py` 脚本可以实现定时自动运行测试、生成报告并发送钉钉通知：

```bash
python run_test_schedule.py
```

该脚本会立即运行一次测试任务，然后按照配置的时间间隔定期执行。默认配置是每小时运行一次，你可以修改脚本中的时间配置：

```python
# 设置定时任务，每小时运行一次
schedule.every().hour.do(
    lambda: [run_tests(), generate_allure_report(), send_dingtalk_notification()]
)

# 也可以设置每天早上9点运行一次（已注释）
# schedule.every().day.at("09:00").do(
#     lambda: [run_tests(), generate_allure_report(), send_dingtalk_notification()]
# )
```

## 测试用例

项目包含23个示例测试用例，覆盖了：
- 用户管理（获取用户列表、获取单个用户、创建用户）
- 帖子管理（获取帖子列表、获取单个帖子、创建帖子、更新帖子、删除帖子）
- 评论管理（获取评论列表、获取帖子评论）
- 待办事项管理（获取待办事项列表、创建待办事项）
- 相册管理（获取相册列表、获取单个相册、创建相册、获取用户相册）
- 照片管理（获取照片列表、获取单个照片、创建照片、获取相册照片、上传照片）

## 钉钉机器人配置

1. 登录钉钉，进入群聊设置
2. 添加机器人，选择"自定义"
3. 配置机器人名称和安全设置（选择"自定义关键词"，并填写"自动测试"）
4. 复制webhook地址，替换 `utils/dingtalk_notifier.py` 中的 `webhook_url`

## 注意事项

1. 确保Allure已安装并添加到系统PATH中，以便生成报告
2. 确保钉钉机器人的webhook地址正确配置在`utils/dingtalk_notifier.py`中
3. 确保钉钉机器人的自定义关键词设置为"自动测试"
4. 运行定时任务脚本前，确保所有依赖已安装完成
5. 确保测试运行后生成了Allure报告数据，否则钉钉通知可能无法正确发送报告链接
6. 如需修改定时任务的执行频率，请编辑`run_test_schedule.py`中的相关配置

## 扩展建议

1. 添加数据库连接和数据验证
2. 实现接口自动化测试的CI/CD集成
3. 添加更多的测试用例和测试场景
4. 实现测试数据的动态生成
5. 添加接口性能测试功能

## 学习价值

1. 掌握自动化测试框架设计
2. 学习pytest测试框架
3. 了解Allure报告集成
4. 掌握API测试最佳实践
5. 学习企业级代码组织方式
6. 了解钉钉机器人集成
7. 学习定时任务实现

## 联系方式

如有问题或建议，请联系项目维护者。
