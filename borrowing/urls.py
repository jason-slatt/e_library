from django.urls import path
from .views import BorrowBookView, AccessResourceView

urlpatterns = [
    path('loans/borrow/', BorrowBookView.as_view(), name='loan-borrow'),
    path('resources/<int:pk>/access/', AccessResourceView.as_view(), name='resource-access'),
]