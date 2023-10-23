from django.shortcuts import render , redirect
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostUpdateForm


# Create your views here.
class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,'home/index.html', {'posts': posts})
    def post(self,request):
        return render(request,'home/index.html')


class PostDetailVeiw(View):
    def get(self ,request, post_id, post_slug):
        post = Post.objects.get(pk = post_id , slug=post_slug)
        return render(request,'home/detail.html',{'post':post})

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk = post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,"post deleted successfully",'success')
        else:
            messages.error(request,"you can not delete this post",'danger')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateForm
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])
        if not post.user.id == request.user.id:
            messages.error(request, 'You Cant Update This Post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,post_id):
        form = self.form_class
        return render(request,'home/update.html',{'form':form})

    def post(self,request,post_id):
        pass

