from django.db import models
from django.contrib.auth import get_user_model
from user_auth.models import RoleChoices

User = get_user_model()


class Book(models.Model):
    """
    Model representing books in the library.
    Supports both digital and physical types.
    """
    TYPE_CHOICES = [
        ('digital', 'Digital'),
        ('physical', 'Physical'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    summary = models.TextField()
    is_available = models.BooleanField(default=True)  # Tracks if the book can be borrowed
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': RoleChoices.LIBRARIAN},  # Restrict uploader to librarians
    )
    file_url = models.URLField(
        null=True,
        blank=True,
        help_text="URL for digital book (only for digital type)"
    )  # Optional URL for digital books

    def save(self, *args, **kwargs):
        """
        Ensure that the file_url is required for digital books but not for physical ones.
        """
        if self.type == 'digital' and not self.file_url:
            raise ValueError("Digital books must have a file URL.")
        if self.type == 'physical' and self.file_url:
            raise ValueError("Physical books cannot have a file URL.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

