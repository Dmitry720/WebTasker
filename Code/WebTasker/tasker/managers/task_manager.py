from django.db.models import Manager, Q
from django.shortcuts import get_object_or_404


class CustomTaskManager(Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def search(self, query):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(description__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def delete_with_slug(self, slug):
        try:
            self.get_queryset().get(slug__iexact=slug.lower()).delete()
            return True
        except self.model.DoesNotExist:
            return False

    def mark_completed(self, slug):
        try:
            self.get_queryset().get(slug__iexact=slug).mark_completed()
            return True
        except self.model.DoesNotExist:
            return False

    def mark_canceled(self, slug):
        try:
            self.get_queryset().get(slug__iexact=slug).mark_canceled()
            return True
        except self.model.DoesNotExist:
            return False

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)

    def safe_get(self, *args, **kwargs):
        try:
            self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


TaskManager = CustomTaskManager()
