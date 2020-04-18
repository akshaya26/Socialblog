from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import  (LoginRequiredMixin,
                                         PermissionRequiredMixin)
from django.urls import  reverse
from  django.views.generic import (CreateView,DetailView,ListView
                                   ,RedirectView)
from .models import Group,GroupMember
# Create your views here.
from django.contrib.auth import get_user_model
User=get_user_model()

class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description')
    model = Group
    #CreateView redirects like below
    # """Return the URL to redirect to after processing a valid form."""
    # if self.success_url:
    #     url = self.success_url.format(**self.object.__dict__)
    # else:
    #     try:
    #         url = self.object.get_absolute_url()

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

#This is a top-level method, and there's one for each HTTP verb - get(), post(), patch(), etc.
    # You would override it when you want to do something before a request is processed by the view, or after.
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except:
            messages.warning(self.request,'You are already a member')
        else:
            messages.success(self.request,'You are a member')

        return super().get(request,*args,**kwargs)# this calles the get method of parent class redirect view


class LeaveGroup(LoginRequiredMixin,RedirectView):
    #class django.views.generic.base.RedirectView¶
# Redirects to a given URL.
#
# The given URL may contain dictionary-style string formatting, which will be interpolated against the
# parameters captured in the URL. Because keyword interpolation is always done (even if no arguments are passed in),
# any "%" characters in the URL must be written as "%%" so that Python will convert them to a single percent sign on output.
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership=GroupMember.objects.filter(user=self.request.user,
                                                  group__slug=self.kwargs.get('slug')).get()

        except GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not a member')

        else:
            membership.delete()
            messages.success(self.request,'You have left the group')

        return  super().get(request,*args,**kwargs)


