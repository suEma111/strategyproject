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
    title = forms.CharField(label='件名')
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['placeholder'] = \
            '田中  太郎'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        
        self.fields['email'].widget.attrs['placeholder'] = \
            'abcd@xx.com'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        
        self.fields['title'].widget.attrs['placeholder'] = \
            'タイトルを入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        
        self.fields['message'].widget.attrs['placeholder'] = \
            'メッセージを入力して下さい'
        self.fields['message'].widget.attrs['class'] = 'form-control'

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'コメントを入力してください'}),
        }