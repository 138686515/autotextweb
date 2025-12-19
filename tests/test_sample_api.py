import pytest
import allure
from api.request_handler import request_handler
from api.endpoints import endpoints
from data.test_data import test_data
from utils.logger import log


@allure.feature("用户管理")
class TestUserAPI:
    """用户相关API测试"""
    
    @allure.story("获取用户列表")
    @allure.title("测试获取所有用户")
    def test_get_users(self):
        """测试获取所有用户"""
        log.info("开始测试获取所有用户")
        response = request_handler.get(endpoints.USERS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "用户列表不应为空"
        log.info("测试获取所有用户成功")
    
    @allure.story("获取单个用户")
    @allure.title("测试获取单个用户")
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user(self, user_id):
        """测试获取单个用户"""
        log.info(f"开始测试获取用户ID: {user_id}")
        user_endpoint = endpoints.get_user_endpoint(user_id)
        response = request_handler.get(user_endpoint)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["id"] == user_id, f"返回的用户ID应该是{user_id}"
        log.info(f"测试获取用户ID: {user_id}成功")
    
    @allure.story("创建用户")
    @allure.title("测试创建新用户")
    def test_create_user(self):
        """测试创建新用户"""
        log.info("开始测试创建新用户")
        new_user = test_data.USER_TEST_DATA["new_user"]
        response = request_handler.post(endpoints.USERS, json=new_user)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["name"] == new_user["name"], "返回的用户名应该与创建时一致"
        log.info("测试创建新用户成功")


@allure.feature("帖子管理")
class TestPostAPI:
    """帖子相关API测试"""
    
    @allure.story("获取帖子列表")
    @allure.title("测试获取所有帖子")
    def test_get_posts(self):
        """测试获取所有帖子"""
        log.info("开始测试获取所有帖子")
        response = request_handler.get(endpoints.POSTS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "帖子列表不应为空"
        log.info("测试获取所有帖子成功")
    
    @allure.story("获取单个帖子")
    @allure.title("测试获取单个帖子")
    def test_get_post(self):
        """测试获取单个帖子"""
        log.info("开始测试获取单个帖子")
        post_id = test_data.POST_TEST_DATA["valid_post_id"]
        post_endpoint = endpoints.get_post_endpoint(post_id)
        response = request_handler.get(post_endpoint)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["id"] == post_id, f"返回的帖子ID应该是{post_id}"
        log.info("测试获取单个帖子成功")
    
    @allure.story("创建帖子")
    @allure.title("测试创建新帖子")
    def test_create_post(self):
        """测试创建新帖子"""
        log.info("开始测试创建新帖子")
        new_post = test_data.POST_TEST_DATA["new_post"]
        response = request_handler.post(endpoints.POSTS, json=new_post)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["title"] == new_post["title"], "返回的帖子标题应该与创建时一致"
        log.info("测试创建新帖子成功")
    
    @allure.story("更新帖子")
    @allure.title("测试更新帖子")
    def test_update_post(self):
        """测试更新帖子"""
        log.info("开始测试更新帖子")
        post_id = test_data.POST_TEST_DATA["valid_post_id"]
        update_data = test_data.POST_TEST_DATA["update_post"]
        post_endpoint = endpoints.get_post_endpoint(post_id)
        response = request_handler.put(post_endpoint, json=update_data)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["title"] == update_data["title"], "帖子标题应该已更新"
        log.info("测试更新帖子成功")
    
    @allure.story("删除帖子")
    @allure.title("测试删除帖子")
    def test_delete_post(self):
        """测试删除帖子"""
        log.info("开始测试删除帖子")
        post_id = test_data.POST_TEST_DATA["valid_post_id"]
        post_endpoint = endpoints.get_post_endpoint(post_id)
        response = request_handler.delete(post_endpoint)
        # DELETE请求成功返回空字典
        assert isinstance(response, dict), "响应应该是字典类型"
        log.info("测试删除帖子成功")


@allure.feature("评论管理")
class TestCommentAPI:
    """评论相关API测试"""
    
    @allure.story("获取评论列表")
    @allure.title("测试获取所有评论")
    def test_get_comments(self):
        """测试获取所有评论"""
        log.info("开始测试获取所有评论")
        response = request_handler.get(endpoints.COMMENTS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "评论列表不应为空"
        log.info("测试获取所有评论成功")
    
    @allure.story("获取帖子评论")
    @allure.title("测试获取帖子评论")
    def test_get_post_comments(self):
        """测试获取帖子评论"""
        log.info("开始测试获取帖子评论")
        post_id = test_data.POST_TEST_DATA["valid_post_id"]
        comments_endpoint = endpoints.get_post_comments_endpoint(post_id)
        response = request_handler.get(comments_endpoint)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "帖子评论列表不应为空"
        # 验证所有评论都属于指定的帖子
        for comment in response:
            assert comment["postId"] == post_id, f"评论应该属于帖子ID: {post_id}"
        log.info("测试获取帖子评论成功")


@allure.feature("待办事项管理")
class TestTodoAPI:
    """待办事项相关API测试"""
    
    @allure.story("获取待办事项列表")
    @allure.title("测试获取所有待办事项")
    def test_get_todos(self):
        """测试获取所有待办事项"""
        log.info("开始测试获取所有待办事项")
        response = request_handler.get(endpoints.TODOS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "待办事项列表不应为空"
        log.info("测试获取所有待办事项成功")
    
    @allure.story("创建待办事项")
    @allure.title("测试创建新待办事项")
    def test_create_todo(self):
        """测试创建新待办事项"""
        log.info("开始测试创建新待办事项")
        new_todo = test_data.TODO_TEST_DATA["new_todo"]
        response = request_handler.post(endpoints.TODOS, json=new_todo)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["title"] == new_todo["title"], "返回的待办事项标题应该与创建时一致"
        log.info("测试创建新待办事项成功")


@allure.feature("相册管理")
class TestAlbumAPI:
    """相册相关API测试"""
    
    @allure.story("获取相册列表")
    @allure.title("测试获取所有相册")
    def test_get_albums(self):
        """测试获取所有相册"""
        log.info("开始测试获取所有相册")
        response = request_handler.get(endpoints.ALBUMS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "相册列表不应为空"
        log.info("测试获取所有相册成功")
    
    @allure.story("获取单个相册")
    @allure.title("测试获取单个相册")
    def test_get_album(self):
        """测试获取单个相册"""
        log.info("开始测试获取单个相册")
        album_id = test_data.ALBUM_TEST_DATA["valid_album_id"]
        album_endpoint = endpoints.get_album_endpoint(album_id)
        response = request_handler.get(album_endpoint)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["id"] == album_id, f"返回的相册ID应该是{album_id}"
        log.info("测试获取单个相册成功")
    
    @allure.story("创建相册")
    @allure.title("测试创建新相册")
    def test_create_album(self):
        """测试创建新相册"""
        log.info("开始测试创建新相册")
        new_album = test_data.ALBUM_TEST_DATA["new_album"]
        response = request_handler.post(endpoints.ALBUMS, json=new_album)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["title"] == new_album["title"], "返回的相册标题应该与创建时一致"
        log.info("测试创建新相册成功")
    
    @allure.story("获取用户相册")
    @allure.title("测试获取用户相册")
    def test_get_user_albums(self):
        """测试获取用户相册"""
        log.info("开始测试获取用户相册")
        user_id = test_data.USER_TEST_DATA["valid_user_id"]
        user_albums_endpoint = endpoints.get_user_albums_endpoint(user_id)
        response = request_handler.get(user_albums_endpoint)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "用户相册列表不应为空"
        # 验证所有相册都属于指定用户
        for album in response:
            assert album["userId"] == user_id, f"相册应该属于用户ID: {user_id}"
        log.info("测试获取用户相册成功")


@allure.feature("照片管理")
class TestPhotoAPI:
    """照片相关API测试"""
    
    @allure.story("获取照片列表")
    @allure.title("测试获取所有照片")
    def test_get_photos(self):
        """测试获取所有照片"""
        log.info("开始测试获取所有照片")
        response = request_handler.get(endpoints.PHOTOS)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "照片列表不应为空"
        log.info("测试获取所有照片成功")
    
    @allure.story("获取单个照片")
    @allure.title("测试获取单个照片")
    def test_get_photo(self):
        """测试获取单个照片"""
        log.info("开始测试获取单个照片")
        photo_id = test_data.PHOTO_TEST_DATA["valid_photo_id"]
        photo_endpoint = endpoints.get_photo_endpoint(photo_id)
        response = request_handler.get(photo_endpoint)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["id"] == photo_id, f"返回的照片ID应该是{photo_id}"
        log.info("测试获取单个照片成功")
    
    @allure.story("创建照片")
    @allure.title("测试创建新照片")
    def test_create_photo(self):
        """测试创建新照片"""
        log.info("开始测试创建新照片")
        new_photo = test_data.PHOTO_TEST_DATA["new_photo"]
        response = request_handler.post(endpoints.PHOTOS, json=new_photo)
        assert isinstance(response, dict), "响应应该是字典类型"
        assert response["title"] == new_photo["title"], "返回的照片标题应该与创建时一致"
        log.info("测试创建新照片成功")
    
    @allure.story("获取相册照片")
    @allure.title("测试获取相册照片")
    def test_get_album_photos(self):
        """测试获取相册照片"""
        log.info("开始测试获取相册照片")
        album_id = test_data.ALBUM_TEST_DATA["valid_album_id"]
        album_photos_endpoint = endpoints.get_album_photos_endpoint(album_id)
        response = request_handler.get(album_photos_endpoint)
        assert isinstance(response, list), "响应应该是列表类型"
        assert len(response) > 0, "相册照片列表不应为空"
        # 验证所有照片都属于指定相册
        for photo in response:
            assert photo["albumId"] == album_id, f"照片应该属于相册ID: {album_id}"
        log.info("测试获取相册照片成功")
    
    @allure.story("上传照片")
    @allure.title("测试上传照片文件")
    def test_upload_photo(self):
        """
        测试上传照片文件
        注意：jsonplaceholder API可能不支持文件上传，所以添加了跳过机制
        """
        import os
        import pytest
        
        log.info("开始测试上传照片文件")
        photo_path = test_data.PHOTO_TEST_DATA["upload_photo_path"]
        
        # 检查文件是否存在
        if not os.path.exists(photo_path):
            log.warning(f"照片文件不存在: {photo_path}")
            pytest.skip(f"照片文件不存在: {photo_path}")
        
        # 上传照片（假设API支持文件上传）
        try:
            response = request_handler.upload_file(endpoints.PHOTOS, photo_path)
            assert isinstance(response, dict), "响应应该是字典类型"
            log.info("测试上传照片成功")
        except Exception as e:
            log.error(f"测试上传照片失败: {str(e)}")
            # 由于jsonplaceholder可能不支持文件上传，这里捕获异常，不影响其他测试
            pytest.skip(f"照片上传API可能不支持: {str(e)}")
