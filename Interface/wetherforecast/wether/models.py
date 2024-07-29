from django.db import models

# Create your models here.


class Data(models.Model):

    locations = models.CharField(max_length=50, primary_key=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.locations


class CropType(models.Model):
    CROP_CHOICES = [
        ('paddy', 'Paddy'),
        ('chilli', 'Chilli'),
        ('cotton', 'Cotton'),
        ('corn', 'Corn'),
    ]

    crop_type = models.CharField(
        max_length=50,
        choices=CROP_CHOICES,
        default='paddy'
    )
    time_frame = models.IntegerField()

    def __str__(self):
        return self.crop_type
