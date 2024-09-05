from django.db.models.manager import Manager


# DEFAULT
class TaskTodotManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=False, is_delete=False)


# DONE
class TaskDoneManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=True, is_delete=False)


# DELETED
class TaskDeletedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=False, is_delete=True)


# DONE & DELETE
class TaskDoneDeletedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_done=True, is_delete=True)
