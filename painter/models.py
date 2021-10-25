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


class PaintersPage(RoutablePageMixin, Page):

    template = "painter/painters_page.html"

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

    def get_context(self, request, *args, **kwargs):
        context = super(PaintersPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['painters_page'] = self
        return context

    def get_posts(self):
        return PainterPage.objects.descendant_of(self).live()

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)

    @route(r"^search/$")
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.posts = self.get_posts()
        if search_query:
            self.filter_term = search_query
            self.filter_type = 'search'
            self.posts = self.posts.search(search_query)
        return self.render(request)



class PainterPage(Page):

    template = "painter/painter_page.html"

    parent_page_types = ["painter.PaintersPage"]

    painter_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    artist_names = StreamField([
        ('names', blocks.NameBlock()),
    ])
    artist_dates = StreamField([
        ('dates', blocks.DateBlock()),
    ], blank=True, null=True)
    bio = RichTextField(null=True, blank=True, features=["bold", "italic"])
    pitch = RichTextField(null=True, blank=True, features=["bold", "italic"])
    links = StreamField([
         ('link', blocks.ButtonBlock()),
    ], blank=True, null=True)


    content_panels = Page.content_panels + [
        ImageChooserPanel('painter_image'),
        StreamFieldPanel('artist_names'),
        StreamFieldPanel('artist_dates'),
        FieldPanel('bio'),
        FieldPanel('pitch'),
        StreamFieldPanel('links'),
    ]
