from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, StartupProfile, InvestorProfile, Post, ForumTopic, ForumReply

# User registration form with user type selection
class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('startup', 'Startup'),
        ('investor', 'Investor'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

# Startup Profile form
class StartupProfileForm(forms.ModelForm):
    class Meta:
        model = StartupProfile
        fields = ['name', 'industry', 'business_stage', 'revenue_model', 
                 'funding_needs', 'funding_history', 'pitch_deck', 
                 'business_plan', 'is_visible']
        
        widgets = {
            'revenue_model': forms.Textarea(attrs={'rows': 4}),
            'funding_history': forms.Textarea(attrs={'rows': 4}),
        }

# Investor Profile form
class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        fields = ['name', 'preferred_industries', 'past_investments', 'investment_preferences']
        
        widgets = {
            'past_investments': forms.Textarea(attrs={'rows': 4}),
            'investment_preferences': forms.Textarea(attrs={'rows': 4}),
        }

# Community Post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

# Forum Topic form
class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['category', 'title', 'content']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

# Forum Reply form
class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
