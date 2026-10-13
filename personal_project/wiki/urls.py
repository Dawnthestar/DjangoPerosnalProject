from django.urls import path
from .views import*
urlpatterns = [
    path('', WikiList.as_view(), name='home'),
    path('post/<int:pk>/', WikiDetail.as_view(), name='wiki_detail'),
    path('post/new', WikiCreateView.as_view(), name='wiki_new'),
    path('post/<int:pk>/edit', WikiEditView.as_view(), name='wiki_edit'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='wiki_delete'),
    path('post/<int:pk>/comment', WikiCommentView.as_view(), name= 'comment_new'),


]
