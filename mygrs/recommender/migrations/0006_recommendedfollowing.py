# Generated by Django 3.0.2 on 2020-11-21 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_recommendedreposfollowing_recommendedrepossimilarity'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommendedfollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('followee', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=100)),
                ('similar', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'FollowingRecommend',
            },
        ),
    ]
