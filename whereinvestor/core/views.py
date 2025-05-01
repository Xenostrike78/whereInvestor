from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import (UserRegistrationForm, StartupProfileForm, InvestorProfileForm, 
                    PostForm, ForumTopicForm, ForumReplyForm)
from .models import (UserProfile, StartupProfile, InvestorProfile, Post, 
                    ForumCategory, ForumTopic, ForumReply, Mentor)

# Landing page view
def landing(request):
    return render(request, 'landing.html')

# User registration view
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            
            # Create user profile
            UserProfile.objects.create(user=user, user_type=user_type)
            
            # Create empty profile based on user type
            if user_type == 'startup':
                StartupProfile.objects.create(user=user, name='')
            else:
                InvestorProfile.objects.create(user=user, name='')
            
            # Log the user in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            messages.success(request, "Registration successful! Please complete your profile.")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

# Dashboard view
@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if user_profile.user_type == 'startup':
            return redirect('dashboard_startup')
        else:
            return redirect('dashboard_investor')
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support.")
        return redirect('landing')

# Startup dashboard view
@login_required
def dashboard_startup(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'startup':
            messages.error(request, "You don't have access to this page.")
            return redirect('dashboard')
        
        startup_profile = StartupProfile.objects.get(user=request.user)
        recent_posts = Post.objects.all().order_by('-created_at')[:5]
        
        context = {
            'user_profile': user_profile,
            'startup_profile': startup_profile,
            'recent_posts': recent_posts,
        }
        return render(request, 'dashboard_startup.html', context)
    except (UserProfile.DoesNotExist, StartupProfile.DoesNotExist):
        messages.error(request, "Profile not found. Please complete your profile.")
        return redirect('profile_startup')

# Investor dashboard view
@login_required
def dashboard_investor(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'investor':
            messages.error(request, "You don't have access to this page.")
            return redirect('dashboard')
        
        investor_profile = InvestorProfile.objects.get(user=request.user)
        recent_posts = Post.objects.all().order_by('-created_at')[:5]
        # Get visible startup profiles
        startups = StartupProfile.objects.filter(is_visible=True)
        
        context = {
            'user_profile': user_profile,
            'investor_profile': investor_profile,
            'recent_posts': recent_posts,
            'startups': startups,
        }
        return render(request, 'dashboard_investor.html', context)
    except (UserProfile.DoesNotExist, InvestorProfile.DoesNotExist):
        messages.error(request, "Profile not found. Please complete your profile.")
        return redirect('profile_investor')

# Startup profile view and edit
@login_required
def profile_startup(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'startup':
            messages.error(request, "You don't have access to this page.")
            return redirect('dashboard')
        
        try:
            startup_profile = StartupProfile.objects.get(user=request.user)
        except StartupProfile.DoesNotExist:
            startup_profile = StartupProfile.objects.create(user=request.user, name='')
        
        if request.method == 'POST':
            form = StartupProfileForm(request.POST, request.FILES, instance=startup_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('dashboard_startup')
        else:
            form = StartupProfileForm(instance=startup_profile)
        
        return render(request, 'profile_startup.html', {'form': form, 'profile': startup_profile})
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('landing')

# Investor profile view and edit
@login_required
def profile_investor(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'investor':
            messages.error(request, "You don't have access to this page.")
            return redirect('dashboard')
        
        try:
            investor_profile = InvestorProfile.objects.get(user=request.user)
        except InvestorProfile.DoesNotExist:
            investor_profile = InvestorProfile.objects.create(user=request.user, name='')
        
        if request.method == 'POST':
            form = InvestorProfileForm(request.POST, instance=investor_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('dashboard_investor')
        else:
            form = InvestorProfileForm(instance=investor_profile)
        
        return render(request, 'profile_investor.html', {'form': form, 'profile': investor_profile})
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('landing')

# Community page view
@login_required
def community(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('community')
    else:
        form = PostForm()
    
    posts_list = Post.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts_list, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'community.html', {'form': form, 'posts': posts})

# Forum page view
@login_required
def forum(request):
    categories = ForumCategory.objects.all()
    
    # Get the most recent topics for each category
    categories_with_topics = []
    for category in categories:
        topics = ForumTopic.objects.filter(category=category).order_by('-created_at')[:5]
        categories_with_topics.append({
            'category': category,
            'topics': topics
        })
    
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, "Topic created successfully!")
            return redirect('forum_detail', topic_id=topic.id)
    else:
        form = ForumTopicForm()
    
    return render(request, 'forum.html', {
        'categories_with_topics': categories_with_topics,
        'form': form
    })

# Forum topic detail view
@login_required
def forum_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    replies = ForumReply.objects.filter(topic=topic).order_by('created_at')
    
    if request.method == 'POST':
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.topic = topic
            reply.save()
            messages.success(request, "Reply posted successfully!")
            return redirect('forum_detail', topic_id=topic.id)
    else:
        form = ForumReplyForm()
    
    return render(request, 'forum_detail.html', {
        'topic': topic,
        'replies': replies,
        'form': form
    })

# Mentor directory view
@login_required
def mentors(request):
    mentor_list = Mentor.objects.all()
    return render(request, 'mentors.html', {'mentors': mentor_list})

# Custom logout view that accepts GET requests
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('landing')
