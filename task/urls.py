from django.urls import path
from task import views


urlpatterns = [
    path('task/add/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/list/',views.TskListView.as_view(), name='task-list'),
    path('task/<int:id>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:id>/remove', views.TaskDeleteView.as_view(), name='task-delete'),
    path('index', views.IndexView.as_view(), name='home'),
    path('signup', views.SignUpView.as_view(), name='register'),
    path('', views.SigninView.as_view(), name='signin'),
    path('logout', views.sign_out, name='signout')

]