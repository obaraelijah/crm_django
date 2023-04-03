from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent, Category
from .forms import  LeadModelForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm
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
            queryset= Lead.objects.filter(
                organisation=user.userprofile,
                agent__null=False
            )
        else: 
            queryset= Lead.objects.filter(organisation=user.agent.organisation, agent__null=False)
            #filter for agent
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset= Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context
        
    
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
    
class AssignAgentView(OrganisorandLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    
    #pass extra args to form
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form) 
    
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organisor:
            queryset= Lead.objects.filter(
                organisation=user.userprofile,
            )
        else: 
            queryset= Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
            context.update({
                "unassigned_lead_count":queryset.filter(category__isnull=True).count()
            })
            return context
    
    def get_queryset(self):
        user = self.request.user
        #leads for entire organisation
        if user.is_organisor:
            queryset= Category.objects.filter(
                organisation=user.userprofile,
            )
        else: 
            queryset= Category.objects.filter(
                organisation=user.agent.organisation, 
            )
        return queryset
    
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        
        leads = self.get_object().leads.all()
        context.update({
                "leads": leads
         })
        return context
    
    def get_queryset(self):
        user = self.request.user
        #leads for entire organisation
        if user.is_organisor:
            queryset= Category.objects.filter(
                organisation=user.userprofile,
            )
        else: 
            queryset= Category.objects.filter(
                organisation=user.agent.organisation, 
            )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    
    
    def get_queryset(self):
         user = self.request.user
        #leads for entire organisation
         user = self.request.user
        #leads for entire organisation
         if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
         else: 
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent
            queryset = queryset.filter(agent__user=self.request.user)
         return queryset
    
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})