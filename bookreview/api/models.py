from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255,default='')
    publication_dt = models.CharField(max_length=255,default='')
    url = models.URLField()
    description = models.TextField()
    # Add any other fields you want to store


class BookList(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    book_image = models.URLField()
    description = models.TextField()
    publisher = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    comment= ArrayField(models.CharField(max_length=200), blank=True, null=True)



class BookComment(models.Model):
    book = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Rating(models.Model):
    book = models.ForeignKey(BookList, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.rating} - {self.book.title}"