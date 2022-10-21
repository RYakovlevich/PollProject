from django.contrib import admin
from django.urls import path, include

import polls.views

urlpatterns = [
    path('', polls.views.HomeView.as_view(), name='home'),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls)

]

