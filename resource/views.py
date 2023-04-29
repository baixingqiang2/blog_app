from django.shortcuts import render
from .models import File
from article.models import Category
# Create your views here.

def resource(request):
    allcategorys = Category.objects.filter(parent_category__name='资源分享').all()
    slug = request.GET.get('slug')
    if slug :
        resources = File.objects.filter(slug=slug).order_by('-id')
    else :
        resources = File.objects.all().order_by('-id')
    context = {
        'categorys':allcategorys,
        'resources' : resources,
    }
    return render(request, 'html/resource.html', context)

