from django.db import models


# Create your models here.
class NewsletterSubscriber(models.Model):
    email = models.EmailField(default='')

    def __str__(self):
        return self.email