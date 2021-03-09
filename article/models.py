from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    file = models.FileField(upload_to='books/pdfs')
    cover = models.FileField(upload_to='books/cover', blank=True, null=True)

    def __str__(self):
        return self.title

    # def delete(self, *args, **kwargs):
    #     self.file.delete()
    #     self.cover.delete()
    #     super().delete(*args, **kwargs)
