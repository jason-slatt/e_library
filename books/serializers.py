from rest_framework import serializers
from .models import Book

class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'subject', 'publication_year', 'type', 'summary', 'is_available']

    def create(self, validated_data):
        # Include the user who uploads the book
        request = self.context.get('request')  # Retrieve request from the context
        user = request.user if request else None

        if not user or not user.user.is_librarian():
            raise serializers.ValidationError({"error": "Only librarians can upload books."})

        # Create the Book instance
        book = Book(
            title=validated_data['title'],
            author=validated_data['author'],
            subject=validated_data['subject'],
            publication_year=validated_data['publication_year'],
            type=validated_data['type'],
            summary=validated_data['summary'],
            uploaded_by=user,
            is_available=validated_data.get('is_available', True)
        )
        book.save()
        return book


class UpdateBookSerializer(serializers.ModelSerializer):
    """
    Serializer for updating books.
    Restricts certain fields from being updated.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'subject', 'publication_year', 'summary', 'is_available']  # Updatable fields

    def update(self, instance, validated_data):
        # Retrieve the request from context
        request = self.context.get('request')
        user = request.user if request else None

        # Check if the user is a librarian
        if not user or not user.is_librarian():
            raise serializers.ValidationError({"error": "Only librarians can update books."})

        # Update the fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

