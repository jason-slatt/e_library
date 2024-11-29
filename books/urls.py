from django.urls import path
from . import views

urlpatterns = [     
    path('createBook/', views.CreateBookView.as_view(), name = 'createBook'),
    path('updateBook/', views.UpdateBookView.as_view(), name = 'updateBook'),
    path('books/<int:pk>/delete/', views.DeleteBookView.as_view(), name='deleteBook'),
]