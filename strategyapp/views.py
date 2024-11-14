from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, FormView
from django.urls import reverse_lazy
from .forms import StrategyPostForm, TweetForm, ContactForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # CustomUser をインポート
from .models import StrategyPost, Tweet
from django.contrib import messages
from django.core.mail import EmailMessage

class IndexView(ListView):
    template_name = 'index.html'
    queryset = StrategyPost.objects.order_by('-posted_at')

@method_decorator(login_required, name='dispatch')
class CreateStrategyView(CreateView):
    form_class = StrategyPostForm
    template_name = "post_strategy.html"
    success_url = reverse_lazy('strategyapp:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)

        # ここで self.request.user を CustomUser にキャスト
        postdata.user = CustomUser.objects.get(pk=self.request.user.pk)

        postdata.save()

        return super().form_valid(form)

class PostSuccessView(TemplateView):
    template_name = 'post_success.html'


class StrategyDetailView(DetailView):
    template_name = 'detail.html'
    model = StrategyPost

class TweetListView(ListView):
    model = Tweet
    template_name = 'tweets_list.html'
    context_object_name = 'tweets'
    ordering = ['-created_at']

class TweetCreateView(CreateView):
    form_class = TweetForm
    template_name = 'tweet_post.html'
    success_url = reverse_lazy('strategyapp:tweets_list')

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.user = self.request.user
        tweet.save()
        return super().form_valid(form)
    
class ContactView(FormView):
    template_name ='contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('strategyapp:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['question_title']
        message = form.cleaned_data['question_detail']
        
        subject = 'お問い合わせ：{}'.format(title)
        message_body = '送信者名：{0}\nメールアドレス:{1}\nタイトル:{2}\nメッセージ:{3}'.format(name, email, title, message)
        
        from_email = 'rasyleena111@gmail.com'
        to_list = ['rasyleena111@gmail.com']
        
        email_message = EmailMessage(subject=subject, body=message_body, from_email=from_email, to=to_list)
        email_message.send()
        
        messages.success(self.request, 'お問い合わせは正常に送信されました')
        return super().form_valid(form)