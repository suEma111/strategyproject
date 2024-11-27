from django.urls import path
from . import views

app_name = 'strategyapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # トップページ

    path('tweets/', views.TweetListView.as_view(), name='tweets_list'),  # ツイート一覧
    
    path('tweets/<int:object_id>/reply/', views.add_tweet_reply, name='tweet_reply'),  # ツイートのリプライ

    path('strategy/<int:object_id>/reply/', views.add_strategy_reply, name='strategy_reply'),  # 攻略情報のリプライ

    path('strategy-detail/<int:pk>/', views.StrategyDetailView.as_view(), name='strategy_detail'),  # 攻略情報詳細
    

    # 投稿作成
    path('post/', views.CreateStrategyView.as_view(), name='post'),

    # 投稿成功ページ
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),

    # Tweet作成
    path('tweet/new/', views.TweetCreateView.as_view(), name='tweet_create'),

    # お問い合わせ
    path('contact/', views.ContactView.as_view(), name='contact'),
]
