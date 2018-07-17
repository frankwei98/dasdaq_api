from django.db import models

# Create your models here.

# CREATE DATABASE IF NOT EXISTS dasdaq DEFAULT CHARACTER SET utf8mb4;


class UserEx(models.Model):
    username = models.CharField(max_length=100)  # 强制用户使用email登录 方便找回密码
    email = models.CharField(max_length=100)
    password_md5 = models.CharField(max_length=100)
    invitation_code = models.CharField(max_length=4)  #
    inviter = models.CharField(max_length=4, default='')  # 邀请者

    avatar_url = models.CharField(max_length=200, default='')
    eos_address = models.CharField(max_length=100, default='')
    eth_address = models.CharField(max_length=100, default='')

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'api'
        db_table = 'user'
        verbose_name_plural = '用户'

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "invitation_code": self.invitation_code,
            "avatar_url": self.avatar_url,
            "inviter": self.inviter,
            "eos_address": self.eos_address,
            "eth_address": self.eth_address
        }
