"""catalog/models.py"""
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django import forms
from django.shortcuts import render
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, BooleanBlock, DateBlock, StructBlock, ChoiceBlock
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


from streams import blocks

# ATTRIBUTES

# CATEGORY
class PaintingPagePaintingCategory(models.Model):
    page = ParentalKey(
        "catalog.PaintingDetailPage", on_delete=models.CASCADE, related_name="categories"
    )
    painting_category = models.ForeignKey(
        "catalog.PaintingCategory", on_delete=models.CASCADE, related_name="post_pages"
    )

    panels = [
        SnippetChooserPanel("painting_category"),
    ]

    class Meta:
        unique_together = ("page", "painting_category")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['painting_index_page'] = self.get_parent().specific
        return context



class PaintingCategory(models.Model):
    """Painting catgory for a snippet."""

    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="name",
        editable=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Painting Category"
        verbose_name_plural = "Painting Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
register_snippet(PaintingCategory)


# Location
class PaintingLocation(models.Model):
    """Painting location for a snippet."""

    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="name",
        editable=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Painting Location"
        verbose_name_plural = "Painting Locations"
        ordering = ["name"]

    def __str__(self):
        return self.name
register_snippet(PaintingLocation)



# Paintings Section

class PaintingIndexPage(RoutablePageMixin, Page):
    """Listing page lists all the Detail Pages(paintings)"""

    template = "catalog/painting_index_page.html"
    max_count = 1

    subtitle = RichTextField(
        features=['h6', 'h5', 'bold', 'italic'],
        max_length=250,
        blank=True,
        null=True,
        help_text='Catchy, short informative description of the page'
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(PaintingIndexPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['painting_index_page'] = self
        return context

    def get_posts(self):
        return PaintingDetailPage.objects.descendant_of(self).live()

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^location/(?P<location>[-\w]+)/$')
    def post_by_location(self, request, location, *args, **kwargs):
        self.search_type = 'location'
        self.search_term = location
        self.posts = self.get_posts().filter(locations__slug=location)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^medium/(?P<medium>[-\w]+)/$')
    def post_by_medium(self, request, medium, *args, **kwargs):
        self.search_type = 'medium'
        self.search_term = medium
        self.posts = self.get_posts().filter(mediums__slug=medium)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^support/(?P<support>[-\w]+)/$')
    def post_by_support(self, request, support, *args, **kwargs):
        self.search_type = 'support'
        self.search_term = support
        self.posts = self.get_posts().filter(supports__slug=support)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^painter/(?P<painter>[-\w]+)/$')
    def post_by_painter(self, request, painter, *args, **kwargs):
        self.search_type = 'painter'
        self.search_term = painter
        self.posts = self.get_posts().filter(painters__slug=painter)
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


class PaintingDetailPage(Page):
    """Painting page"""

    template = "catalog/painting_detail_page.html"

    #parent_page_types = ["catalog.PaintingIndexPage"]

    MOTIF_TYPES = (
        ('ge', 'Genre painting (everyday life)'),
        ('por', 'Portrait'),
        ('apa', 'Autoportrait'),
        ('la', 'Landscape'),
        ('nm', 'Still life'),
        ('ot', 'Other'),
    )

    painter = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    date = models.DateField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    motif = ChoiceBlock(choices=MOTIF_TYPES, help_text='The subject-matter')
    tags = ClusterTaggableManager(through="catalog.PaintingPageTag", blank=True)
    #categories = ParentalManyToManyField("catalog.PaintingCategory", blank=True)
    locations = ParentalManyToManyField("catalog.PaintingLocation", blank=True)
    mediums = ParentalManyToManyField("catalog.PaintingMedium", blank=True)
    supports = ParentalManyToManyField("catalog.PaintingSupport", blank=True)
    description = StreamField(
        [
            ("simple_richtext", blocks.SimpleRichtextBlock()),
        ],
        null=True,
        blank=True,
    )

    links = StreamField([
        ('links', blocks.ButtonBlock(null=True, blank=True)),
    ], null=True, blank=True)

    initial_inventory = StreamField([
        ('dbreference', CharBlock(max_length=50, null=True, blank=True,
                                         help_text="Entry from initial Excel Inventory by JMC, for internal needs only", default='a')),

        ('remark', CharBlock(max_length=150, null=True, blank=True,
                                  help_text="Entry from initial Excel Inventory by JMC, for internal needs only", default='a')),
        ('signature', BooleanBlock(null=True, blank=True, detault='Yes')),
    ], null=True, blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,)

    content_panels = Page.content_panels + [
        ImageChooserPanel("image"),

        PageChooserPanel('painter'),    # ('painter', 'painter.PainterPage'),
        StreamFieldPanel("description"),
        FieldPanel('date'),
        MultiFieldPanel(
            [
                FieldPanel("width"),
                FieldPanel("height")
            ],
            heading="Dimensions",
            classname="collapsible collapsed",
        ),


        # MultiFieldPanel(
        #    [StreamFieldPanel('technical_details')]
        # ),
        FieldPanel("tags"),
        InlinePanel("categories", label="category"),

        # MultiFieldPanel(
        #     [
        #         FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        #     ],
        #     heading="Categories",
        #     classname="collapsible collapsed",
        # ),

        MultiFieldPanel([
            FieldPanel('locations', widget=forms.CheckboxSelectMultiple),
        ],
            heading="Location",
            classname="collapsible collapsed",
        ),

        MultiFieldPanel([
            FieldPanel('mediums', widget=forms.CheckboxSelectMultiple),
        ],
            heading="Medium",
            classname="collapsible collapsed",
        ),

        MultiFieldPanel([
            FieldPanel('supports', widget=forms.CheckboxSelectMultiple),
        ],
            heading="Support",
            classname="collapsible collapsed",
        ),
        StreamFieldPanel('links'),
        StreamFieldPanel('initial_inventory'),

    ]

    @property
    def painting_index_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PaintingDetailPage, self).get_context(request, *args, **kwargs)
        context['painting_index_page'] = self.painting_index_page
        context['post'] = self
        return context



# TAGS
class PaintingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PaintingDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )





# SUPPORT
@register_snippet
class PaintingSupport(models.Model):
    """Painting support for a snippet."""

    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="name",
        editable=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Paining Support"
        verbose_name_plural = "Painting Supports"
        ordering = ["name"]

    def __str__(self):
        return self.name


# Medium
@register_snippet
class PaintingMedium(models.Model):
    """Painting medium for a snippet."""

    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="name",
        editable=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Paining Medium"
        verbose_name_plural = "Painting Mediums"
        ordering = ["name"]

    def __str__(self):
        return self.name
