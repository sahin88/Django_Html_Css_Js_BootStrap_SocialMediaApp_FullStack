"""filesystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_view
from article import views as article_view
from postlist import views as postlist_view
from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', postlist_view.home, name='home'),
    path('signup', core_view.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('article/upload/', article_view.upload, name='article-upload'),
    path('article/list/', article_view.list, name='article-list'),
    path('article/<int:pk>/', article_view.delete_article, name='delete_article'),
    path('post/<int:id>/detail/', postlist_view.post_detail, name='post_detail'),
    path('post/<int:id>/update/', postlist_view.post_update, name='post_update'),
    path('post/<int:id>/delete/', postlist_view.post_delete, name='post_delete'),
    path('comments/<int:id>/delete/',
         postlist_view.comments_delete, name='comments_delete'),
    path('comment/<int:id>/detail/',
         postlist_view.comment_detail, name='comment_detail'),
    path('comments/create/',
         postlist_view.comments_create, name='comments_create'),
    path('post/create/', postlist_view.post_create, name='post_create'),
    path('profil/<str:username>/<int:id>/',
         postlist_view.user_profil, name='page_of_user'),
    path('post-likes/', postlist_view.post_likes, name='post_like'),
    path('friend-unfollow/<str:username>/',
         postlist_view.unfollow, name='f_unfollow'),
    path('friend-follow/<str:username>/',
         postlist_view.follow, name='follow'),

    path('accounts/logout', core_view.signOut, name='logout'),
    path('profil/<int:id>/update/',
         postlist_view.profil_update, name='profile_update'),
    path('email/<str:username>/',
         postlist_view.email, name='email'),
    path('thanks/',
         postlist_view.thanks, name='thanks')



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.STATIC_URL,
#                       document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL,
#                       document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
