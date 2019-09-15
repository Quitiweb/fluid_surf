from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

TITLE = 100
TEXT = 15000
URL = 1000


class Post(models.Model):

    view_on_site = False

    titulo = models.CharField(max_length=TITLE, default='Titulo del Post')

    slug = models.SlugField(
        _('slug'), max_length=255,
        unique_for_date='fecha_de_publicacion',
        default='titulo-del-post',
        help_text=_("Se auto-rellena al escribir el Título")
    )

    subtitulo = models.CharField(max_length=TITLE, default='Subtitulo del Post')
    imagen_principal = models.ImageField(upload_to='img/post/')

    introduccion = HTMLField(
        max_length=TEXT,
        default='Escribe aquí el texto de la introducción...',
        help_text=_('La intro se muestra en la página principal de las Noticas')
    )

    texto_1 = HTMLField(max_length=TEXT, default='Escribe aquí la primera parte del post...')
    imagen_1 = models.ImageField(upload_to='img/post/', default='', blank=True)
    texto_2 = HTMLField(max_length=TEXT, default='', blank=True)
    imagen_2 = models.ImageField(upload_to='img/post/', default='', blank=True)
    texto_3 = HTMLField(max_length=TEXT, default='', blank=True)

    url_video_final = models.CharField(max_length=URL, default='', blank=True)

    fecha_de_publicacion = models.DateTimeField(
        _('Fecha de publicacion'),
        db_index=True, default=timezone.now,
    )

    def __str__(self):
        return self.fecha_de_publicacion.strftime('%Y-%m-%d') + " - " + self.titulo

    def get_absolute_url(self):
        """
        Builds and returns the entry's URL based on
        the slug and the creation date.
        """
        publication_date = self.fecha_de_publicacion
        if timezone.is_aware(publication_date):
            publication_date = timezone.localtime(publication_date)
        return reverse('noticias:single', kwargs={
            'year': publication_date.strftime('%Y'),
            'month': publication_date.strftime('%m'),
            'day': publication_date.strftime('%d'),
            'slug': self.slug})

    def get_url(self):
        pub_date = self.fecha_de_publicacion
        return pub_date.strftime('%Y') + '/' + pub_date.strftime('%m') + '/' + pub_date.strftime('%d') + '/' + self.slug

    def get_video_url(self):
        """
        Si el link del video de YouTube está copy+pasted
        directamente sin el código, cogemos sólo dicho código final.
        :return: el código del vídeo
        """
        url_video = self.url_video_final
        if "watch" in url_video:
            return url_video.split("watch?v=", 1)[1]
        return url_video
