from django import forms
from .models import StrategyPost, Tweet, Reply

class StrategyPostForm(forms.ModelForm):
    class Meta:
        model = StrategyPost
        fields = ['title', 'comment', 'image1', 'image2'] 

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'ツイート内容を入力...'})
        }

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.CharField(label='メールアドレス')
    title = forms.CharField(label='件名')  # 'question_title' を 'title' に変更
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 共通の設定を一箇所で定義
        field_attributes = {
            'class': 'form-control',
            'placeholder': ''
        }
        
        # フィールドごとの個別設定
        self.fields['name'].widget.attrs.update({'placeholder': '田中  太郎', **field_attributes})
        self.fields['email'].widget.attrs.update({'placeholder': 'abcd@xx.com', **field_attributes})
        self.fields['title'].widget.attrs.update({'placeholder': 'タイトルを入力してください', **field_attributes})
        self.fields['message'].widget.attrs.update({'placeholder': 'メッセージを入力して下さい', **field_attributes})


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

    def __init__(self, *args, **kwargs):
        content_type = kwargs.pop('content_type', None)
        object_id = kwargs.pop('object_id', None)
        super().__init__(*args, **kwargs)

        if content_type and object_id:
            self.instance.content_type = content_type
            self.instance.object_id = object_id
