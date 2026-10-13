from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
# Create your views here.
class WikiList(ListView):
    model = Article
    template_name = "home.html"


class WikiDetail(DetailView):
    model= Article
    template_name = 'article_detail.html'


class WikiCreateView(CreateView):
    model= Article
    template_name='article_new.html'
    fields=['title', 'author', 'body']


class WikiEditView(UpdateView):
    model=Article
    template_name='article_edit.html'
    fields=['title', 'body']
    
class WikiCommentView(CreateView):
    model=Comment
    template_name='comment_new.html'
    fields=['author', 'body']
    def form_valid(self, form):
        # 1. Look up the specific article using the ID passed via the URL route
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        
        # 2. Bind the article to the comment instance without saving to DB yet
        form.instance.article = article
        
        # 3. Call the super class to save the model and handle the redirect
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Article
    template_name='article_delete.html'
    success_url = reverse_lazy('home')


