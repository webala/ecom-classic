from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    inventory = models.IntegerField()
    image = models.ImageField()
    # is_limited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @property
    def image_url(self):
        return self.image.url

# class Rating(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.IntegerChoices()