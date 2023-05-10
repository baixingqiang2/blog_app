import re

import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from markdown.extensions.toc import TocExtension

from users.models import Profile
from .models import ArticlePost, Category, Like, default_image
# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404
# 引入HttpResponse
from django.http import HttpResponse, JsonResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from comment.models import Comment

#文章列表
def article_list(request,*args,**kwargs):
    search = request.GET.get('search')
    slug = request.GET.get('slug')
    order = request.GET.get('order')
    cite_cate = ''

    # 初始化查询集
    article_list = ArticlePost.objects.filter(status='p').all()
    # 用户搜索逻辑
    if search:
            article_list = ArticlePost.objects.filter(status='p').filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
    if slug: # 分类查询
        article_list = ArticlePost.objects.filter(Q(category__slug__icontains=slug))
        categoss = article_list.filter(category__slug=slug).values('category__name')
        if len(categoss) > 0 :
            cite_cate = categoss[0].get('category__name')
        else :
            cite_cate = ''

        # 查询集排序
    if order == 'total_views' :
        article_list = article_list.order_by('-total_views')

    catego = Category.objects.filter(parent_category__name='文章专栏').all()

    tui = ArticlePost.objects.filter(status='p').filter(tui__name='作者推荐')[:3]  # 查询推荐位ID为1的文章

    new_article = ArticlePost.objects.filter(status='p').all().order_by('-id')[0 :6]#最新文章


    page = request.GET.get("page")
    paginator = Paginator(article_list, 6)  # 实例化对象

    try :
        allarticle = paginator.page(page)  # 根据URL(页数)，获取相应的数据
    except PageNotAnInteger :
        allarticle = paginator.page(1)
    except EmptyPage :
        allarticle = paginator.page(paginator.num_pages)  # 页码不存在返回最后一页。


    context = {
        'search': search,
        'catego': catego,
        'tui': tui,
        'cite_cate':cite_cate,
        'new_article':new_article,
        "allarticle" : allarticle,
        'article_list':article_list,

    }

    return render(request, 'html/article.html', context)

#文章管理
@login_required(login_url='/users/login/')
def article_admin(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    user = request.user
    status = request.GET.get('status')
    article_list = ArticlePost.objects.filter(author=user).all()

    # 用户搜索逻辑
    if search :
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else :
        # 将 search 参数重置为空
        search = ''
    if status:
        article_list = article_list.filter(status=status)

        # 查询集排序
    if order == 'total_views' :
        article_list = article_list.order_by('-total_views')


    paginator = Paginator(article_list,10)
    page = request.GET.get('page',1)

    try :
        articles = paginator.get_page(page)
    except PageNotAnInteger :
        # 如果页码不是一个整数，返回第一页
        articles = paginator.get_page(1)
    except EmptyPage :
        # 如果页码超出范围，返回最后一页
        articles = paginator.get_page(paginator.num_pages)
    context = {
        'search':search,
        'order':order,
        'articles': articles,
        'page':page,
        'paginator':paginator,
    }
    return render(request, 'article/article_admin_list.html', context)

#文章详情
def article_detail(request,slug,id):
    #取出对应文章
    if request.method == "GET":
        curr_article = get_object_or_404(ArticlePost,id=id, slug=slug)
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                # 'markdown.extensions.toc',
                TocExtension(slugify=slugify),
            ]
        )
        curr_article.body = md.convert(curr_article.body)
        curr_toc = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        curr_article.toc = curr_toc.group(1) if curr_toc is not None else ''
        # 取出文章评论
        comments = Comment.objects.filter(article=curr_article)
        # 该文章所有点赞
        like_form = Like.objects.filter(like_article=curr_article)
        # 用户是否已经点过赞
        if request.session.get('is_login', None):
            like_user = like_form.filter(like_user=request.user)
        else:
            like_user = ''
        # 浏览量 +1
        # curr_article.update_views()

        # 过滤出所有的id比当前文章小的文章
        pre_article = ArticlePost.objects.filter(id__lt=id).order_by('-id')
        # 过滤出id大的文章
        next_article = ArticlePost.objects.filter(id__gt=id).order_by('id')

        # 取出相邻前一篇文章
        if pre_article.count() > 0 :
            pre_article = pre_article[0]
        else :
            pre_article = None

        # 取出相邻后一篇文章
        if next_article.count() > 0 :
            next_article = next_article[0]
        else :
            next_article = None

        article = curr_article

        # 需要传递给模板（templates）的对象
        context = {
            'article': article,
            'comments': comments,
            'pre_article': pre_article,
            'next_article': next_article,
            'like_form': like_form,
            'like_user': like_user,
            'toc': md.toc,
        }
        # render函数：载入模板，并返回context对象
        return render(request, 'article/detail.html', context)

# 写文章的视图
# 检查登录
@login_required(login_url='/users/login/')
def article_create(request):

    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = Profile.objects.get(id=1)
            if request.FILES:  # 判断是否上传图片，否则使用默认图片
                new_article.avatar = request.FILES['avatar']
            else:
                new_article.avatar = default_image()
            # 将新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        categorys = Category.objects.filter(parent_category__name='文章专栏').all()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
            'categorys': categorys
        }
        # 返回模板
        return render(request, 'article/create.html', context)

# 删除文章
@login_required(login_url='/users/login/')
def article_safe_delete(request,slug, id):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    article.delete()
    return redirect("article:article_admin")

# 修改文章
@login_required(login_url='/users/login/')
def article_update(request,slug,id):
    """
    这个视图函数用来修改文章
    通过POST方法提交表单，更新的有title、body等字段
    GET方法进入初始表单页面
    id为文章的id
    """
    article = get_object_or_404(ArticlePost,id=id, slug=slug)
    # 过滤非作者的用户
    if request.user != article.author :
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == 'GET' :
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        categorys = Category.objects.filter(parent_category__name='文章专栏').all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article' : article, 'article_post_form' : article_post_form,'categorys':categorys}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)

    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':

        # 将提交的数据赋值到表单实例
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.tags = request.POST['tags']
            if request.FILES:
                article.avatar = request.FILES['avatar']
            else:
                article.avatar = article.avatar
            article.status = request.POST['status']

            article.save(commit=False)
            #完成后返回到修改后的文章中，需要传入文章的id值
            return redirect("article:article_detail", id=id,slug=slug)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有问题啊，重新写一下！")
@login_required(login_url='/users/login/')
def update_status(request,slug,id):
    article = get_object_or_404(ArticlePost,slug=slug,id=id)
    if article.status == 'd':
        article.status = 'p'
    else:
        article.status = 'd'
    article.save()
    return redirect('article:article_detail',slug=slug,id=id)


#作者推荐
def author_suggest(request):
    suggest = ArticlePost.objects.all().order_by('total_views')[:3]
    categorys = Category.objects.all()

    context = {
        'categorys' : categorys,
        'suggest': suggest,
    }
    return render(request, 'html/article.html', context)

#分类导航

def tag(request, tag):
    pass

# 点赞视图
@login_required(login_url='/users/login/')
def article_like(request):
    slug = request.POST.get('post_slug')
    id = request.POST.get('post_id')
    article_like = get_object_or_404(ArticlePost,slug=slug, id=id)
    like_user = Like.objects.filter(like_article=article_like, like_user=request.user)
    if like_user.exists():
        like_user.delete()
        article_like.likes -= 1
        data = {'success' : False,'like_count':article_like.likes}
    else:
        Like.objects.create(like_article=article_like, like_user=request.user)
        article_like.likes += 1
        data = {'success' : True,'like_count':article_like.likes}
    article_like.save()
    return JsonResponse(data)
