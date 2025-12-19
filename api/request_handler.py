import os
import requests
from typing import Dict, Any, Optional
from config.config import config
from utils.logger import log


class RequestHandler:
    """请求封装类"""
    
    def __init__(self):
        self.base_url = config['BASE_URL']
        self.timeout = config['API_TIMEOUT']
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """设置默认请求头"""
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        # 如果有API_KEY，添加到请求头
        if config.get('API_KEY'):
            self.session.headers.update({
                'Authorization': f'Bearer {config["API_KEY"]}'
            })
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送GET请求
        :param url: 请求URL（相对路径）
        :param params: 查询参数
        :param kwargs: 其他请求参数
        :return: 响应结果
        """
        full_url = f"{self.base_url}{url}"
        log.info(f"发送GET请求: {full_url}, params: {params}")
        
        try:
            response = self.session.get(full_url, params=params, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            result = response.json()
            log.info(f"GET请求成功: {full_url}, 响应: {result}")
            return result
        except requests.exceptions.RequestException as e:
            log.error(f"GET请求失败: {full_url}, 错误: {str(e)}")
            raise
    
    def post(self, url: str, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送POST请求
        :param url: 请求URL（相对路径）
        :param json: JSON请求体
        :param data: 表单数据
        :param kwargs: 其他请求参数
        :return: 响应结果
        """
        full_url = f"{self.base_url}{url}"
        log.info(f"发送POST请求: {full_url}, json: {json}, data: {data}")
        
        try:
            response = self.session.post(full_url, json=json, data=data, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            result = response.json()
            log.info(f"POST请求成功: {full_url}, 响应: {result}")
            return result
        except requests.exceptions.RequestException as e:
            log.error(f"POST请求失败: {full_url}, 错误: {str(e)}")
            raise
    
    def put(self, url: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送PUT请求
        :param url: 请求URL（相对路径）
        :param json: JSON请求体
        :param kwargs: 其他请求参数
        :return: 响应结果
        """
        full_url = f"{self.base_url}{url}"
        log.info(f"发送PUT请求: {full_url}, json: {json}")
        
        try:
            response = self.session.put(full_url, json=json, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            result = response.json()
            log.info(f"PUT请求成功: {full_url}, 响应: {result}")
            return result
        except requests.exceptions.RequestException as e:
            log.error(f"PUT请求失败: {full_url}, 错误: {str(e)}")
            raise
    
    def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """
        发送DELETE请求
        :param url: 请求URL（相对路径）
        :param kwargs: 其他请求参数
        :return: 响应结果
        """
        full_url = f"{self.base_url}{url}"
        log.info(f"发送DELETE请求: {full_url}")
        
        try:
            response = self.session.delete(full_url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            # DELETE请求可能返回空响应
            if response.text:
                result = response.json()
            else:
                result = {}
            log.info(f"DELETE请求成功: {full_url}, 响应: {result}")
            return result
        except requests.exceptions.RequestException as e:
            log.error(f"DELETE请求失败: {full_url}, 错误: {str(e)}")
            raise
    
    def update_headers(self, headers: Dict[str, Any]):
        """
        更新请求头
        :param headers: 要更新的请求头
        """
        self.session.headers.update(headers)
        log.info(f"更新请求头: {headers}")
    
    def close(self):
        """
        关闭会话
        """
        self.session.close()
        log.info("关闭请求会话")
    
    def upload_file(self, url: str, file_path: str, file_name: str = None, **kwargs) -> Dict[str, Any]:
        """
        上传文件
        :param url: 请求URL（相对路径）
        :param file_path: 本地文件路径
        :param file_name: 上传后的文件名（可选）
        :param kwargs: 其他请求参数
        :return: 响应结果
        """
        full_url = f"{self.base_url}{url}"
        
        # 如果没有指定文件名，使用原文件名
        if not file_name:
            file_name = os.path.basename(file_path)
        
        log.info(f"上传文件: {full_url}, 文件路径: {file_path}, 文件名: {file_name}")
        
        try:
            # 读取文件
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}
                
                # 临时移除Content-Type，让requests自动设置
                original_content_type = self.session.headers.pop('Content-Type', None)
                
                response = self.session.post(full_url, files=files, timeout=self.timeout, **kwargs)
                
                # 恢复原Content-Type
                if original_content_type:
                    self.session.headers['Content-Type'] = original_content_type
                
                response.raise_for_status()
                result = response.json()
                log.info(f"文件上传成功: {full_url}, 响应: {result}")
                return result
        except FileNotFoundError:
            log.error(f"文件不存在: {file_path}")
            raise
        except requests.exceptions.RequestException as e:
            log.error(f"文件上传失败: {full_url}, 错误: {str(e)}")
            raise
        except Exception as e:
            log.error(f"文件上传异常: {str(e)}")
            raise


# 导出RequestHandler实例供其他模块使用
request_handler = RequestHandler()
