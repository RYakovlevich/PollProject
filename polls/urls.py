from django.urls import path
from polls import views as polls_views
from . import views

app_name = 'polls'
urlpatterns = [
    path('', polls_views.HomeView.as_view(), name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('profile/<int:user_id>', polls_views.profile, name='profile')
]
