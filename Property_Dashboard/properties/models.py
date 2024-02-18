from django.db import models

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    listing_date = models.DateField(auto_now_add=True)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    square_feet = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=2)
    garage = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    year_built = models.IntegerField()
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)  # Requires Pillow library



    def __str__(self):
        return self.title

