from django.db.models import Manager, Q
from django.shortcuts import get_object_or_404


class CustomProjectManager(Manager):
    def search(self, query):
        qs = self.get_queryset().all()
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

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)

    def safe_get(self, *args, **kwargs):
        try:
            self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


ProjectManager = CustomProjectManager()
