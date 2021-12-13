from django.db import models

import requests

class Board(models.Model):
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=5)
    banner = models.ImageField(upload_to=f'boards/banners/', null=True, blank=True)
    # Board flags
    anonymous = models.BooleanField(help_text="Are user names hidden", default=True)
    nsfw = models.BooleanField(help_text="Allow NSFW content", default=False)
    secret = models.BooleanField(help_text="Is board hidden from board list", default=False)
    # Limits
    max_threads = models.IntegerField(default=50)
    max_bumps = models.IntegerField(default=150)
    max_images = models.IntegerField(default=50)
    # Functionality
    # allow - user can upload such content
    # display - such content is displayed
    allow_images = models.BooleanField(default=True)
    display_images = models.BooleanField(default=True)
    allow_links = models.BooleanField(default=True)
    display_links = models.BooleanField(default=True)

    def __str__(self):
        return f'/{self.short}/ - {self.name}'


class Post(models.Model):
    thread = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=f'threads/images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    message = models.CharField(max_length=512)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        data = {
            'thread': self.thread.id,
            'image': 'NOT_IMPLEMENTED',
            'timestamp': str(self.timestamp),
            'message': self.message
        }
        req = requests.post('http://localhost:5000/post/', json=data)

