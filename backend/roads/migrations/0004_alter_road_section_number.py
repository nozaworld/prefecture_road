from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0003_alter_road_prefecture_all_47'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='section_number',
            field=models.BigIntegerField(verbose_name='区間番号'),
        ),
    ]
