from django.db import models
from django.contrib.auth.models import User
from user_app.constant import create_slug
# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=255)
    is_secret = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class FolderData(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    is_secret = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    file_docs = models.FileField(upload_to='FolderData/docs', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slugs = list(FolderData.objects.all().values_list('slug', flat=True))
            self.slug = create_slug(name=self.name, slugs=slugs)
        super(FolderData, self).save(*args, **kwargs)

class FolderDataAccess(models.Model):
    folder_data = models.ForeignKey(FolderData, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name='folderdataaccess_users')


class FriendList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friendlist_friends')

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected','rejected'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendrequest_owner')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_status = models.CharField(max_length=255, choices=STATUS_CHOICES)


class OwnerPin(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=10)


