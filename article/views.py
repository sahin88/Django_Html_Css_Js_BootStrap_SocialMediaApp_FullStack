from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Article
from  .forms import ArticleForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def upload(request):
	if request.method=='POST':
		form=ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('article-list')
	else:
		form=ArticleForm()
	return render(request, 'article.html', {'form':form})
@login_required
def delete_article(request,pk):
	if request.method=='POST':
		article=Article.objects.get(pk=pk)
		article.delete()
		return redirect('article-list')

@login_required
def list(request):
	articles=Article.objects.all()

	return render(request, 'article_list.html',{'articles':articles})
