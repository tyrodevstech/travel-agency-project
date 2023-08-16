from django.shortcuts import render
from app_flight.filters import AirPlaneTicketFilters
from app_flight.models import AirplaneTicket
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from app_flight.filters import AirPlaneTicketFilters
from app_main.forms import CustomUserForm, UserFeedbackForm
from app_main.models import CustomUser

# Create your views here.


def index_view(request):
    context = {
        "filter": AirPlaneTicketFilters(
            request.GET, queryset=AirplaneTicket.objects.all()
        )
    }
    return render(request, "app_main/index.html", context)


def search_view(request):
    return render(request, "app_main/search.html")


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("app_main:home")
    else:
        if request.method == "POST":
            got_username = request.POST.get("email_or_phone")
            password = request.POST.get("password")

            if "@" in got_username:
                userObject = CustomUser.objects.filter(email=got_username).last()
            else:
                userObject = CustomUser.objects.filter(phone=got_username).last()

            if userObject:
                username = userObject.user.username
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("app_main:home")
            else:
                messages.error(
                    request, "Email / Phone or Password didn't match. Please try again!"
                )

    return render(request, "app_main/signin.html")


def signup_view(request):
    form = CustomUserForm()
    userform = UserCreationForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        updated_request = request.POST.copy()
        username = request.POST.get("name")

        updated_request["username"] = username.replace(" ", "_")

        userform = UserCreationForm(updated_request)
        if form.is_valid() and userform.is_valid():
            new_userform = userform.save(commit=False)
            new_userform.email = request.POST.get("email")
            new_userform.save()

            new_form = form.save(commit=False)
            new_form.user = new_userform
            new_form.save()
            messages.success(request, "Account Created successfully !")
            return redirect("app_main:signin")

    context = {"form": form, "userform": userform}
    return render(request, "app_main/signup.html", context)


@login_required(login_url="app_main:signin")
def signout_view(request):
    logout(request)
    return redirect("app_main:signin")


@login_required(login_url="app_main:signin")
def dashboard_view(request):
    messages.info(request, "Welcome to your dashboard!")
    return render(request, "app_main/dashboard/order.html")


@login_required(login_url="app_main:signin")
def update_profile_view(request):
    user = get_object_or_404(User, id=request.user.id)
    customuser = get_object_or_404(CustomUser, user=user)
    form = CustomUserForm(instance=customuser)

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=customuser)
        if form.is_valid():
            username = request.POST.get("name")
            user.username = username.replace(" ", "_")
            user.email = request.POST.get("email")
            user.save()
            form.save()
            messages.success(request, "Your information has been updated!")

            return redirect("app_main:update-profile")

    context = {
        "form": form,
    }
    return render(request, "app_main/dashboard/update_profile.html", context)


@login_required(login_url="app_main:signin")
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("app_main:change-password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "app_main/dashboard/change_password.html", {"form": form})


def user_feedback_view(request):
    form = UserFeedbackForm()
    if request.method == "POST":
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Your feedback has been sent!")
            return redirect("app_main:feedback")

    return render(request, "app_main/feedback.html", {"form": form})

    context = {
        "filter": AirPlaneTicketFilters(
            request.GET, queryset=AirplaneTicket.objects.all()
        )
    }
    return render(request, "app_main/index.html", context)
