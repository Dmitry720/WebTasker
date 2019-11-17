from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404


class CustomUserManager(BaseUserManager):
    def search(self, query):
        qs = self.model.objects.all()
        if query:
            or_lookup = (Q(username__icontains=query) | Q(first_name__icontains=query)
                         | Q(last_name__icontains=query) | Q(email__icontains=query))
            qs = qs.filter(or_lookup)
        return qs

    def delete_with_slug(self, slug):
        try:
            self.model.objects.get(slug__iexact=slug.lower()).delete()
            return True
        except self.model.DoesNotExist:
            return False

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)

    def safe_get(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def safe_delete(self, obj):
        if obj is None:
            return False
        if obj is QuerySet:
            for elem in obj:
                elem.safe_delete()
        else:
            obj.delete()
            return True
        return False


UserManager = CustomUserManager()
