from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile
from .forms import UpdateProfileForm



@login_required
def dashbo(request):
    return render(request,'dashboard.html')
def homePage(request):
    return render(request,'home.html')

@login_required
def profile(request,pk):
    user = User.objects.get(id=pk)

    userDetails = Profile.objects.all()
    context={'user':user}
    return render(request,'profile.html',context)
@login_required
def update(request):
    
    try:
      profile = request.user.profile
    except Profile.DoesNotExist:
      profile = Profile.objects.create(user=request.user)
    if request.method == 'POST':
        
            

            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,'PROFILE UPDATED SUCCESSFULLY')
                user=request.user
                return redirect('users-profile',pk=user.id)
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)
    context={'profile_form':profile_form}
    return render(request,'update_profile.html',context)