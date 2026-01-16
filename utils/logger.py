import logging
import os
import json

class Logger:
    """
    日志工具类，用于记录程序运行日志
    """
    
    def __init__(self, config_path="config.json"):
        """
        初始化日志配置
        
        Args:
            config_path: 配置文件路径
        """
        # 读取配置文件
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # 获取日志级别
        log_level = getattr(logging, config.get("log_level", "INFO"))
        
        # 创建日志记录器
        self.logger = logging.getLogger("file_transfer_tool")
        self.logger.setLevel(log_level)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # 创建文件处理器
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setLevel(log_level)
        
        # 定义日志格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """
        获取日志记录器
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        return self.logger

# 创建全局日志实例
logger = Logger().get_logger()