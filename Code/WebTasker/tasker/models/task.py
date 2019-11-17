from django.db import models
from django.urls import reverse
from django.utils import timezone
from tasker.encryptors import task_slug_generate
from tasker.constants import TASK_STATUSES
from tasker.managers import TaskManager


class Task(models.Model):
    """Model class for working with tasks.

    Fields:
        title - Caption of Task;
        slug - Short link to refer to a specific object;
        description - Description of task;
        project - Reference to the project host;
        status - Status of the current task. Settings in "/constants.py", TASK_STATUSES;
        developer - Reference to the executing developer;
        date_create - Date of creating task;
        date_completion - Date of ending due task;

    """
    title = models.CharField(max_length=32, unique=True)
    slug = models.CharField(max_length=32)
    description = models.TextField()
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE, related_name='tasks')
    status = models.PositiveSmallIntegerField(default=0)
    developer = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='tasks')
    date_create = models.DateTimeField(default=timezone.now)
    date_completion = models.DateTimeField(blank=True, null=True)

    objects = TaskManager

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Task, self).save(force_insert, force_update, using, update_fields)
        self.slug = task_slug_generate(self.title)
        super(Task, self).save()

    def mark_completed(self):
        if self.status == TASK_STATUSES['Complete']:
            self.status = TASK_STATUSES['Default']
        else:
            self.status = TASK_STATUSES['Complete']
        self.save()

    def mark_canceled(self):
        if self.status == TASK_STATUSES['Canceled']:
            self.status = TASK_STATUSES['Default']
        else:
            self.status = TASK_STATUSES['Canceled']
        self.save()

    def task_status(self):
        """Get string version of task status"""
        for i, j in TASK_STATUSES.items():
            if self.status == j:
                return i
        return TASK_STATUSES[0]

    def get_absolute_url(self):
        return reverse('task_details_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_task', kwargs={'slug': self.slug})
