from django.contrib import admin
from .models import UserProfile, StartupProfile, InvestorProfile, Post, ForumCategory, ForumTopic, ForumReply, Mentor

# Register models for admin interface
admin.site.register(UserProfile)
admin.site.register(StartupProfile)
admin.site.register(InvestorProfile)
admin.site.register(Post)
admin.site.register(ForumCategory)
admin.site.register(ForumTopic)
admin.site.register(ForumReply)
admin.site.register(Mentor)
