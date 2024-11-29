
from datetime import date, timedelta
from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book

User = get_user_model()

class Loan(models.Model):
    """
    Loan model to track borrowed resources.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    @staticmethod
    def can_borrow(book, user):
        """
        Check if the book is available and if the user can borrow.
        """
        # Check if the book is already loaned out
        if not book.is_available:
            return False, "This resource is already loaned out."

        # Check for overdue loans
        overdue_loans = Loan.objects.filter(user=user, returned=False, due_date__lt=date.today())
        if overdue_loans.exists():
            return False, "You have overdue loans. Please return them to borrow again."

        return True, "You can borrow this resource."

    def save(self, *args, **kwargs):
        """
        Override save to mark the book as unavailable when borrowed.
        """
        if not self.returned:
            self.book.is_available = False
            self.book.save()
        super().save(*args, **kwargs)

    def mark_as_returned(self):
        """
        Mark the loan as returned and make the book available again.
        """
        self.returned = True
        self.book.is_available = True
        self.book.save()
        self.save()

