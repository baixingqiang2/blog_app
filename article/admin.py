from django.contrib import admin
from .models import ArticlePost, Tui, Category, Keyword, Like


# #注册ArticlePost
# admin.site.register(ArticlePost)

@admin.register(ArticlePost)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'author', 'total_views','create_date','status')
    # 文章列表里显示想要显示的字段
    list_per_page = 6
    # 满50条数据就自动分页
    ordering = ('-create_date',)
    #后台数据列表排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点击进入编辑界面
    # 排除一些不想被编辑的 fields, 没有在列表的不可被编辑
    # fields = ('title', 'author', 'category','tags', 'avatar', 'excerpt', 'body')
    # 显示搜索框，搜索框大小写敏感
    search_fields = ('title',)
    #列表内可直接修改
    list_editable = ('status',)


#
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','parent_category','slug', 'index')


@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'like_article','like_user','pub_date')