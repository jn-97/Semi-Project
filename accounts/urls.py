from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('any/', views.any, name='any'),
]
