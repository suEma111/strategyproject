from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, FormView
from django.urls import reverse_lazy, reverse
from .forms import StrategyPostForm, TweetForm, ContactForm, ReplyForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # CustomUserモデルをインポート
from .models import StrategyPost, Tweet, Reply
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType

# トップページのビュー
class IndexView(ListView):
    template_name = 'index.html'  # 表示するテンプレート
    queryset = StrategyPost.objects.order_by('-posted_at')  # 投稿日時の降順で攻略情報を取得

# 攻略情報の作成ビュー (ログイン必須)
@method_decorator(login_required, name='dispatch')
class CreateStrategyView(CreateView):
    form_class = StrategyPostForm  # 使用するフォーム
    template_name = "post_strategy.html"  # 表示するテンプレート
    success_url = reverse_lazy('strategyapp:post_done')  # 成功時のリダイレクト先

    # フォームのバリデーションが成功した場合の処理
    def form_valid(self, form):
        postdata = form.save(commit=False)  # フォームのデータを保存前に取得
        postdata.user = CustomUser.objects.get(pk=self.request.user.pk)  # ログイン中のユーザーを設定
        postdata.save()  # データを保存
        return super().form_valid(form)

# 投稿成功ページのビュー
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'  # 表示するテンプレート

# 攻略情報の詳細ビュー
class StrategyDetailView(DetailView):
    model = StrategyPost  # 詳細を表示するモデル
    template_name = 'detail.html'  # 表示するテンプレート

    # コンテキストデータをカスタマイズ
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ContentTypeを使用してリプライを取得
        content_type = ContentType.objects.get_for_model(StrategyPost)
        context['replies'] = Reply.objects.filter(
            content_type=content_type,
            object_id=self.object.id  # 現在の攻略情報のIDに関連するリプライを取得
        ).order_by('-created_at')
        # リプライフォームを追加
        context['reply_form'] = ReplyForm()
        return context

# ツイート一覧表示ビュー
class TweetListView(ListView):
    model = Tweet  # 表示するモデル
    template_name = 'tweets_list.html'  # 表示するテンプレート
    context_object_name = 'tweets'  # コンテキスト名を 'tweets' に設定
    ordering = ['-created_at']  # 作成日時の降順で取得

    # コンテキストデータをカスタマイズ
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 各ツイートに関連するリプライを取得
        for tweet in context['tweets']:
            tweet.replies = Reply.objects.filter(
                content_type=ContentType.objects.get_for_model(Tweet),
                object_id=tweet.id  # 現在のツイートに関連するリプライのみを取得
            ).order_by('-created_at')
        
        context['reply_form'] = ReplyForm()  # リプライフォームを追加
        return context

# ツイート投稿ビュー
class TweetCreateView(CreateView):
    form_class = TweetForm  # 使用するフォーム
    template_name = 'tweet_post.html'  # 表示するテンプレート
    success_url = reverse_lazy('strategyapp:tweets_list')  # 成功時のリダイレクト先

    # フォームのバリデーションが成功した場合の処理
    def form_valid(self, form):
        tweet = form.save(commit=False)  # フォームのデータを保存前に取得
        tweet.user = self.request.user  # ログイン中のユーザーを設定
        tweet.save()  # データを保存
        return super().form_valid(form)

# お問い合わせフォームのビュー
class ContactView(FormView):
    template_name = 'contact.html'  # 表示するテンプレート
    form_class = ContactForm  # 使用するフォーム
    success_url = reverse_lazy('strategyapp:contact')  # 成功時のリダイレクト先

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        
        # メール送信設定
        subject = 'お問い合わせ：{}'.format(title)
        message_body = '送信者名：{0}\nメールアドレス:{1}\nタイトル:{2}\nメッセージ:{3}'.format(name, email, title, message)
        
        from_email = 'rasyleena111@gmail.com'
        to_list = ['rasyleena111@gmail.com']
        
        email_message = EmailMessage(subject=subject, body=message_body, from_email=from_email, to=to_list)
        email_message.send()  # メールを送信
        
        # 成功メッセージを追加
        messages.success(self.request, 'お問い合わせは正常に送信されました')
        
        # メッセージが1回だけ表示されるようにリダイレクト
        return super().form_valid(form)

    # リダイレクト後にメッセージを表示しないように
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# ツイートへのリプライ追加
@login_required
def add_tweet_reply(request, object_id):
    # ツイートモデルのContentTypeを取得
    content_type_model = ContentType.objects.get(model='tweet')
    # 該当ツイートを取得
    content_object = get_object_or_404(Tweet, id=object_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)  # POSTデータからフォームを作成
        if form.is_valid():
            reply = form.save(commit=False)  # フォームのデータを保存前に取得
            reply.user = request.user  # ログイン中のユーザーを設定
            reply.content_type = content_type_model  # ContentTypeを設定
            reply.object_id = content_object.id  # 対象ツイートのIDを設定
            reply.save()  # リプライを保存
            # ツイート一覧ページにリダイレクト
            return redirect('strategyapp:tweets_list')
    else:
        form = ReplyForm()

    # POST以外のリクエストが来た場合は、ツイート一覧に戻る
    return redirect('strategyapp:tweets_list')

# 攻略情報へのリプライ追加
@login_required
def add_strategy_reply(request, object_id):
    # 攻略情報モデルのContentTypeを取得
    content_type_model = ContentType.objects.get(model='strategypost')
    # 該当攻略情報を取得
    content_object = get_object_or_404(StrategyPost, id=object_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)  # POSTデータからフォームを作成
        if form.is_valid():
            reply = form.save(commit=False)  # フォームのデータを保存前に取得
            reply.user = request.user  # ログイン中のユーザーを設定
            reply.content_type = content_type_model  # ContentTypeを設定
            reply.object_id = content_object.id  # 対象攻略情報のIDを設定
            reply.save()  # リプライを保存
            # 攻略情報の詳細ページにリダイレクト
            return redirect('strategyapp:strategy_detail', pk=content_object.id)
    else:
        form = ReplyForm()

    # POST以外のリクエストが来た場合は攻略情報の詳細に戻る
    return redirect('strategyapp:strategy_detail', pk=content_object.id)

    def form_valid(self, form):
        tweet = form.save(commit=False)  # フォームのデータを保存前に取得
        tweet.user = self.request.user  # ログイン中のユーザーを設定
        tweet.save()  # データを保存
        return super().form_valid(form)