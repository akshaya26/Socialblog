from django.shortcuts import render

# Create your views here.
from  django.contrib import  messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView,ListView,DetailView,DeleteView)
from django.http import Http404

from braces.views import SelectRelatedMixin
from  . import  models
from . import forms

from django.contrib.auth import get_user_model
User=get_user_model()


class PostList(SelectRelatedMixin,ListView):
    model= models.Post
    select_related = ('user','group')


class UserPosts(ListView):
    model=models.Post
    template_name = 'posts/user_post_list.html'
#We use select_related when the object that you're going to select is a single object,
    #  which means forward ForeignKey, OneToOne and backward OneToOne.

    #That means forward ManyToMany and backward ManyToMany, ForeignKey. prefetch_related does a separate lookup
    # for each relationship, and performs the “joining” in Python.
    def get_queryset(self):

        queryset = super().get_queryset()
        try:
            return_val= queryset.filter(user_id=self.request.user.id )

        except User.DoesNotExist:
            raise Http404
        else:

            return return_val


        # try:
        #
        #     self.post_user = User.objects.prefetch_related("posts").get(
        #         username__iexact=self.kwargs.get("username")
        #     )
        # except User.DoesNotExist:
        #     raise Http404
        # else:
        #     return self.post_user.posts.all()

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['post_user']=self.post_user
    #     return context


class PostDetail(SelectRelatedMixin,DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    fields=('message','group')
    model = models.Post

#BELOW IS DONE TO SAVE VALUE TO USER FIELD
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,DeleteView):
        model = models.Post
        select_related = ('user','group')
        success_url = reverse_lazy('posts:all')

        def get_queryset(self):
            queryset=super().get_queryset()
            return  queryset.filter(user_id=self.request.user.id)

        def delete(self, *args, **kwargs):
            messages.success(self.request,'Post Deleted')
            return super().delete(*args,**kwargs)




