from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import UserRegistrationForm, UserAdditionForm
from .models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.


def signup(request):
    print('request', request.user)
    # try:
    #     UserProfile.objects.create(user=User.object.create(request.user))

    # except Exception as err1:
    #     print('err_1', err1)

    if request.method == 'POST':
        print("request.post", request.POST)
        try:

            form = UserRegistrationForm(request.POST)
            # profile_form = UserAdditionForm(
            #     request.POST, instance=request.user)
            if form.is_valid():
                # and profile_form.is_valid():
                user = form.save()
                #profile = profile_form.save(commit=False)
                #profile.user = user
                # profile.save()
                return redirect('login')
        except Exception as erss:
            print('erss', erss)
    else:
        form = UserRegistrationForm()
        # profile_form = UserAdditionForm()
    # 'profile_form': profile_form,
    context = {'form': form}

    return render(request, 'registration/signup.html', context)


def signOut(request):
    logout(request)
    return render(request, 'registration/logoutinfo.html')
