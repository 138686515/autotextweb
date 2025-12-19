import os
from loguru import logger
from config.config import config


class Logger:
    """日志配置类"""
    
    def __init__(self):
        self.log_dir = config['LOG_DIR']
        self.log_level = config['LOG_LEVEL']
        self._setup_logger()
    
    def _setup_logger(self):
        """配置日志"""
        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 移除默认的控制台输出
        logger.remove()
        
        # 配置控制台输出
        logger.add(
            sink=lambda msg: print(msg, end=""),
            level=self.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True
        )
        
        # 配置文件输出
        logger.add(
            sink=os.path.join(self.log_dir, "api_test_{time:YYYY-MM-DD}.log"),
            level=self.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="00:00",  # 每天0点创建新日志文件
            retention="7 days",  # 保留7天日志
            encoding="utf-8"
        )


# 初始化日志实例
logger_instance = Logger()

# 导出logger供其他模块使用
log = logger
