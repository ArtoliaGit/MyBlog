from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType


# Create your views here.
def blog_list(request):
    page_num = request.GET.get('page', 1)
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.PAGE_SIZE)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    paginator_list = get_page_list(paginator, current_page_num)

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['paginator_list'] = paginator_list
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

    page_num = request.GET.get('page', 1)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, settings.PAGE_SIZE)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    paginator_list = get_page_list(paginator, current_page_num)

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['paginator_list'] = paginator_list
    return render_to_response('blog/blogs_with_type.html', context)


def get_page_list(paginator, current_page_num):
    if current_page_num < 5:
        current_page_num = 3
    if current_page_num > paginator.num_pages - 4:
        current_page_num = paginator.num_pages - 2
    paginator_list = [x for x in range(current_page_num - 2,
                                       current_page_num + 3) if x > 0 and x <= paginator.num_pages]
    if paginator_list[0] != 1:
        paginator_list.insert(0, 1)
        if paginator_list[1] > 2:
            paginator_list.insert(1, '···')
    if paginator_list[-1] != paginator.num_pages:
        if current_page_num < paginator.num_pages - 3:
            paginator_list.append('···')
        paginator_list.append(paginator.num_pages)

    return paginator_list
