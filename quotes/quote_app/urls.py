from django.urls import path
from . import views

app_name = 'quote_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_quote/', views.quote, name='add_quote'),
    path('add_tag/', views.tag, name='add_tag'),
    path('add_author/', views.author, name='add_author'),
    path('detail/<int:author_id>', views.detail, name='detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
]