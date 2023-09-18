from django.shortcuts import render, redirect, get_object_or_404
from . models import Community, Comment
from .forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/account/login/')
def new(request):
    if request.method == 'GET':
        return render(request, 'new.html')
    else:
        community = Community()
        community.title = request.POST['title']
        community.content = request.POST['content']
        community.image = request.FILES.get('image')
        community.author = request.user
        community.save()
        return redirect('detail', community.id)

@login_required(login_url='/account/login/')
def detail(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    return render(request, 'detail.html', {'community':community})

def index(request):
    community_index = Community.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'community_index':community_index})

@login_required(login_url='/account/login/')
@csrf_exempt
def comment(request, community_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Community, pk=community_id)
        finished_form.author = request.user
        finished_form.save()
    return redirect('detail', community_id)

def page_not_found(request, exception):
    return render(request, '404.html')

@login_required(login_url='/account/login/')
def update(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    if request.method == 'POST':
        community.title = request.POST['title']
        community.content = request.POST['content']
        community.image = request.FILES.get('image')
        community.author = request.user
        community.save()
        return redirect('detail', community.id)
    else:
        return render(request, 'update.html', {'community':community})

@login_required(login_url='/account/login/')
def delete(reuqest, community_id):
    community = Community.objects.get(id=community_id)
    community.delete()
    return redirect('index')

@login_required(login_url='/account/login/')
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    community_id = comment.post.id
    comment.delete()
    return redirect('detail', community_id)