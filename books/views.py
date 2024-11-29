from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CreateBookSerializer, UpdateBookSerializer
from rest_framework import generics, status
from user_auth.permissions import IsLibrarian
from .models import Book


# Create your views here.


class CreateBookView(generics.CreateAPIView):
    serializer_class = CreateBookSerializer
    permission_classes = [IsLibrarian]
    def post(self, request):
        serializer = self.serializer_class(data = request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class UpdateBookView(generics.UpdateAPIView):
    """
    API View for updating books.
    Only librarians can perform this action.
    """
    serializer_class = UpdateBookSerializer  # Specify the serializer for updates
    queryset = Book.objects.all()  # Queryset for retrieving book instances
    permission_classes = [IsLibrarian]  # Use the IsLibrarian permission class

    def put(self, request, *args, **kwargs):
        """
        Handles PUT requests to update book details.
        """
        # Retrieve the book instance by its primary key
        book = self.get_object()

        # Validate the user has the librarian role
        if not request.user.is_librarian():
            raise PermissionDenied({"error": "Only librarians can update book details."})

        # Pass the data to the serializer for validation and updating
        serializer = self.serializer_class(book, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#have to come back on it 
class DeleteBookView(generics.DestroyAPIView):
    """
    View for deleting book resources.
    Only librarians can perform this operation.
    """
    queryset = Book.objects.all()  # Queryset for books
    permission_classes = [IsLibrarian]  # Ensure only librarians can delete books

    def delete(self, request, *args, **kwargs):
        book = self.get_object()  # Fetch the book instance
        book.delete()  # Delete the book
        return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    