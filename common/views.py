from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from article.models import ArticlePost,Category
from resource.models import File,PictureWall
from users.models import Profile
from common.models import Notice,Link,Banner



def header_views(request):
    us_id = request.GET.get('user_id')
    profiles = Profile.objects.filter(user_id=us_id)
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()

    context={
        'profiles': profiles,
        'linecategory': linecategory,
    }

    return render(request, 'header.html',context)

def index_views(request):


    links = Link.objects.all()  # 链接列表

    banner = Banner.objects.filter(is_active=True)[0 :4]  # 查询所有幻灯图数据，并进行切片

    tui = ArticlePost.objects.filter(status='p').filter(tui__name='最新推荐')[:6]  # 查询推荐位ID为1的文章

    hot = ArticlePost.objects.filter(status='p').order_by('total_views')[:10]  # 热文排行列表

    notices = Notice.objects.all() #公告列表

    page = request.GET.get("page")
    content_list = ArticlePost.objects.filter(status='p').order_by('-id')  # 从数据取数据
    paginator = Paginator(content_list, 4)  # 实例化对象

    try :
        articles = paginator.page(page)  # 根据URL(页数)，获取相应的数据
    except PageNotAnInteger :
        articles = paginator.page(1)
    except EmptyPage :
        articles = paginator.page(paginator.num_pages)  # 页码不存在返回最后一页。

    context = {
        'articles':articles,
        'links': links,
        'banner': banner,
        'tui': tui,
        'hot': hot,
        'notices': notices,
    }
    return render(request, 'home.html',context)

def about_views(request):
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()
    links = Link.objects.all()
    adminuser = Profile.objects.filter(is_superuser=True).values()
    profiles =Profile.objects.filter(is_superuser=True).all
    context = {
        'links': links,
        'adminuser':adminuser,
        'profiles':profiles,
        'linecategory' : linecategory,
    }
    return render(request, 'html/about.html',context)

def resource_views(request):
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()
    categorys = Category.objects.filter(parent_category__name='资源分享').all()
    resources = File.objects.all()
    context ={
        'categorys': categorys,
        'resources': resources,
        'linecategory' : linecategory,
    }
    return render(request, 'html/resource.html',context)

def timeline_views(request):
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()
    context = {
        'linecategory': linecategory,
    }
    return render(request, 'html/timeline.html',context)
    # return render(request, 'banner.html')

def picturewall(request):
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()
    picturewalls = PictureWall.objects.all()
    context = {
        'linecategory' : linecategory,
        'picturewalls': picturewalls,
    }
    return render(request,'timeline/picturewall.html',context)

def musicland(request):
    linecategory = Category.objects.filter(parent_category__name='展示墙').all()
    context = {
        'linecategory' : linecategory,
    }
    return render(request,'timeline/musicland.html',context)


def error_404_view(request, exception):
    return render(request, 'error/404.html', status=404)


def error_403_view(request, exception) :
    return render(request, 'error/403.html', status=403)


def error_400_view(request, exception):
    return render(request, 'error/400.html', status=400)


def error_500_view(request):
    return render(request, 'error/500.html', status=500)
