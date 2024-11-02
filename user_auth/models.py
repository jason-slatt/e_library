from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    LIBRARIAN = 'librarian', 'Librarian'
    USER = 'user', 'User'

    def __str__(self) -> Any:
        return super().__str__()

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.role}"  # Return the user's email and role

    
 

    def is_admin(self):
        return self.role == RoleChoices.ADMIN

    def is_librarian(self):
        return self.role == RoleChoices.LIBRARIAN

    def is_user(self):
        return self.role == RoleChoices.USER
