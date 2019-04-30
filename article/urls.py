# Django2.0之后，app的urls.py必须配置app_name，否则会报错
from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    # 文章列表
    path('article-list/', views.article_list, name='article-list'),
    # 文章详情 (Django2.0的path新语法用尖括号<>定义需要传递的参数。这里需要传递名叫id的整数到视图函数中去)
    path('article-detail/<int:id>/', views.article_detail, name='article-detail'),
    # 创建文章
    path('article-create/', views.article_create, name='article-create'),
    # 删除文章
    path('article-delete/<int:id>/', views.article_delete, name='article-delete'),
    # 修改文章
    path('article-update/<int:id>/', views.article_update, name='article-update'),
]
