from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from interactions.models import Like, Rate
from recipes.models import Recipe


@method_decorator(login_required, name="dispatch")
class LikeView(View):
    def get(self, request, recipe_pk):
        return redirect("detail", recipe_pk=recipe_pk)

    def post(self, request, recipe_pk):
        like, created = Like.objects.get_or_create(
            recipe=Recipe.objects.get(pk=recipe_pk), user=request.user
        )
        if not created:
            Like.objects.get(pk=like.pk).delete()
        return redirect("detail", recipe_pk=recipe_pk)


@method_decorator(login_required, name="dispatch")
class RateView(View):
    def get(self, request, recipe_pk):
        return redirect("detail", recipe_pk=recipe_pk)

    def post(self, request, recipe_pk):
        rate = Rate.objects.filter(
            recipe=Recipe.objects.get(pk=recipe_pk), user=request.user,
        ).first()

        if rate:
            rate.rate = request.POST.get("rate")
            rate.save()
        else:
            Rate.objects.create(
                recipe=Recipe.objects.get(pk=recipe_pk),
                user=request.user,
                rate=request.POST.get("rate"),
            )
        return redirect("detail", recipe_pk=recipe_pk)
