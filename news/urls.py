from django.conf.urls import url

from news.views import NewsView, AddNewsView, NewsPremoderationMessageView, NewsDetailView, EditNewsView

urlpatterns = [
    url(r'^add$', AddNewsView.as_view(), name='add-news'),
    url(r'^added$', NewsPremoderationMessageView.as_view(), name='news-added'),
    url(r'^edit/(?P<pk>[0-9]+)/?$', EditNewsView.as_view(), name='edit-news'),
    url(r'(?P<pk>[0-9]+)', NewsDetailView.as_view(), name='news-detail'),
    url(r'', NewsView.as_view(), name='news'),
]

