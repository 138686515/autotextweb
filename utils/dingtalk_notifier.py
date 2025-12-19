import os
import sys
import time
import requests
import socket
import schedule
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import log
from config.config import config


class DingTalkNotifier:
    """钉钉通知类"""
    
    def __init__(self):
        self.webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=994449cdb5a1f9546881a2de6cdcae4f4991f4746a6569a6f8efb6bdc7323361"
        self.keyword = "自动测试"
        self.report_dir = config['ALLURE_REPORT_DIR']
        self.port = 8080
    
    def get_local_ip(self) -> str:
        """
        获取本地局域网IP地址
        :return: 局域网IP地址
        """
        try:
            # 创建一个UDP套接字，连接到一个公共DNS服务器
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            log.error(f"获取本地IP失败: {str(e)}")
            return "127.0.0.1"
    
    def send_dingtalk_message(self, message: str):
        """
        发送钉钉消息
        :param message: 消息内容
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{self.keyword} {message}"
            }
        }
        
        try:
            response = requests.post(self.webhook_url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result["errcode"] == 0:
                log.info("钉钉消息发送成功")
            else:
                log.error(f"钉钉消息发送失败: {result['errmsg']}")
        except Exception as e:
            log.error(f"发送钉钉消息异常: {str(e)}")
    
    def start_report_server(self):
        """
        启动Allure报告HTTP服务器
        """
        # 检查是否已有进程在运行
        import subprocess
        import psutil
        
        # 检查端口是否被占用
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and f"python -m http.server {self.port}" in ' '.join(cmdline):
                    log.info(f"HTTP服务器已在端口{self.port}运行")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # 启动HTTP服务器
        log.info(f"启动HTTP服务器，端口: {self.port}")
        subprocess.Popen(
            ["python", "-m", "http.server", str(self.port), "--directory", self.report_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # 等待服务器启动
    
    def get_test_statistics(self):
        """
        获取测试结果统计信息
        :return: 测试统计信息字典
        """
        log.info("获取测试结果统计信息")
        
        # Allure测试结果数据目录
        allure_results_dir = config['ALLURE_RESULTS_DIR']
        
        # 初始化统计结果
        stats = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "broken": 0,
            "skipped": 0
        }
        
        try:
            # 遍历allure结果目录下的json文件
            for filename in os.listdir(allure_results_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(allure_results_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 检查是否是测试结果文件
                    if isinstance(data, dict) and data.get('uuid') and data.get('status'):
                        stats["total"] += 1
                        status = data["status"]
                        if status == "passed":
                            stats["passed"] += 1
                        elif status == "failed":
                            stats["failed"] += 1
                        elif status == "broken":
                            stats["broken"] += 1
                        elif status == "skipped":
                            stats["skipped"] += 1
            
            log.info(f"测试结果统计: {stats}")
        except Exception as e:
            log.error(f"获取测试统计信息失败: {str(e)}")
        
        return stats
    
    def notify_report_url(self):
        """
        发送报告URL通知
        """
        log.info("开始发送Allure报告URL通知")
        
        # 启动报告服务器
        self.start_report_server()
        
        # 获取本地IP
        local_ip = self.get_local_ip()
        
        # 构建报告URL
        report_url = f"http://{local_ip}:{self.port}"
        
        # 获取测试结果统计信息
        stats = self.get_test_statistics()
        
        # 构建测试结果统计信息
        stats_message = f"\n测试结果统计:\n" \
                       f"总用例数: {stats['total']}\n" \
                       f"通过: {stats['passed']}\n" \
                       f"失败: {stats['failed']}\n" \
                       f"错误: {stats['broken']}\n" \
                       f"跳过: {stats['skipped']}"
        
        # 发送钉钉消息
        message = f"Allure报告已生成，访问地址: {report_url}{stats_message}"
        self.send_dingtalk_message(message)
        
        log.info(f"Allure报告URL: {report_url}")
    
    def schedule_notification(self, interval: int = 60):
        """
        定时发送通知
        :param interval: 时间间隔，单位：分钟
        """
        log.info(f"设置定时任务，每{interval}分钟发送一次报告URL")
        
        # 立即发送一次
        self.notify_report_url()
        
        # 设置定时任务
        schedule.every(interval).minutes.do(self.notify_report_url)
        
        # 循环执行
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    import subprocess
    
    # 生成Allure报告
    log.info("生成Allure报告")
    try:
        # 尝试生成Allure报告
        subprocess.run(["allure", "generate", config['ALLURE_RESULTS_DIR'], "-o", config['ALLURE_REPORT_DIR'], "--clean"], check=True)
        log.info("Allure报告生成成功")
    except FileNotFoundError:
        log.error("未找到allure命令，请确保已安装Allure并添加到系统PATH中")
    except subprocess.CalledProcessError as e:
        log.error(f"生成Allure报告失败: {str(e)}")
    except Exception as e:
        log.error(f"生成Allure报告异常: {str(e)}")
    
    # 初始化钉钉通知器
    notifier = DingTalkNotifier()
    
    # 发送一次通知
    notifier.notify_report_url()
    
    # 或者设置定时任务
    # notifier.schedule_notification(interval=60)
