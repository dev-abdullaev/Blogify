from ckeditor.fields import RichTextField

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post_list")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_images/")
    facebook_url = models.CharField(max_length=550, null=True, blank=True)
    instagram_url = models.CharField(max_length=550, null=True, blank=True)
    twitter_url = models.CharField(max_length=550, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="post", on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="pictures/")
    likes = models.ManyToManyField(User, related_name="blog_post")
    snippet = models.CharField(max_length=250, default="Click read more button to read...")

    class Meta:
        ordering = ["-created", "-published"]

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, null=True, blank=True, related_name="comment_owner", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.post.title} |  {self.author}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
