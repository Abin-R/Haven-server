from django.db import models
from django.core.validators import FileExtensionValidator
from events.models import *

# Create your models here.
class EventPosting(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    description = models.TextField()
    completionStatus = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} - {self.description}"
    

class Image(models.Model):
    image = models.ImageField(upload_to='event_images/')
    
    def __str__(self):
        return f"Image {self.id}"


class EventReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Image, related_name='event_reviews')


    def __str__(self):
        return f"{self.user.username} - {self.event}"