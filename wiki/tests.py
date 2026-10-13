from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import *
# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #makes a fake user
        cls.user = get_user_model().objects.create_user(
        username="testuser", email="testgmail.com", password="secret"
          )
        cls.post = Article.objects.create(
            #makes a fake post by the fake user
            title="a good title",
            body="nice body content",
            author=cls.user,
        )

        cls.comment = Comment.objects.create(
            # no idea how to manually accociate!
            #i have an idea of how to manuallly accociate
            article=cls.post,
            author=cls.user,
            body='nice comment',
        )
    def test_post_model(self):
        #tests if the post contains correct information and did not mess up
        self.assertEqual(self.post.title, "a good title")
        self.assertEqual(self.post.body, "nice body content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "a good title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
    def test_comment_moodel(self):
        self.assertEqual(self.comment.body, 'nice comment')
        self.assertEqual(self.comment.author.username, 'testuser')
       
    def test_url_exsists_at_correct_location_listview(self):
        #makes sure it exixsts where it should exist for the homepage
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_url_exsists_at_correct_location_detailview(self):
        #checks to make sure the post exists wheere it should
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exsists_at_correct_location_commentview(self):
        response=self.client.get('/post/1/comment')
        self.assertEqual(response.status_code, 200)
    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "a good title")
        self.assertTemplateUsed(response, "home.html")
    def test_post_detailview(self):
        response = self.client.get(reverse("wiki_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/wiki/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "nice body content")
        self.assertContains(response, 'nice comment')
        self.assertTemplateUsed(response, "article_detail.html")
    def test_create_view(self):
        response = self.client.post(
            reverse("wiki_new"),
            {
                "title": "new title",
                "body":"new body",
                "author": self.user.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.last().title, "new title")
        self.assertEqual(Article.objects.last().body,"new body")

    def test_create_comment(self):
        #i wrote this!!!!
        response = self.client.post(
            reverse('comment_new', kwargs={"pk": self.post.pk}),
            {
                "article":self.post, 
                "body": "nice new body",
                "author":self.user.id,
            }
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Comment.objects.last().body,"nice new body")

    def test_update_view(self):
        response = self.client.post(
            reverse("wiki_edit", args="1"),
            {
                "title": "newer title",
                "body":"newer body"


            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.last().title, "newer title")
        self.assertEqual(Article.objects.last().body,"newer body")
    def test_post_deleteview(self):
        response= self.client.post(reverse("wiki_delete", args="1"))
        self.assertEqual(response.status_code, 302)
