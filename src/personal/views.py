from django.shortcuts import render
from blog.models import BlogPost
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from blog.views import get_blog_queryset

BLOG_POSTS_PER_PAGE = 10


def home_page(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query),
                        key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_page)
    context['blog_posts'] = blog_posts

    return render(request, 'personal/home.html', context)
