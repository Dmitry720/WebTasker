from django.db import models
from django.urls import reverse
from django.utils import timezone
from tasker.encryptors import project_slug_generate
from tasker.managers import ProjectManager


class Project(models.Model):
    """Model class for work with projects.

    Fields:
        title - Caption of project;
        slug - Short link to refer to a specific object;
        description - Description of project;
        manager - Reference to the manager of project;
        date_create - Date of creating project;
    """
    title = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    manager = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='manage_projects')
    date_create = models.DateTimeField(default=timezone.now)

    objects = ProjectManager

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Project, self).save(force_insert, force_update, using, update_fields)
        self.slug = project_slug_generate(self.title)
        super(Project, self).save()

    def get_absolute_url(self):
        return reverse('project_details_url', kwargs={'slug': self.slug})

    def get_delete_link(self):
        return reverse('delete_project', kwargs={'slug': self.slug})
