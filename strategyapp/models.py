from django.db import models
from accounts.models import CustomUser

class StrategyPost(models.Model):

    user = models.ForeignKey(
        CustomUser,

        verbose_name='ユーザー',

        on_delete=models.CASCADE
        )

    title = models.CharField(
        verbose_name ='タイトル',
        max_length=200
        )
    
    comment = models.TextField(
        verbose_name='コメント',
        )
    
    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to = 'images',
        )
    
    image2 = models.ImageField(
        verbose_name='イメージ2',
        upload_to = 'images',
        blank=True,
        null=True
        )


    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
        )
    
    def __str__(self):
        return self.title
    
class Tweet(models.Model):
    user  = models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        on_delete=models.CASCADE
    )
    content = models.TextField(
        verbose_name="ツイート内容",
        max_length=280
    )
    created_at = models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True
    )

    def __str__(self):
        return self.content[:50]