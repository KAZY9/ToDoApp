from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True) #作成した日付を自動で登録

    #DBの管理パネルで表示される
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["completed"] #completedで並び替えが可能になる