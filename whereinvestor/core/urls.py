from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.landing, name='landing'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/startup/', views.dashboard_startup, name='dashboard_startup'),
    path('dashboard/investor/', views.dashboard_investor, name='dashboard_investor'),
    
    # Profiles
    path('profile/startup/', views.profile_startup, name='profile_startup'),
    path('profile/investor/', views.profile_investor, name='profile_investor'),
    
    # Community
    path('community/', views.community, name='community'),
    
    # Forum
    path('forum/', views.forum, name='forum'),
    path('forum/topic/<int:topic_id>/', views.forum_detail, name='forum_detail'),
    
    # Mentors
    path('mentors/', views.mentors, name='mentors'),
]
