from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from article.models import ArticlePost
from .forms import CommentForm
from .models import Message, Comment


# 文章评论
@login_required(login_url='/users/login/')
def add_comment(request, slug, id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, slug=slug,id=id)
    # 处理 POST 请求
    if request.method == 'POST' :
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() :
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                # new_comment.parent_id = parent_comment.get_root().id

                new_comment.parent_id = parent_comment.id
                # 被回复人
                new_comment.reply_to = parent_comment.author
                new_comment.save()

                return redirect(article)

            new_comment.save()
            return redirect(article)
        else:
            return render(request,'article/detail.html')

@login_required(login_url='/users/login/')
def message_form(request):
    # 从html中提取数据保存到数据库中
    # 如果是POST，进行取数据
    if request.method == "POST":
        # 进行值的提取
        # POST属性调用get方法，可理解为dict字典所有用get方法,""代表值不存在的话设置默认值
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        message_text = request.POST.get("message", "")
        suggest_text = request.POST.get("suggest", "")

        message = Message()
        # 和上面对应
        message.name = name
        message.phone = phone
        message.email = email
        message.message = message_text
        message.suggest = suggest_text
        message.save()
    # 如果是get，直接render页面
        return redirect(request, "html/about.html")
# 从服务器中提取出数据展示到html页面
    if request.method == "GET":
        var_dict = {}
        # 这里取数据使用filter方法，如果没有数据会返回一个空的list
        all_message = Message.objects.filter()
        if all_message:# 判断是否有数据，若没有数据取第0个会报错
            message = all_message[0]# 取第0个时会直接转为message对象而不是原来的QuerySet
            # 将views中的数据传到html页面中，传入一个字典{}，键值对的名称可以任意写，值需要为message
            var_dict = {
                "message":message
            }
            return render(request,"html/about.html", var_dict)
            # 或者可以直接写为：locals(),可以将所有的局部变量全部变成key-value的形式，但此习惯不好
            # return render(request, "message_form.html", locals())
        else:# 若没有数据直接返回页面，不然会抛异常
            return render(request, "html/about.html")


