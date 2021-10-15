# Generated by Django 3.2.7 on 2021-10-15 11:03

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paintingpagepaintinglocation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintinglocation',
            name='page',
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintinglocation',
            name='painting_location',
        ),
        migrations.AlterUniqueTogether(
            name='paintingpagepaintingmedium',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintingmedium',
            name='page',
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintingmedium',
            name='painting_medium',
        ),
        migrations.AlterUniqueTogether(
            name='paintingpagepaintingsupport',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintingsupport',
            name='page',
        ),
        migrations.RemoveField(
            model_name='paintingpagepaintingsupport',
            name='painting_support',
        ),
        migrations.AddField(
            model_name='paintingdetailpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='catalog.PaintingCategory'),
        ),
        migrations.AddField(
            model_name='paintingdetailpage',
            name='locations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='catalog.PaintingLocation'),
        ),
        migrations.AddField(
            model_name='paintingdetailpage',
            name='mediums',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='catalog.PaintingMedium'),
        ),
        migrations.AddField(
            model_name='paintingdetailpage',
            name='supports',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='catalog.PaintingSupport'),
        ),
        migrations.DeleteModel(
            name='PaintingPagePaintingCategory',
        ),
        migrations.DeleteModel(
            name='PaintingPagePaintingLocation',
        ),
        migrations.DeleteModel(
            name='PaintingPagePaintingMedium',
        ),
        migrations.DeleteModel(
            name='PaintingPagePaintingSupport',
        ),
    ]
