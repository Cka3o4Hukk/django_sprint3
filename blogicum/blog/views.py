from blogicum import settings
from django.shortcuts import get_object_or_404, render
from .models import Post, Category
from django.utils.timezone import now


def index(request):
    posts = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )[:settings.POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    posts = get_object_or_404(
        Post.objects.select_related(
            'author', 'category', 'location',
        ).filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        ),
        id=post_id
    )

    return render(request, 'blog/detail.html', {'post': posts})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.post_set.filter(
        is_published=True,
        pub_date__lt=now()
    )
    return render(request, 'blog/category.html',
                  {'post_list': post_list, 'category': category})
