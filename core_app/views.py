# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CommentForm
from .models import Category, Comment, Post


class PostListView(ListView):
    paginate_by = 4
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create.html"
    fields = ["title", "body", "category", "snippet", "published", "image"]
    context_object_name = "post"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


def PostDetailView(request, pk):
    cat_menu = Category.objects.all()
    stuff = get_object_or_404(Post, id=pk)
    post = Post.objects.get(id=pk)

    comments = post.comments.filter(active=True)
    new_comment = None

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    total_likes = stuff.total_likes
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(
        request,
        "blog/detail.html",
        {
            "form": form,
            "comments": comments,
            "post": post,
            "total_likes": total_likes,
            "cat_menu": cat_menu,
            "liked": liked,
        },
    )


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/update.html"
    fields = ["title", "body", "category", "snippet", "published", "image"]
    login_url = "login"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/delete.html"
    success_url = reverse_lazy("post_list")
    login_url = "login"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = "category/category_add.html"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_menu"] = Category.objects.all()
        return context


def CategoryView(request, cats):
    cat_menu = Category.objects.all()
    category_list = Post.objects.filter(category__name__contains=cats.replace("-", " "))

    return render(
        request,
        "category/categories.html",
        {
            "cats": cats.title().replace("-", " "),
            "category_list": category_list,
            "cat_menu": cat_menu,
        },
    )


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("post_detail", args=[str(pk)]))


class CommentCreateView(CreateView):
    model = Comment
    template_name = "comment.html"
    fields = ["name", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "comment/comment_update.html"
    fields = ["name", "body"]
    success_url = reverse_lazy("post_detail")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        comment = form.save()
        self.pk = comment.post.pk
        return super(CommentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment/comment_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        comment = form.save()
        self.pk = comment.post.pk


def reply_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get("post_id")  # from hidden input
            parent_id = request.POST.get("parent")  # from hidden input
            post_url = request.POST.get("post_url")  # from hidden input
            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url + "#" + str(reply.id))

        context = {"form": form}
    return render(request, context)


class SearchResultsListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        ).distinct()

