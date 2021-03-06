# 视图函数
import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from article.forms import ArticlePostForm
from article.models import ArticlePost, ArticleColumn


# 查看article列表
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')

    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search))
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


# 文章article详情
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
    ], safe_mode=True, enable_attributes=False)
    article.body = md.convert(article.body)

    context = {'article': article, 'toc': md.toc }

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    return render(request, 'article/detail.html', context)


# 创建article
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 当前登录用户id
            new_article.author = User.objects.get(id=request.user.id)
            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 保存article
            new_article.save()
            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            return redirect('article:article-list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = { 'article_post_form': article_post_form, 'columns': columns }
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者且不是超级管理员的用户
    if request.user != article.author and (not request.user.is_superuser):
        return HttpResponse("抱歉，你无权删除这篇文章。")

    article.delete()
    return redirect("article:article-list")


# 修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者且不是超级管理员的用户
    if request.user != article.author and (not request.user.is_superuser):
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            tags = request.POST['tags']
            if tags.strip() != '':
                tags_arr = tags.replace(' ', '').split(',')
                article.tags.set(*tags_arr, clear=False)
            else:
                article.tags.clear()

            # 保存article
            article.save()
            return redirect('article:article-detail', id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/update.html', context)
