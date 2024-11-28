from django.urls import path
from . import views

# アプリケーション名を指定
app_name = 'strategyapp'

urlpatterns = [
    # トップページ：IndexViewを呼び出す
    path('', views.IndexView.as_view(), name='index'),  # トップページ
    
    # ツイート一覧ページ：TweetListViewを呼び出す
    path('tweets/', views.TweetListView.as_view(), name='tweets_list'),  # ツイート一覧
    
    # ツイートにリプライを追加するページ：add_tweet_replyビューを呼び出す
    path('tweets/<int:object_id>/reply/', views.add_tweet_reply, name='tweet_reply'),  # ツイートのリプライ

    # 攻略情報にリプライを追加するページ：add_strategy_replyビューを呼び出す
    path('strategy/<int:object_id>/reply/', views.add_strategy_reply, name='strategy_reply'),  # 攻略情報のリプライ

    # 攻略情報詳細ページ：StrategyDetailViewを呼び出す
    path('strategy-detail/<int:pk>/', views.StrategyDetailView.as_view(), name='strategy_detail'),  # 攻略情報詳細
    
    # 新しい攻略情報を投稿するページ：CreateStrategyViewを呼び出す
    path('post/', views.CreateStrategyView.as_view(), name='post'),  # 投稿作成

    # 投稿成功ページ：PostSuccessViewを呼び出す
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),  # 投稿成功ページ

    # 新しいツイートを作成するページ：TweetCreateViewを呼び出す
    path('tweet/new/', views.TweetCreateView.as_view(), name='tweet_create'),  # Tweet作成

    # お問い合わせページ：ContactViewを呼び出す
    path('contact/', views.ContactView.as_view(), name='contact'),  # お問い合わせ
]
