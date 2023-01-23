from django.shortcuts import render, redirect
from task.forms import TaskForm, RegistrationForm, LoginForm
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, FormView
from task.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator


def signin_requried(fn):
    def wrapper(request, *args, **kw):

        if not request.user.is_authenticated:
            messages.error(request, 'you must login')
            return redirect('signin')
        else:
            return fn(request, *args, **kw)

    return wrapper


@method_decorator(signin_requried, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        messages.success(self.request, 'account created')
        return super().form_valid(form)


class SigninView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kw):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, self.template_name, {'form': form})


@method_decorator(signin_requried, name='dispatch')
class TaskCreateView(CreateView):
    template_name = 'task-add.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'task created')
        return super().form_valid(form)

    # def get(self, request, *args, **kw):
    #     form = TaskForm()
    #     return render(request, 'task-add.html', {'form':form})

    # def post(self, request, *args, **kw):
    #     form = TaskForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    #         return redirect('task-create')
    #     else:
    #         return render(request, 'task-add.html', {'form':form})


@method_decorator(signin_requried, name='dispatch')
class TskListView(ListView):
    model = Task
    template_name = 'task-list.html'
    context_object_name = 'todo'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    # def get(self, request, *args, **kw):
    #     qs = Task.objects.all()
    #     return render(request, 'task-list.html', {'todo':qs})


@method_decorator(signin_requried, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task-detail.html'
    context_object_name = 'detail'
    pk_url_kwarg = 'id'
    # def get(self, request, *args, **kwargs):
    #     id = kwargs.get('id')
    #     qs = Task.objects.get(id=id)
    #     return render(request, 'task-detail.html', {'detail':qs} )


@method_decorator(signin_requried, name='dispatch')
class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Task.objects.get(id=id).delete()
        messages.success(self.request, 'task deleted')
        return redirect('task-list')


@signin_requried
def sign_out(request, *args, **kw):
    logout(request)
    return redirect('signin')
