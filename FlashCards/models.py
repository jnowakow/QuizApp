from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class Card(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marked_as_known = models.BooleanField(default=False)
    front_side_text = models.TextField(max_length=1000, null=True, blank=True)
    front_side_img = models.ImageField(upload_to='flash_cards_images', blank=True)
    back_side_text = models.TextField(max_length=1000, null=True, blank=True)
    back_side_img = models.ImageField(upload_to='flash_cards_images', blank=True)

    def __str__(self):
        return "{} card".format(self.pk)



