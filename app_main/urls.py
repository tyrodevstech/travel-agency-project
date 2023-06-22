from django.urls import path
from app_main.views import *

app_name = "app_main"


urlpatterns = [
    path("", index_view, name="home"),
]


# htmx_urlpatters = [

# ]


# urlpatterns += htmx_urlpatters
