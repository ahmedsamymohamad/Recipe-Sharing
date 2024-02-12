from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.utils import timezone
from django.shortcuts import redirect

from interactions.forms import RateForm
from interactions.models import Like, Rate

from .forms import RecipeForm
from .models import Ingredient, Recipe


class RecipeListView(ListView):
    model = Recipe
    ordering = "-created_at"
    context_object_name = "recipes"
    template_name = "recipes.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.annotate(
            recipe_count=Count("recipe")
        ).order_by("-recipe_count")[:5]
        return context


@method_decorator(login_required, name="dispatch")
class ShareView(CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy("home")
    template_name = "share.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "edit_recipe.html"
    pk_url_kwarg = "recipe_pk"
    context_object_name = "recipe"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.updated_at = timezone.now()
        recipe.save()
        form.save_m2m()
        return redirect("detail", recipe_pk=recipe.pk)


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    pk_url_kwarg = "recipe_pk"
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rate_form"] = RateForm
        if self.request.user.is_authenticated:
            context["is_liked"] = Like.objects.filter(
                recipe=context["recipe"], user=self.request.user
            )
            context["is_rated"] = Rate.objects.filter(
                recipe=context["recipe"], user=self.request.user
            )
        else:
            context["is_liked"] = False
            context["is_rated"] = False
        return context


class ListByIngredientView(RecipeListView):
    context_object_name = "recipes"
    template_name = "recipes.html"

    def get_queryset(self):
        return (
            Ingredient.objects.get(pk=self.kwargs["ingredient_pk"])
            .recipe_set.all()
            .order_by("-created_at")
        )


class SearchView(RecipeListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            # NOTE: description can be useful too
            search = search.replace(",", " ").split()  # parse search string
            query = Q()
            # Search all keywords in both recipe name and recipe ingredients
            for keyword in search:
                query |= Q(name__icontains=keyword)
                query |= Q(ingredients__name__icontains=keyword)
            obj_list = (
                self.model.objects.filter(query).order_by("-created_at").distinct()
            )
        else:
            obj_list = self.model.objects.all().order_by("-created_at")
        return obj_list
