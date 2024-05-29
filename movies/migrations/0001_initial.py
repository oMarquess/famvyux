from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=4)),
                ('imdb_rating', models.CharField(max_length=4)),
                ('metascore', models.CharField(max_length=3)),
                ('image_url', models.URLField()),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
