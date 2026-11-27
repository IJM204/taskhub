from django.db import migrations


def forwards(apps, schema_editor):
    Task = apps.get_model("core", "Task")

    for task in Task.objects.all().iterator():
        task.title_normalized = task.title.strip().lower()
        task.save(update_fields=["title_normalized"])


def backwards(apps, schema_editor):
    Task = apps.get_model("core", "Task")

    Task.objects.all().update(title_normalized=None)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_task_title_normalized"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
