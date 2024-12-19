
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_application_cover_letter_application_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='externalinternship',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='externalinternship',
            name='external_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='externalinternship',
            name='source',
            field=models.CharField(default='manual', max_length=100),
        ),
        migrations.AddField(
            model_name='externalinternship',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('REVIEWING', 'Reviewing'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer', 'reviewed')},
        ),
        migrations.AddIndex(
            model_name='externalinternship',
            index=models.Index(fields=['external_id'], name='jobs_extern_externa_374b30_idx'),
        ),
        migrations.AddIndex(
            model_name='externalinternship',
            index=models.Index(fields=['is_active', '-created_at'], name='jobs_extern_is_acti_a71713_idx'),
        ),
    ]
