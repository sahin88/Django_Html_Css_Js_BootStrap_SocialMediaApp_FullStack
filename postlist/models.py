from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class postList(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='post_list/images', blank=True, null=True)
    video = models.FileField(
        upload_to='post_list/videos', blank=True, null=True)
    likes = models.ManyToManyField(
        User, related_name='likes', blank=True, default=None)
    video_link = models.URLField(max_length=2000, blank='True')
    caption = RichTextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    #slug= models.SlugField(unique=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ('-created_date', )

    def get_absolute_url(self, *args, **kwargs):
        return reverse('detail', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        super(postList, self).delete(*args, **kwargs)


STATUS_LIKES = (('Like', 'Like'),
                ('Unlike', 'Unlike'))


class comments(models.Model):

    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_id = models.ForeignKey(postList, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_date', )


# class Like(models.Model):
#     user_likes = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(postList, on_delete=models.CASCADE)
#     value = models.CharField(choices=STATUS_LIKES,
#                              default='Like', max_length=10)

#     def __str__(self):
#         return str(self.post)
