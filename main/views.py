from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, PostForm, EditProfileForm, CustomLoginForm, Edit_Form, PasswordChange
from .models import Student, Post, Teacher, Category, Profile
from django.views.generic import ListView,DetailView,CreateView,TemplateView,UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.views import generic
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, get_object_or_404

class Homepage(ListView):
    model = Student 
    template_name = 'homepage.html'
    ordering = ['-id']

def search_website(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')

        search_filter = Q(title__icontains=searched) | Q(body__icontains=searched)

        posts = Post.objects.filter(search_filter)

        return render(request, 'search.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'search.html', {})


class Update(UpdateView):
    model = Post
    form_class = Edit_Form
    template_name = "update.html"

    def get_success_url(self):
        return reverse_lazy('details', args=[self.object.pk])

class Delete(DeleteView):
    model = Post
    template_name = "delete.html"

    def get_success_url(self):
        # Get the category of the post being deleted
        category = self.object.category  # Assuming 'category' is the ForeignKey field name

        # Generate the URL for the category detail view
        category_url = reverse_lazy('category', args=[category.pk])

        return category_url



class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student.objects.create(
                user=user,
                strand=form.cleaned_data['strand'],
                grade_level=form.cleaned_data['grade_level']
            )
            login(request, user)
            return redirect('homepage')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(View):
    form_class = CustomLoginForm 
    template_name = 'registration/login.html'


class Details(DetailView):
    model = Post
    template_name = 'details.html'
    ordering = ['-id']

class CategoryDetailView(DetailView):
    model = Category 
    template_name = 'category.html'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filter posts based on the category or subject associated with the current view
        context['posts'] = Post.objects.filter(category=self.object)  # You can use 'subject' here too if needed
        
        return context

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.user, request.POST, request.FILES)  # Pass request.FILES to handle file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            teacher = Teacher.objects.get(teacher=request.user)
            chosen_subject = post.subject

            try:
                category = Category.objects.get(subject=chosen_subject)
            except Category.DoesNotExist:
                category = None

            post.category = category
            post.save()
            return redirect('homepage')
    else:
        form = PostForm(request.user)
    return render(request, 'post.html', {'form': form})



def categories_context(request):
    categories = Category.objects.all()  # Fetch all categories
    return {'categories': categories}


def post_context(request):
    posts = Post.objects.all()  # Fetch all categories
    return {'posts': posts}


class About_Us(ListView):
    template_name = "about.html" 
    model = Post 


class UserEdit(generic.UpdateView):
    form_class = EditProfileForm 
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChange
    success_url = reverse_lazy('homepage')

class ProfilePage(DetailView):
    model = Profile
    template_name = 'registration/profile_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        page_user = self.object  # Use self.object to access the current profile

        context["page_user"] = page_user
        return context
