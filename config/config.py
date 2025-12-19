import os
from typing import Dict, Any


class Config:
    """配置管理类"""
    
    # 基础配置
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 日志配置
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_LEVEL = 'INFO'
    
    # API配置
    API_TIMEOUT = 30
    
    # 测试报告配置
    REPORT_DIR = os.path.join(BASE_DIR, 'reports')
    ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, 'allure')  # Allure测试结果数据目录
    ALLURE_REPORT_DIR = os.path.join(REPORT_DIR, 'allure-report')  # 生成的Allure HTML报告目录
    
    @staticmethod
    def get_config(env: str = 'dev') -> Dict[str, Any]:
        """
        获取指定环境的配置
        :param env: 环境名称，可选值：dev, prod
        :return: 配置字典
        """
        configs = {
            'dev': {
                'BASE_URL': 'https://jsonplaceholder.typicode.com',
                'API_KEY': '',
            },
            'prod': {
                'BASE_URL': 'https://jsonplaceholder.typicode.com',  # 示例，实际应替换为生产环境URL
                'API_KEY': '',
            }
        }
        
        # 合并基础配置和环境配置
        base_config = {
            'BASE_DIR': Config.BASE_DIR,
            'LOG_DIR': Config.LOG_DIR,
            'LOG_LEVEL': Config.LOG_LEVEL,
            'API_TIMEOUT': Config.API_TIMEOUT,
            'REPORT_DIR': Config.REPORT_DIR,
            'ALLURE_RESULTS_DIR': Config.ALLURE_RESULTS_DIR,
            'ALLURE_REPORT_DIR': Config.ALLURE_REPORT_DIR,
        }
        
        env_config = configs.get(env, configs['dev'])
        base_config.update(env_config)
        
        return base_config


# 默认配置实例
config = Config.get_config(os.getenv('TEST_ENV', 'dev'))
