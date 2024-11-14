from django.urls import path
from . import views

app_name = 'strategyapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('post/', views.CreateStrategyView.as_view(), name='post'),

    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),

    path('strategy-detail/<int:pk>',
         views.StrategyDetailView.as_view(),
         name = 'strategy_detail'
         ),

     path('tweets/', views.TweetListView.as_view(), name='tweets_list'), 
     path('tweet/new/', views.TweetCreateView.as_view(), name='tweet_create'),

     path(
         'contact/',
         views.ContactView.as_view(),
         name='contact'
     )
]