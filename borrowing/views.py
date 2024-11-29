# File: book_app/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import BorrowBookSerializer
from user_auth.permissions import IsRegularUser
from rest_framework.exceptions import PermissionDenied
from books.models import Book
from .models import Loan


class BorrowBookView(generics.CreateAPIView):
    """
    View for borrowing books.
    """
    serializer_class = BorrowBookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccessResourceView(generics.APIView):
    """
    View to allow users to download or read resources online.
    """
    permission_classes = [IsRegularUser]

    def get(self, request, pk):
        """
        Check if the user has an active loan for the resource.
        """
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has borrowed the book and not yet returned it
        active_loan = Loan.objects.filter(user=request.user, book=book, returned=False).exists()
        if not active_loan:
            raise PermissionDenied("You do not have access to this resource.")

        return Response({"file_url": book.file_url}, status=status.HTTP_200_OK)