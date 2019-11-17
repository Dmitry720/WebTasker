from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tasker.encryptors import user_slug_generate


class User(AbstractUser):
    """Model class for use by site users. Django authentication enabled.
    Username and password are required. Other fields are optional.

    Fields:
        first_name - First name user;
        last_name - Last name user;
        email - Mail of profile user;
        username - Unique username of profile user;
        password - Password of profile user. Saving in encrypted view;
        slug - Short reference to use in URL's;
        tasks - Foreign key. Get manager of all tasks of user;
        subtasks - Foreign key. Get manager of all subtasks of task of user;
        manage_projects - Foreign key. Get manager of all managing projects of user;
        is_stuff - Can profile login in admin panel;
        is_manager - Get access for managing projects;
        is_active - This profile has confirmed email or not;
        date_joined - Date of creating profile of user;
    """
    slug = models.CharField(_('slug'), max_length=150)
    password = models.CharField(_('password'), max_length=128)

    def __str__(self):
        return f"Developer {self.username}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(User, self).save(force_insert, force_update, using, update_fields)
        self.slug = user_slug_generate(self.username)
        super(User, self).save()

    def get_absolute_url(self):
        return reverse('profile_user_url', kwargs={'slug': self.username})

    def get_all_projects(self):
        return list(set([task.project for task in self.tasks.all()]))

    def get_all_tasks(self):
        return self.tasks

    def get_delete_link(self):
        return reverse('delete_user', kwargs={'slug': self.slug})
