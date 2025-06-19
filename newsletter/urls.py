from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.comment_board, name='comment_board'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]
