import pytest
from api.request_handler import request_handler
from utils.logger import log


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """
    全局fixture，用于测试会话的setup和teardown
    :return:
    """
    log.info("=== 开始测试会话 ===")
    
    # 测试开始前的初始化工作
    # 这里可以添加一些全局的初始化代码，如数据库连接、测试数据准备等
    
    yield
    
    # 测试结束后的清理工作
    log.info("=== 结束测试会话 ===")
    # 关闭请求会话
    request_handler.close()


@pytest.fixture(scope="function", autouse=True)
def test_case_setup(request):
    """
    每个测试用例的setup和teardown
    :param request: pytest的请求对象
    :return:
    """
    test_name = request.node.name
    log.info(f"=== 开始测试用例: {test_name} ===")
    
    yield
    
    log.info(f"=== 结束测试用例: {test_name} ===")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    用于生成测试报告的钩子函数
    :param item: 测试用例对象
    :param call: 测试用例的调用对象
    :return:
    """
    outcome = yield
    report = outcome.get_result()
    
    # 为Allure报告添加测试用例的额外信息
    if report.when == "call":
        # 可以在这里添加一些自定义的报告信息
        pass
