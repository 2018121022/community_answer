from django.shortcuts import render, redirect, get_object_or_404
from . models import Community
from .forms import CommentForm

# Create your views here.

def new(request):
    if request.method == 'GET':
        return render(request, 'new.html')
    else:
        community = Community()
        community.title = request.POST['title']
        community.content = request.POST['content']
        community.image = request.FILES.get('image')
        community.save()
        return redirect('detail', community.id)

def detail(request, community_id):
    community = get_object_or_404(Community, pk=community_id)
    return render(request, 'detail.html', {'community':community})

def index(request):
    community_index = Community.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'community_index':community_index})

def comment(request, community_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Community, pk=community_id)
        finished_form.save()
    return redirect('detail', community_id)

def page_not_found(request, exception):
    return render(request, '404.html')