from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

# Create your views here.


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "registration/register.html", context={"form": form})


def password_reset_request(request):
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get("email")
        query = User.objects.filter(email=email)
        if query.exists():
            associated_user = query.first()
            subject = ("Password Reset Requested",)
            email_template = "registration/password_reset_email.txt"
            email_context = {
                "email": associated_user.email,
                "domain": "localhost:8000",
                "site_name": "Veannes",
                "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                "user": associated_user,
                "token": default_token_generator.make_token(associated_user),
                "protocol": "http",
            }

            email = render_to_string(email_template, email_context)
            try:
                send_mail(
                    subject,
                    email,
                    'webdspam@gmail.com',
                    [associated_user.email],
                    fail_silently=False
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found')

            return redirect('password-reset-done')
    
    return render(request, 'registration/password_reset.html', context={'form': form})
