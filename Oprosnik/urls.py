from django.urls import path, include
from django.contrib import admin
from polls.views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', include('registration.urls')),
    path('captcha/', include('captcha.urls'))

]

