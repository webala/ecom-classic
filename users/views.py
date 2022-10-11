from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    
    return render(request, 'registration/register.html', context={'form': form})