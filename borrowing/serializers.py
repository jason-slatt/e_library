
from datetime import date, timedelta
from rest_framework import serializers
from .models import Loan

class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrowed_date', 'due_date', 'returned']

    def validate(self, data):
        user = self.context['request'].user
        book = data['book']

        # Check borrowing eligibility
        can_borrow, message = Loan.can_borrow(book, user)
        if not can_borrow:
            raise serializers.ValidationError({"error": message})

        # Default due date to 14 days if not provided
        if 'due_date' not in data:
            data['due_date'] = date.today() + timedelta(days=14)

        return data

    def create(self, validated_data):
        # Create loan and set book as unavailable
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
