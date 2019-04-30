# Generated by Django 2.2 on 2019-04-29 03:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_articlepost_total_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30)),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 4, 29, 3, 23, 11, 668122, tzinfo=utc))),
            ],
        ),
        migrations.AddField(
            model_name='articlepost',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='article.ArticleColumn'),
        ),
    ]