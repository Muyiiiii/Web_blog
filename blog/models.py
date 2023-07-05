from django.db import models
from django.utils import timezone


# Create your models here.
class Moment(models.Model):
    pic = models.FileField(upload_to='pic/', verbose_name='图片')
    date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='标题')
    content = models.CharField(max_length=10000, null=False, blank=False, default='无内容', verbose_name='内容')
    author_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='作者')
    email = models.CharField(max_length=100, null=False, blank=False, verbose_name='邮箱')
    kind = models.CharField(max_length=100, null=False, blank=False, verbose_name='类别')
    is_valid = models.BooleanField(verbose_name='内容是否合法', default=False)
    dianzan_count = models.IntegerField(default=0, verbose_name='点赞数')

    def __str__(self):
        return self.title

    # 重定向表的名称
    class Meta:
        db_table = 'Moment'
        verbose_name = '帖子库'  # 别名
        verbose_name_plural = verbose_name


class Contact(models.Model):
    real_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='真实姓名')
    date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    user_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='用户名')
    email = models.CharField(max_length=100, null=False, blank=False, verbose_name='邮箱')
    phone_number = models.CharField(max_length=100, null=False, blank=False, verbose_name='手机号')
    subject = models.CharField(max_length=100, null=False, blank=False, verbose_name='主题')
    content = models.CharField(max_length=10000, null=False, blank=False, default='无内容', verbose_name='内容')

    def __str__(self):
        return self.user_name

    # 重定向表的名称
    class Meta:
        db_table = 'Contact'
        verbose_name = '联系信息表'  # 别名
        verbose_name_plural = verbose_name


class User(models.Model):
    profile = models.FileField(upload_to='pic/', default='pic/1.png', verbose_name='头像')
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='用户名')
    pwd = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False, verbose_name='邮箱')
    if_login = models.BooleanField(verbose_name='是否在线', default=False)
    if_tourist = models.BooleanField(verbose_name='是否是游客', default=True)

    def __str__(self):
        return self.name

    # 重定向表的名称
    class Meta:
        db_table = 'User'
        verbose_name = '用户表'  # 别名
        verbose_name_plural = verbose_name


class Comment(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    moment_id = models.IntegerField(default=0, verbose_name='所属帖子')
    content = models.CharField(max_length=10000, null=False, blank=False, default='无评论', verbose_name='评论内容')
    author_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='发布者')

    def __str__(self):
        return self.author_name

    # 重定向表的名称
    class Meta:
        db_table = 'Comment'
        verbose_name = '评论库'  # 别名
        verbose_name_plural = verbose_name


class Video(models.Model):
    video_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='视频名称')
    video_file = models.FileField(upload_to='videos/', verbose_name='视频路径')

    def __str__(self):
        return self.video_name

    class Meta:
        db_table = 'Video'
        verbose_name = '视频库'
        verbose_name_plural = verbose_name
