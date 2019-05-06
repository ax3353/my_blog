from PIL import Image
from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager


class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    title = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    """
    博客文章数据模型
    """

    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)
    # 文章正文。注意为MDTextField()
    body = MDTextField()
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')
    # 文章标签
    tags = TaggableManager(blank=True)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d', blank=True)

    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # 将文章标题返回
        return self.title

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
