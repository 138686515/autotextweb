from typing import List, Dict, Any


class TestData:
    """测试数据管理类"""
    
    # 用户相关测试数据
    USER_TEST_DATA = {
        "valid_user_id": 1,
        "invalid_user_id": 999,
        "new_user": {
            "name": "John Doe",
            "username": "johndoe",
            "email": "john.doe@example.com",
            "address": {
                "street": "123 Main St",
                "suite": "Apt 4B",
                "city": "New York",
                "zipcode": "10001",
                "geo": {
                    "lat": "40.7128",
                    "lng": "-74.0060"
                }
            },
            "phone": "123-456-7890",
            "website": "johndoe.com",
            "company": {
                "name": "Example Company",
                "catchPhrase": "Innovation at its finest",
                "bs": "technology development"
            }
        }
    }
    
    # 帖子相关测试数据
    POST_TEST_DATA = {
        "valid_post_id": 1,
        "invalid_post_id": 999,
        "new_post": {
            "title": "Test Post",
            "body": "This is a test post content.",
            "userId": 1
        },
        "update_post": {
            "title": "Updated Test Post",
            "body": "This is an updated test post content.",
            "userId": 1
        }
    }
    
    # 评论相关测试数据
    COMMENT_TEST_DATA = {
        "valid_comment_id": 1,
        "invalid_comment_id": 999,
        "new_comment": {
            "postId": 1,
            "name": "Test Comment",
            "email": "test@example.com",
            "body": "This is a test comment.",
        }
    }
    
    # 待办事项相关测试数据
    TODO_TEST_DATA = {
        "valid_todo_id": 1,
        "invalid_todo_id": 999,
        "new_todo": {
            "userId": 1,
            "title": "Test Todo",
            "completed": False
        }
    }
    
    # 相册相关测试数据
    ALBUM_TEST_DATA = {
        "valid_album_id": 1,
        "invalid_album_id": 999,
        "new_album": {
            "title": "Test Album",
            "userId": 1
        }
    }
    
    # 照片相关测试数据
    PHOTO_TEST_DATA = {
        "valid_photo_id": 1,
        "invalid_photo_id": 999,
        "new_photo": {
            "albumId": 1,
            "title": "Test Photo",
            "url": "https://example.com/photo.jpg",
            "thumbnailUrl": "https://example.com/thumbnail.jpg"
        },
        "upload_photo_path": "photo\1寸蓝底 - 副本.png"  # 用户提供的照片文件路径
    }
    
    # 参数化测试数据
    @classmethod
    def get_user_id_params(cls) -> List[Dict[str, Any]]:
        """获取用户ID参数化测试数据"""
        return [
            {"user_id": 1, "expected_status": 200},
            {"user_id": 2, "expected_status": 200},
            {"user_id": 3, "expected_status": 200},
        ]
    
    @classmethod
    def get_post_id_params(cls) -> List[Dict[str, Any]]:
        """获取帖子ID参数化测试数据"""
        return [
            {"post_id": 1, "expected_status": 200},
            {"post_id": 2, "expected_status": 200},
            {"post_id": 3, "expected_status": 200},
        ]
    
    @classmethod
    def get_invalid_id_params(cls) -> List[Dict[str, Any]]:
        """获取无效ID参数化测试数据"""
        return [
            {"invalid_id": 999, "endpoint": "/users/{}", "expected_status": 404},
            {"invalid_id": 999, "endpoint": "/posts/{}", "expected_status": 404},
            {"invalid_id": 999, "endpoint": "/comments/{}", "expected_status": 404},
        ]


# 导出TestData实例供其他模块使用
test_data = TestData()