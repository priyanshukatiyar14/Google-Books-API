from django.db import models
from user.models import Users
import uuid

class BookRecommendation(models.Model):
	id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	description = models.TextField()
	cover_image = models.URLField(blank=True, null=True)
	publication_date = models.DateField()
	rating = models.FloatField(default=0.0)
	genre = models.CharField(max_length=255)
	submitted_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='submitted_books')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class UserInteraction(models.Model):
	id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(Users, on_delete=models.CASCADE)
	book = models.ForeignKey(BookRecommendation, on_delete=models.CASCADE, related_name='interactions')
	liked = models.BooleanField(default=False)
	comment = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.book.title}"
