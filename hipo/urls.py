"""hipo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views as accounts_views
from interactions import views as interactions_views
from recipes import views as recipes_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", recipes_views.RecipeListView.as_view(), name="home"),
    path("share/", recipes_views.ShareView.as_view(), name="share"),
    path(
        "recipes/<int:ingredient_pk>/",
        recipes_views.ListByIngredientView.as_view(),
        name="recipes",
    ),
    path(
        "recipe/<int:recipe_pk>/",
        recipes_views.RecipeDetailView.as_view(),
        name="detail",
    ),
    path("signup/", accounts_views.Signup.as_view(), name="signup"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("like/<int:recipe_pk>/", interactions_views.LikeView.as_view(), name="like"),
    path("rate/<int:recipe_pk>/", interactions_views.RateView.as_view(), name="rate"),
    path("search/", recipes_views.SearchView.as_view(), name="search"),
    path(
        "recipe/<int:recipe_pk>/edit/",
        recipes_views.RecipeUpdateView.as_view(),
        name="edit",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
