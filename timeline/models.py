from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# class Post(models.Model):
#     content = models.TextField(max_length=150)
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.author.username}:{self.content[:20]}"

#     @property
#     def number_of_comments(self):
#         return Comment.objects.filter(post_connected=self).count()


# class Comment(models.Model):
#     content = models.TextField(max_length=150)
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.author.username}:post{self.post_connected.id}"

# class PostReaction(models.Model):
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_id = models.TextField(max_length=128)
    name =  models.TextField(max_length=128)
    artist_id =  models.TextField(max_length=128)
    artist_name =  models.TextField(max_length=128)
    album_id =  models.TextField(max_length=128)
    album_image_url =  models.URLField()
    album_name =  models.TextField(max_length=128)
    popularity = models.IntegerField()
    url = models.URLField()
    preview_url = models.URLField()
    release_date = models.DateField()
    played_at = models.DateTimeField()
    added_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.played_at} {self.user.first_name} {self.artist_name} {self.name}"