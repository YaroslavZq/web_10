from django.db import models

# Create your models here.


class Tag(models.Model):
	name = models.CharField(max_length=75, null=False, unique=True)

	def __str__(self):
		return f"{self.name}"


class Author(models.Model):
	fullname = models.CharField(max_length=50, null=False, unique=True)
	born = models.CharField(max_length=100, default="born")
	description = models.CharField(max_length=5000, default="description")

	def __str__(self):
		return f"{self.fullname}"


class Quote(models.Model):
	text = models.CharField(max_length=1500, null=False, unique=True)
	tags = models.ManyToManyField(Tag)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return f"{self.text}"
