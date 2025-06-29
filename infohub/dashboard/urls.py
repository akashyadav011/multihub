from django.urls import path
from .views import home, refresh_quote, refresh_joke

urlpatterns = [
    path('', home, name="home"),
    path('refresh-quote/', refresh_quote, name="refresh_quote"),
    path('refresh-joke/', refresh_joke, name="refresh_joke"),
]
