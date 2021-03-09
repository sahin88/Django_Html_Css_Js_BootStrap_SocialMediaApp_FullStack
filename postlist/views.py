from django.shortcuts import render, get_object_or_404, redirect
from .models import postList, comments as yorum  # ,  # Like
from .forms import postForm, ContactForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import UserProfile
from core.forms import UserAdditionForm2
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from .decorations import allowed_users,isUserauthenticated,isUserauthenticatedorAdmin
from django.views.generic import ListView, DetailView,DeleteView, CreateView,UpdateView

class PostListView(ListView):
	model=postList

	template_name='/home/alex/Documents/soc-med/templates/home.html'
	context_object_name='posts'
	ordering=['-created_date']
	paginate_by=5

# Create your views here.


def home(request):
    
    page_obj = postList.objects.all()
    paginator = Paginator(page_obj, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    com = yorum.objects.all()
    bos_list = []
    dict_list = []
    for ids in postList.objects.all():
        bos_list.append(ids.id)

    for id_index in range(len(bos_list)):
        post_instance = get_object_or_404(postList, id=bos_list[id_index])
        num_comment_by_id = yorum.objects.filter(post_id=post_instance).count()
        dict_list.append(
            ((bos_list[id_index]), (num_comment_by_id)))

    # total_comment_dict = dict(dict_list)

    # print('total_comment_dict', dict_list)

    query = request.GET.get('q')
    if query:
        page_obj = postList.objects.all()
        posts = page_obj.filter(caption__icontains=query)
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    post_latest = postList.objects.filter().order_by('-created_date')[0:3]
    paginator = Paginator(post_latest, 1)
    page_number = request.GET.get('page')
    post_latest = paginator.get_page(page_number)
    total_comment = dict(dict_list)

    print('total_comment', com)

    return render(request, 'home.html', {'posts':  page_obj, 'post_latest': post_latest, 'UserProfile': UserProfile, 'comments': com, 'total_comment': total_comment})


@login_required
def post_detail(request, id):
    po = postList.objects.get(id=id)
    comment = yorum.objects.filter(post_id=po)
    total = {'total': len(comment)}
    return render(request, 'detail.html', {'post': po, 'yorum': total,  'comments': comment})


@login_required
def logout(request):
    print('clicked')
    return logout()


@login_required
def comment_detail(request, id):
    po = yorum.objects.filter(post_id=id).count()
    print('po', po)
    return po


@login_required
def post_update(request, id):
    po = get_object_or_404(postList, id=id)
    form = postForm(request.POST or None, request.FILES or None, instance=po)
    if form.instance.author != request.user:
        messages.error(
            request, 'You try to change the post, which not belong to you!')
        logout(request)
        return redirect('login')
    form = postForm(request.POST or None, request.FILES or None, instance=po)
    if form.is_valid() and form.instance.author == request.user:
        form.save()
        return redirect('home')

    return render(request, 'update.html', {'form': form})


@login_required

def post_delete(request, id):
    po = get_object_or_404(postList, id=id)
    form = postForm(request.POST or None, instance=po)
    if form.instance.author != request.user  or request.user.is_superuser:
        messages.error(request, 'You try to change the post, which not belong to you!')
        logout(request)
        return redirect('login')
    else:
        po.delete()
    return redirect('home')


@login_required


# @allowed_users(allowed_roles=['admin'])

def comments_delete(request, id):
    po = get_object_or_404(yorum, id=id)
    form = postForm(request.POST or None, instance=po)
    if form.instance.author != request.user or request.user.is_superuser:
        messages.error(
            request, 'You try to change the post, which not belong to you!')
        logout(request)
        return redirect('login')
    else:
        po.delete()
        return redirect('home')


@login_required
def comments_create(request):
    comment = request.POST.get('comm')
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    po = get_object_or_404(postList, id=int(post_id))
    if comment==" Enter your comments ...":
        return redirect('home')

    try:
        saving_ = yorum.objects.create(
            user_id=request.user, post_id=po, comments=comment)
        print('se', saving_)

    except Exception as identifier:
        print('identifier', identifier)
    print('data', comment, 'user_id', user_id, 'post_id', post_id)
    return redirect('home')


@login_required
def post_create(request):
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)
        form.instance.author = request.user
        form.save()
        return redirect('home')
    else:
        form = postForm()
    return render(request, 'create.html', {'form': form})


@login_required
def user_profil(request, username, id):
    page_obj = postList.objects.all().filter(author__username__icontains=username)
    paginator = Paginator(page_obj, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    user_profile = get_object_or_404(UserProfile, user_id=id)
    total_comment = []
    posts = postList.objects.all().filter(author__username__icontains=username)
    user = get_object_or_404(User, id=id)
    comments = yorum.objects.filter(user_id=user)
    for post in posts:
        total = comments.filter(
            post_id=get_object_or_404(postList, id=post.id))
        total_comment.append((post.id, len(total)))
    total_dict = dict(total_comment)
    context = {}
    context['posts'] = posts
    # post_2 = {'user': 'hayyam'}
    context['post_2'] = user_profile
    context['comments'] = comments
    context['totalComment'] = total_dict
    context['page_obj']=page_obj

    return render(request, 'profile.html', context=context)


@login_required
def post_likes(request):
    # iterlists()
    user = request.user
    comin = dict(request.POST)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
    post_obj = postList.objects.get(id=post_id)
    if user in post_obj.likes.all():
        post_obj.likes.remove(user)
    else:
        post_obj.likes.add(user)

    return redirect('home')


@login_required
def profil_update(request, id):
    user_object = get_object_or_404(UserProfile, user_id=id)

    forms = UserAdditionForm2(request.POST or None,
                              request.FILES or None, instance=user_object)
    if forms.is_valid():
        forms.save()
        return redirect('home')
    context = {'form': forms}
    return render(request, 'profile_update.html', context)


@login_required
def unfollow(request, username):
    user_profile = get_object_or_404(User, username=username)

    request.user.userprofile.friends.remove(user_profile)
    return redirect('page_of_user', username=user_profile.username, id=user_profile.id)


@login_required
def follow(request, username):
    user_profile = get_object_or_404(User, username=username)

    request.user.userprofile.friends.add(user_profile)
    return redirect('page_of_user', username=user_profile.username, id=user_profile.id)


@login_required
def email(request, username):
    if request.method == 'GET':
        form = ContactForm()
        user_profile = get_object_or_404(User, username=username)
        print('user_profile', user_profile.userprofile.email)
        form.from_email = user_profile.userprofile.email

    else:

        user_profile = get_object_or_404(User, username=username)
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = user_profile.email
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "email.html", {'form': form})


@login_required
def thanks(request):
    return render(request, "thanks.html")
