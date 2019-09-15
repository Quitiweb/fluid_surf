# Generated by Django 2.1.9 on 2019-08-08 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='propuestacomercial',
            name='emisor',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='propuestacomercial',
            name='receptor',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='promocion',
            name='articulos_compra',
            field=models.ManyToManyField(blank=True, related_name='requeridos', to='landing.Articulo'),
        ),
        migrations.AddField(
            model_name='promocion',
            name='articulos_obtiene',
            field=models.ManyToManyField(related_name='promocionados', to='landing.Articulo'),
        ),
        migrations.AddField(
            model_name='promocion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promociones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='marca',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marca', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='maestro',
            name='estilo',
            field=models.ManyToManyField(blank=True, to='landing.EstiloVida'),
        ),
        migrations.AddField(
            model_name='maestro',
            name='mercado',
            field=models.ManyToManyField(blank=True, to='landing.Mercado'),
        ),
        migrations.AddField(
            model_name='maestro',
            name='target',
            field=models.ManyToManyField(blank=True, to='landing.Target'),
        ),
        migrations.AddField(
            model_name='maestro',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='galeriaarticulo',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.Articulo'),
        ),
        migrations.AddField(
            model_name='espacio',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espacio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='definicionvariante',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variantes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conexion',
            name='emisor',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emisor_conexion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conexion',
            name='receptor',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receptor_conexion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coleccion',
            name='articulos',
            field=models.ManyToManyField(related_name='articulos', to='landing.Articulo'),
        ),
        migrations.AddField(
            model_name='coleccion',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colecciones', to='users.Empresa'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='categoria_padre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='landing.Categoria'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='articulo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='en_carrito', to='landing.Articulo'),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='variante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='en_carrito', to='landing.VarianteArticulo'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='items',
            field=models.ManyToManyField(related_name='articulos_carrito', to='landing.CarritoItem'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='promocion_asociada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promocion_carrito', to='landing.Promocion'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrito', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulo',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artcategorias', to='landing.Categoria'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='mercado',
            field=models.ManyToManyField(blank=True, to='landing.Mercado'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='subcategoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artsubcategorias', to='landing.Categoria'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='target',
            field=models.ManyToManyField(blank=True, to='landing.Target'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulo',
            name='variantes',
            field=models.ManyToManyField(blank=True, to='landing.DefinicionVariante'),
        ),
        migrations.AddField(
            model_name='alquiler',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Empresa'),
        ),
        migrations.AlterUniqueTogether(
            name='variantearticulo',
            unique_together={('opcion_1', 'opcion_1_value', 'opcion_2', 'opcion_2_value', 'opcion_3', 'opcion_3_value', 'articulo')},
        ),
    ]
