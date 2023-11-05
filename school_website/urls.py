from django.contrib import admin
from django import views 
from django.urls import path, include
from main.views import RegistrationView, ProfilePage,Homepage, Details, create_post, CategoryDetailView, search_website, Update, Delete, UserEdit, About_Us, PasswordChangeView, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views 
from django.urls import reverse_lazy



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name=''),
    path('details/<int:pk>', Details.as_view(), name="details"),
    path('category/<int:pk>', CategoryDetailView.as_view(), name="category"), 
    path('post/', create_post, name="post"),
    path('', Homepage.as_view(), name="homepage"),
    path('about_us/', About_Us.as_view(), name="about"),
    path('search/', search_website, name="search"),
    path('users/', include("django.contrib.auth.urls")),
    path('edit/<int:pk>', Update.as_view(), name="edit"),
    path('delete/<int:pk>', Delete.as_view(), name="delete"),
    path('edit_profile/', UserEdit.as_view(), name='edit_profile'),
    path('password/', PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('<int:pk>/profile_page/', ProfilePage.as_view(), name="profile_page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
