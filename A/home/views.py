from django.shortcuts import render , redirect
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


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
    form_class = PostCreateUpdateForm
    def setup(self, request, *args, **kwargs):
        self.post_instans = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instans
        if not post.user.id == request.user.id:
            messages.error(request, 'You Cant Update This Post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,*args, **kwargs):
        post = self.post_instans
        form = self.form_class(instance=post)
        return render(request,'home/update.html',{'form':form})

    def post(self,request,*args, **kwargs):
        post = self.post_instans
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug =slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,'You apdated this post','success')
            return redirect('home:post_detail',post.id,post.slug)


class PostCreateView(LoginRequiredMixin , View):
    form_class = PostCreateUpdateForm
    def get(self,request,*args, **kwargs):
        form = self.form_class
        return render(request,'home/create.html/',{'form':form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request,'You Create A New Post','success')
            return redirect('home:post_detail',new_post.id,new_post.slug)



