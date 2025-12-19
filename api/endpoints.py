class Endpoints:
    """API端点管理类"""
    
    # 用户相关端点
    USERS = "/users"
    USER = "/users/{user_id}"
    
    # 帖子相关端点
    POSTS = "/posts"
    POST = "/posts/{post_id}"
    USER_POSTS = "/users/{user_id}/posts"
    
    # 评论相关端点
    COMMENTS = "/comments"
    COMMENT = "/comments/{comment_id}"
    POST_COMMENTS = "/posts/{post_id}/comments"
    
    # 相册相关端点
    ALBUMS = "/albums"
    ALBUM = "/albums/{album_id}"
    USER_ALBUMS = "/users/{user_id}/albums"
    
    # 照片相关端点
    PHOTOS = "/photos"
    PHOTO = "/photos/{photo_id}"
    ALBUM_PHOTOS = "/albums/{album_id}/photos"
    
    # 待办事项相关端点
    TODOS = "/todos"
    TODO = "/todos/{todo_id}"
    USER_TODOS = "/users/{user_id}/todos"
    
    @classmethod
    def get_user_endpoint(cls, user_id: int) -> str:
        """获取单个用户端点"""
        return cls.USER.format(user_id=user_id)
    
    @classmethod
    def get_post_endpoint(cls, post_id: int) -> str:
        """获取单个帖子端点"""
        return cls.POST.format(post_id=post_id)
    
    @classmethod
    def get_user_posts_endpoint(cls, user_id: int) -> str:
        """获取用户帖子端点"""
        return cls.USER_POSTS.format(user_id=user_id)
    
    @classmethod
    def get_comment_endpoint(cls, comment_id: int) -> str:
        """获取单个评论端点"""
        return cls.COMMENT.format(comment_id=comment_id)
    
    @classmethod
    def get_post_comments_endpoint(cls, post_id: int) -> str:
        """获取帖子评论端点"""
        return cls.POST_COMMENTS.format(post_id=post_id)
    
    @classmethod
    def get_album_endpoint(cls, album_id: int) -> str:
        """获取单个相册端点"""
        return cls.ALBUM.format(album_id=album_id)
    
    @classmethod
    def get_user_albums_endpoint(cls, user_id: int) -> str:
        """获取用户相册端点"""
        return cls.USER_ALBUMS.format(user_id=user_id)
    
    @classmethod
    def get_photo_endpoint(cls, photo_id: int) -> str:
        """获取单个照片端点"""
        return cls.PHOTO.format(photo_id=photo_id)
    
    @classmethod
    def get_album_photos_endpoint(cls, album_id: int) -> str:
        """获取相册照片端点"""
        return cls.ALBUM_PHOTOS.format(album_id=album_id)
    
    @classmethod
    def get_todo_endpoint(cls, todo_id: int) -> str:
        """获取单个待办事项端点"""
        return cls.TODO.format(todo_id=todo_id)
    
    @classmethod
    def get_user_todos_endpoint(cls, user_id: int) -> str:
        """获取用户待办事项端点"""
        return cls.USER_TODOS.format(user_id=user_id)


# 导出Endpoints实例供其他模块使用
endpoints = Endpoints()
