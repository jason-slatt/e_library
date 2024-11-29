# from datetime import date, timedelta
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from .models import Book, Loan
# from user_auth.models import UserRole, RoleChoices

# User = get_user_model()

# class BookLoanTests(APITestCase):
#     """
#     Test cases for books, borrowing, and resource access.
#     """

#     def setUp(self):
#         """
#         Setup initial data for testing.
#         """
#         # Create roles
#         self.librarian_role = UserRole.objects.create(RoleChoices.LIBRARIAN)
#         self.user_role = UserRole.objects.create(RoleChoices.USER)

#         # Create a librarian user and assign the librarian role
#         self.librarian = User.objects.create_user(
#             name="librarian_user",
#             password="password123",
#             email="librarian@gmail.com"
#         )
#         self.librarian.role = self.librarian_role  # Assign librarian role
#         self.librarian.save()

#         # Create a regular user and assign the user role
#         self.user = User.objects.create_user(
#             name="regular_user",
#             password="password123",
#             email="user@gmail.com"
#         )
#         self.user.role = self.user_role  # Assign user role
#         self.user.save()

#         # URLs for borrowing and accessing resources
#         self.borrow_url = "/loans/borrow/"
#         self.access_url_template = "/resources/{book_id}/access/"

#     def test_create_digital_book(self):
#         """
#         Test creating a digital book with a valid file URL.
#         """
#         book = Book.objects.create(
#             title="Digital Book",
#             author="Author 1",
#             subject="Subject 1",
#             publication_year=2023,
#             type="digital",
#             summary="This is a digital book.",
#             file_url="http://example.com/digital-book.pdf",
#             uploaded_by=self.librarian
#         )
#         self.assertEqual(book.type, "digital")
#         self.assertEqual(book.file_url, "http://example.com/digital-book.pdf")

#     def test_create_physical_book_without_file_url(self):
#         """
#         Test creating a physical book without a file URL.
#         """
#         book = Book.objects.create(
#             title="Physical Book",
#             author="Author 2",
#             subject="Subject 2",
#             publication_year=2022,
#             type="physical",
#             summary="This is a physical book.",
#             uploaded_by=self.librarian
#         )
#         self.assertEqual(book.type, "physical")
#         self.assertIsNone(book.file_url)

#     def test_cannot_create_digital_book_without_file_url(self):
#         """
#         Test that creating a digital book without a file URL raises an error.
#         """
#         with self.assertRaises(ValueError):
#             Book.objects.create(
#                 title="Invalid Digital Book",
#                 author="Author 3",
#                 subject="Subject 3",
#                 publication_year=2023,
#                 type="digital",
#                 summary="This book lacks a file URL.",
#                 uploaded_by=self.librarian
#             )

#     def test_cannot_create_physical_book_with_file_url(self):
#         """
#         Test that creating a physical book with a file URL raises an error.
#         """
#         with self.assertRaises(ValueError):
#             Book.objects.create(
#                 title="Invalid Physical Book",
#                 author="Author 4",
#                 subject="Subject 4",
#                 publication_year=2021,
#                 type="physical",
#                 summary="This book should not have a file URL.",
#                 file_url="http://example.com/physical-book.pdf",
#                 uploaded_by=self.librarian
#             )

#     def test_regular_user_cannot_upload_books(self):
#         """
#         Test that regular users cannot upload books.
#         """
#         with self.assertRaises(ValueError):
#             Book.objects.create(
#                 title="Regular User's Book",
#                 author="Author 5",
#                 subject="Subject 5",
#                 publication_year=2024,
#                 type="digital",
#                 summary="This book was uploaded by a regular user.",
#                 file_url="http://example.com/regular-book.pdf",
#                 uploaded_by=self.user
#             )

#     def test_borrow_available_book(self):
#         """
#         Test borrowing an available book.
#         """
#         book = Book.objects.create(
#             title="Available Book",
#             author="Author 6",
#             subject="Subject 6",
#             publication_year=2020,
#             type="physical",
#             summary="This book is available.",
#             uploaded_by=self.librarian
#         )

#         self.client.login(username="regular_user", password="password123")
#         response = self.client.post(self.borrow_url, {"book": book.id})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         book.refresh_from_db()
#         self.assertFalse(book.is_available)

#     def test_cannot_borrow_unavailable_book(self):
#         """
#         Test that a user cannot borrow a book that is already loaned out.
#         """
#         book = Book.objects.create(
#             title="Unavailable Book",
#             author="Author 7",
#             subject="Subject 7",
#             publication_year=2019,
#             type="physical",
#             summary="This book is unavailable.",
#             is_available=False,  # Set as unavailable
#             uploaded_by=self.librarian
#         )

#         self.client.login(username="regular_user", password="password123")
#         response = self.client.post(self.borrow_url, {"book": book.id})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_access_digital_resource_with_active_loan(self):
#         """
#         Test accessing a digital resource with an active loan.
#         """
#         book = Book.objects.create(
#             title="Digital Resource",
#             author="Author 8",
#             subject="Subject 8",
#             publication_year=2021,
#             type="digital",
#             summary="This is a digital resource.",
#             file_url="http://example.com/digital-resource.pdf",
#             uploaded_by=self.librarian
#         )

#         # Create a loan
#         Loan.objects.create(
#             user=self.user,
#             book=book,
#             borrowed_date=date.today(),
#             due_date=date.today() + timedelta(days=14),
#             returned=False
#         )

#         self.client.login(username="regular_user", password="password123")
#         response = self.client.get(self.access_url_template.format(book_id=book.id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("file_url", response.data)
#         self.assertEqual(response.data["file_url"], book.file_url)

#     def test_cannot_access_resource_without_active_loan(self):
#         """
#         Test that a user cannot access a resource without an active loan.
#         """
#         book = Book.objects.create(
#             title="Restricted Resource",
#             author="Author 9",
#             subject="Subject 9",
#             publication_year=2022,
#             type="digital",
#             summary="This resource is restricted.",
#             file_url="http://example.com/restricted-resource.pdf",
#             uploaded_by=self.librarian
#         )

#         self.client.login(username="regular_user", password="password123")
#         response = self.client.get(self.access_url_template.format(book_id=book.id))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
