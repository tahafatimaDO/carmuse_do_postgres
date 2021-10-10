from django.db import models
#from django_extensions.db.fields import AutoSlugField
from django import forms
from django.shortcuts import render
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.core.blocks import CharBlock, RichTextBlock, BooleanBlock, DateBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from wagtail.embeds.blocks import EmbedBlock


class PaintersPage(Page):

    template = "catalog/painting_index_page.html"

    subtitle = RichTextField(
        features=['h6', 'h5', 'bold', 'italic'],
        max_length=250,
        blank=True,
        null=True,
        help_text='Catchy, short informative description of the page'
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def serve(self, request):
        """Custom serve method"""
        painter_list = PainterPage.objects.live().order_by('first_name')
        return render(request, 'painters/painters_index.html', {
            'page': self,
            'painter_list': painter_list
        })



class PainterPage(Page):

    template = "painter/painter_page.html"

    parent_page_types = ["painter.PaintersPage"]

    painter_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    artist_names = StreamField([
        ('names', blocks.NameBlock()),
    ])
    artist_dates = StreamField([
        ('dates', blocks.DateBlock()),
    ])
    #artist_links = StreamField([
     #    ('links', blocks.CTABlock()),
    #])
    bio = RichTextField(null=True, features=["bold", "italic"])
    pitch = RichTextField(null=True, features=["bold", "italic"])
    links = StreamField([
         ('link', blocks.ButtonBlock(null=True, blanc=True)),
    ])


    content_panels = Page.content_panels + [
        ImageChooserPanel('painter_image'),
        StreamFieldPanel('artist_names'),
        #StreamFieldPanel('artist_dates'),
        FieldPanel('bio'),
        FieldPanel('pitch'),
        #StreamFieldPanel('artist_links'),
        StreamFieldPanel('links'),
        #InlinePanel('painter_links', label="link"),
    ]
