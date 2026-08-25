from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='prefecture',
            field=models.CharField(
                choices=[
                    ('shizuoka', '静岡県'),
                    ('aichi', '愛知県'),
                    ('gifu', '岐阜県'),
                    ('mie', '三重県'),
                    ('nagano', '長野県'),
                    ('niigata', '新潟県'),
                    ('toyama', '富山県'),
                    ('ishikawa', '石川県'),
                    ('fukui', '福井県'),
                    ('yamanashi', '山梨県'),
                ],
                max_length=20,
                verbose_name='都道府県',
            ),
        ),
    ]
