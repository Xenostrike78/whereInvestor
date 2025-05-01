from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# User Profile model to extend Django's User model
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('startup', 'Startup'),
        ('investor', 'Investor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

# Startup Profile model
class StartupProfile(models.Model):
    BUSINESS_STAGE_CHOICES = (
        ('idea', 'Idea Phase'),
        ('mvp', 'MVP'),
        ('early', 'Early Traction'),
        ('growth', 'Growth'),
        ('scaling', 'Scaling'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    business_stage = models.CharField(max_length=10, choices=BUSINESS_STAGE_CHOICES)
    revenue_model = models.TextField()
    funding_needs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    funding_history = models.TextField(blank=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    business_plan = models.FileField(upload_to='business_plans/', blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# Investor Profile model
class InvestorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    preferred_industries = models.CharField(max_length=200)
    past_investments = models.TextField(blank=True)
    investment_preferences = models.TextField()
    
    def __str__(self):
        return self.name

# Community Post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

# Forum Category model
class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Forum Categories"
    
    def __str__(self):
        return self.name

# Forum Topic model
class ForumTopic(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum_detail', args=[str(self.id)])

# Forum Reply model
class ForumReply(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Forum Replies"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply by {self.author.username} on {self.topic.title}"

# Mentor model for Mentor Directory
class Mentor(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=200)
    bio = models.TextField()
    contact_email = models.EmailField()
    
    def __str__(self):
        return self.name
