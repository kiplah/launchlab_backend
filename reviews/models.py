from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=5)
    text = models.TextField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating}/5)"
