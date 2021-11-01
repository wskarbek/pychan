from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=30)
    short = models.CharField(max_length=5)
    banner = models.ImageField(upload_to=f'boards/banners/', null=True, blank=True)
    max_threads = models.IntegerField()
    nsfw = models.BooleanField(default=False)

    def __str__(self):
        return f'/{self.short}/ - {self.name}'

class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    thread = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=f'threads/images/', null=True, blank=True)
    timestamp = models.TimeField(auto_now=True, auto_now_add=False)
    message = models.CharField(max_length=512)
