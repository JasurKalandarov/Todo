from django.db import models
from django.db.models import Manager
from django.db.models import TextField, DateTimeField

from task.managers import TaskTodotManager, TaskDoneManager, TaskDeletedManager, TaskDoneDeletedManager


class Task(models.Model):
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"

    title = models.CharField(max_length=128,
                             verbose_name="Заголовок", )

    description = TextField(verbose_name="Описание:", )
    is_delete = models.BooleanField(default=False, verbose_name="Удалено")
    is_done = models.BooleanField(default=False, verbose_name="Выполнено")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # managers  # Task.objects.all()
    objects = Manager()  # Task.objects.all()
    todo = TaskTodotManager()  # Task.todo.all()
    done = TaskDoneManager()  # Task.done.all()
    delete = TaskDeletedManager()  # Task.delete.all()
    done_delete = TaskDoneDeletedManager()  # Task.done_delete.all()

    def __str__(self):
        return self.title

    @property
    def status(self):
        code = "DONE & DELETE" if self.is_done and self.is_delete else "DONE" if self.is_done else "DELETE" if self.is_delete else "TODO"
        return code

    @property
    def css_class(self):
        cls = "dark" if self.is_done and self.is_delete else "success" if self.is_done else "danger" if self.is_delete else "warning"
        return cls

# Ismingizni kiriting* blank = False > Majburiy
# Ismingizni kiriting  blank = True > Ixtiyoriy
# Boshlik, Null
# Unique - yagonalik (misol uchun email, telefon raqam)
# Verbose_name = "", adminkada nom berish
# help_text = "", Verbose_name ning tegidagi yordamchi so'zlar
