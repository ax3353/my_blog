from django import forms

from article.models import ArticlePost


class ArticlePostForm(forms.ModelForm):
    """
    写文章的表单类
    """

    class Meta:
        model = ArticlePost
        fields = ('title', 'body', 'tags', 'avatar')
