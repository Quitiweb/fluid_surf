from django.http import HttpResponse
from django.template import loader
from django.views.generic import DetailView
from django.utils import timezone

from . import models


class Single(DetailView):
    model = models.Post
    template_name = 'noticias/single.html'


def noticias(request):
    post_list = models.Post.objects.filter(
        fecha_de_publicacion__lte=timezone.now()
    ).order_by('-fecha_de_publicacion')

    random_list = models.Post.objects.order_by('?')[:4]
    random_mini_list = models.Post.objects.order_by('?')[:4]

    template = loader.get_template('noticias/noticias.html')

    context = {
        'post_list': post_list,
        'random_list': random_list,
        'random_mini_list': random_mini_list,
    }

    return HttpResponse(template.render(context, request))
