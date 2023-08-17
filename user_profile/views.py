from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Profile

def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get_or_create(user=request.user)[0]

        if request.method == 'POST':
            profile = Profile.objects.get_or_create(user=request.user)[0]
            profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
            profile.user.full_name = request.POST.get('full_name', profile.user.full_name)
            profile.user.nip = request.POST.get('nip', profile.user.nip)
            profile.user.email = request.POST.get('email', profile.user.email)
            password = request.POST.get('password')
            if password:
                profile.user.set_password(password)
            profile.user.save()
            profile.save()

            # Redirect to the profile page
            return redirect(reverse('profile'))
        
        return render(request, 'profile.html', {'profile': profile})
    else:
        # If user is not authenticated, redirect to custom login with the 'next' parameter
        next_url = reverse('profile')
        return redirect(reverse('login') + f'?next={next_url}')