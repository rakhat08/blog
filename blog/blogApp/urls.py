from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('my_articles/', views.my_article_list, name='my_article_list'),
    path('', views.all_articles, name='all_articles'),
    path('full_article/<int:pk>', views.full_article, name='full_article'),
    path('create_article/', views.create_article, name='create_article'),
    path('edit_article/<int:pk>', views.edit_article, name='edit_article'),
    path('delete_article/<int:pk>', views.delete_article, name='delete_article'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('login/', LoginView.as_view(template_name='login.html', next_page = 'my_article_list'), name='login')
]