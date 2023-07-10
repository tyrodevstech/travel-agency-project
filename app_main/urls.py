from django.urls import path
from app_main.views import *

app_name = "app_main"


urlpatterns = [
    path("", index_view, name="home"),
    path("search/", search_view, name="search"),
    path("order-list/", dashboard_view, name="order-list"),
    path("update-profile/", update_profile_view, name="update-profile"),
    path("change-password/", change_password_view, name="change-password"),

    path("signin/", signin_view, name="signin"),
    path("signout/", signout_view, name="signout"),
    path("signup/", signup_view, name="signup"),
]


# htmx_urlpatters = [

# ]
# urlpatterns += htmx_urlpatters
