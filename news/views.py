
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView

from common.consts import OBJECT_STATUS_ACTIVE
from news.forms import NewsForm, CommentForm
from news.models import News, Comment
from news.tasks import send_informing_about_comment_email


class NewsView(ListView):
    template_name = "news.html"
    context_object_name = 'news'
    model = News
    paginate_by = 5
    queryset = News.objects.filter(news_status="A", status=OBJECT_STATUS_ACTIVE).order_by("-created")


class NewsDetailView(DetailView):
    template_name = "news_detail.html"
    context_object_name = 'news'
    model = News
    queryset = News.objects.filter(news_status="A", status=OBJECT_STATUS_ACTIVE)

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.get_object(), status=OBJECT_STATUS_ACTIVE).order_by("-created")
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm({"content": request.POST['comment'],
                            "author": request.user,
                            "news": self.get_object()})
        if form.is_valid():
            comment = form.save()
            if comment.news.author_id != comment.author_id:
                domain = get_current_site(self.request).domain
                send_informing_about_comment_email.delay(comment.news.author_id, comment.author_id, comment.news_id, domain)

        return redirect(reverse_lazy("news-detail", kwargs={ "pk": self.get_object().pk}))


class AddNewsView(LoginRequiredMixin, FormView):
    template_name = "add_news.html"
    success_url = reverse_lazy("news-added")
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.news_status = "A" if self.request.user.groups.filter(Q(name='Editor') | Q(name='Admin')).exists() else "IA"
        form.save()
        return super(AddNewsView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news') if self.request.user.groups.filter(Q(name='Editor') | Q(name='Admin')).exists() else reverse_lazy("news-added")


class EditNewsView(LoginRequiredMixin, UpdateView):
    template_name = "edit_news.html"
    success_url = reverse_lazy("news-added")
    form_class = NewsForm

    def get_queryset(self):
        return News.objects.filter(author=self.request.user, status=OBJECT_STATUS_ACTIVE)

    def get_initial(self):
        initial = super().get_initial()
        news = News.objects.get(pk=self.kwargs['pk'])

        initial['title'] = news.title
        initial['content'] = news.content

        return initial

    def form_valid(self, form):
        form.instance.news_status = "A" if self.request.user.groups.filter(Q(name='Editor') | Q(name='Admin')).exists() else "IA"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news') if self.request.user.groups.filter(Q(name='Editor') | Q(name='Admin')).exists() else reverse_lazy("news-added")



class NewsPremoderationMessageView(TemplateView):
    template_name = "message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Новость была отправлена на премодерацию"
        return context
