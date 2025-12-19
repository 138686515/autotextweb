import os
import sys
import time
import subprocess
import schedule

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import log
from config.config import config


def run_tests():
    """
    运行测试用例
    """
    log.info("=== 开始运行测试用例 ===")
    
    try:
        # 运行pytest测试
        result = subprocess.run(
            ["python", "-m", "pytest"],
            check=True,
            capture_output=True,
            text=True
        )
        log.info(f"测试运行成功\n输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"测试运行失败\n错误: {e.stderr}")
        return False
    except Exception as e:
        log.error(f"测试运行异常: {str(e)}")
        return False


def generate_allure_report():
    """
    生成Allure报告
    """
    log.info("=== 开始生成Allure报告 ===")
    
    try:
        # 生成Allure报告
        result = subprocess.run(
            ["allure", "generate", config['ALLURE_RESULTS_DIR'], "-o", config['ALLURE_REPORT_DIR'], "--clean"],
            check=True,
            capture_output=True,
            text=True
        )
        log.info(f"Allure报告生成成功\n输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Allure报告生成失败\n错误: {e.stderr}")
        return False
    except FileNotFoundError:
        log.error("未找到allure命令，请确保已安装Allure并添加到系统PATH中")
        return False
    except Exception as e:
        log.error(f"Allure报告生成异常: {str(e)}")
        return False


def send_dingtalk_notification():
    """
    发送钉钉通知
    """
    log.info("=== 开始发送钉钉通知 ===")
    
    try:
        # 运行钉钉通知脚本
        result = subprocess.run(
            ["python", "utils/dingtalk_notifier.py"],
            check=True,
            capture_output=True,
            text=True
        )
        log.info(f"钉钉通知发送成功\n输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"钉钉通知发送失败\n错误: {e.stderr}")
        return False
    except Exception as e:
        log.error(f"钉钉通知发送异常: {str(e)}")
        return False


def main():
    """
    主函数
    """
    log.info("=== 启动定时测试任务 ===")
    
    # 立即运行一次
    log.info("立即运行测试任务")
    run_tests()
    generate_allure_report()
    send_dingtalk_notification()
    
    # 设置定时任务，每小时运行一次
    schedule.every().hour.do(
        lambda: [run_tests(), generate_allure_report(), send_dingtalk_notification()]
    )
    
    # 每天运行一次的配置（注释形式）
    # schedule.every().day.at("09:00").do(
    #     lambda: [run_tests(), generate_allure_report(), send_dingtalk_notification()]
    # )
    
    # 循环执行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    main()
