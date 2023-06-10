from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('question/', views.index, name='question'),
    path('contest/<slug:slug>/', views.contest_detail, name='contest_detail'),
    path('contest/<slug:slug>/vote', views.vote, name='contest_vote'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('accounts/signup/', views.signup, name='account_signup'),
    path('accounts/login/', views.loginView, name='account_login'),
    path('contest/<slug:slug>/contest_register/', views.contest_register, name='contest_register'),
    path('contest/<slug:slug>/contest_update/<int:pk>/', views.contest_update, name='contest_update'),
    path('guest_list/', views.guest_list, name='guest_list'),
    path('guest_list/<slug:slug>/choice_participant/', views.choice, name='choice_participant'),
    path('guest_list/<slug:slug>/choice_participant/vote', views.vote, name='vote'),
    path('contest/<slug:slug>/results/', views.results, name='results'),
]
