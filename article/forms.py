from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import ArticlePost



class ArticlePostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ArticlePost
        fields =('title', 'body', 'tags', 'avatar', 'status')
