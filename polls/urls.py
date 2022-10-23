from django.urls import path
from polls import views as polls_views
from . import views

app_name = 'polls'
urlpatterns = [
    path('', polls_views.HomeView.as_view(), name='index'),
    path('<int:test_id>/', views.open_test, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('profile/<int:user_id>', polls_views.Profile, name='profile')
]
