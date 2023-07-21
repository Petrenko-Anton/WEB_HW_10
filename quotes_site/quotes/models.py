from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        db_table = 'authors'


class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    class Meta:
        db_table = 'tags'


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, db_table='quote_tag_association')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        db_table = 'quotes'
