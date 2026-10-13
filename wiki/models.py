from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
# Create your models here.




class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete= models.CASCADE,
        )
    body = models.TextField()
    comms=models.CharField(max_length=100)
   


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("wiki_detail", kwargs={"pk": self.pk})




   
class Comment(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments')
    author = models.ForeignKey(
        "auth.User",
        on_delete= models.CASCADE,
        )
    body = models.TextField()
    def get_absolute_url(self):
        return reverse('wiki_detail', kwargs={'pk': self.article.pk})
    def __str__(self):
         return f"{self.author}: {self.body}"
    