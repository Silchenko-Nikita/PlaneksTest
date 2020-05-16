from django.forms import ModelForm

from news.models import News, Comment


class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = ('title', 'tag', 'content')


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('news', 'author', 'content')
