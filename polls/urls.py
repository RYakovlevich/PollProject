from django.urls import path
from polls import views as polls_views
from . import views

app_name = 'polls'
urlpatterns = [
    path('', polls_views.HomeView.as_view(), name='index'),
    path('<int:test_id>/', views.open_test, name='first'),
    path('<int:test_id>/<int:queue>', views.next_question, name='detail'),
    path('<int:test_id>/<int:queue>/results/', views.next_question, name='results'),
    path('<int:test_id>/<int:queue>/vote/', views.vote, name='vote'),
]
