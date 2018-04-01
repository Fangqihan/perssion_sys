from django.db import models


class Menu(models.Model):
    """
    菜单表
    """
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey(to="Menu", null=True, blank=True)

    def __str__(self):
        caption_list = [self.caption, ]
        p = self.parent
        while p:
            caption_list.insert(0, self.parent.caption)
            p = p.parent

        return '-'.join(caption_list)


class Permissions(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=255)
    menu = models.OneToOneField(to='Menu', null=True, blank=True)

    def __str__(self):
        return '%s---%s<%s>' % (self.title, self.menu,self.url)


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to='Permissions')

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户信息表
    一个用户可以有多个角色，一个角色也可以对应多个用户
    """
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    role = models.ManyToManyField(to='Role')

    def __str__(self):
        return self.name



