from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Project
from django.contrib.auth.decorators import login_required


# Create your views here.
'''
@login_required
def get_projects(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        budget = request.POST.get("budget")
        deadline = request.POST.get("deadline")
        project = Project.objects.create(
            title=title,
            description=description,
            budget=budget,
            deadline=deadline
        )
        return render(request, "projects/project_template.html", {"project": project})
    elif request.method == "GET":
    projects = Project.objects.all()
    return render(request, "projects/projects_list.html", {"projects": projects})


def get_project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, "projects/project_template.html", {"project": project})

'''


class ProjectView(View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, "projects/projects_list.html", {"projects": projects})




class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

'''
class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['title', 'description', 'budget', 'deadline']
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.employer = self.request.user.employerprofile  # Предполагаем, что у пользователя есть профиль работодателя
        return super().form_valid(form)
'''