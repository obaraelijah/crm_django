from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import  LeadModelForm,CustomUserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorandLoginRequiredMixin
# crud + List

class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
    
class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        #leads for entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else: 
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset
    
class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        #leads for entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else: 
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset
class LeadCreateView(OrganisorandLoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # sending email
        send_mail(
            subject="A lead has been created",
            message="Go to site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)
class LeadUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganisorandLoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    