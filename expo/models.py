from django.db import models
from django_extensions.db.fields import AutoSlugField
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.snippets.models import register_snippet

from wagtail.core import blocks as streamfield_blocks
# from streams import blocks

"""
1 create a list with page header and subtitle . 
2. add context for expo page. Pass to page only header, subtitle image and button. No cards
3. add carousel orderable and link to page.
4. check migrations. If work. display it on the current cards of the with bground whene the button is used for modal the carfousel
"""

# class ExpoPageExpoImages(Orderable):
#     """Between 1 and 9 images for the home page carousel."""
#     page = ParentalKey(ExpoPage, related_name="expo_images")
#     carousel_image = models.ForeignKey(
#         "wagtailimages.Image",
#         null=True,
#         blank=False,
#         on_delete=models.SET_NULL,
#         related_name="+",
#     )
#
#     carousel_caption = models.CharField(blank=True, max_length=1000)
#
#     panels = [
#         ImageChooserPanel("carousel_image"),
#         FieldPanel("carousel_caption"),
#     ]



class ExpoIndexPage(Page):

    subpage_types = ['expo.ExpoPage']

    template = "expo/expo_list_page.html"

    subtitle = RichTextField(features=["bold", "italic"])

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        expopages = ExpoPage.objects.live().public().order_by('-first_published_at')
        context['expopages'] = expopages
        return context


    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all expos
        all_expos = ExpoPage.objects.live().public().order_by('-first_published_at')
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_expos = all_expos.filter(tags__slug__in=[tags])
        # Paginate all posts by 3 per page
        paginator = Paginator(all_expos, 3)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            expos = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            expos = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            expos = paginator.page(paginator.num_pages)
        # "expos" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["expos"] = expos
        #context["tags"] = ExpoTags.objects.all()
        return context


class ExpoPage (RoutablePageMixin, Page):

    parent_page_types = ["expo.ExpoIndexPage"]

    template = "expo/expo_page.html"

    subtitle = RichTextField(max_length=500, null=True, blank=True, features=["bold", "italic"],
                                          help_text='Catchy, short informative description of the expo')

    button_text = models.CharField(null=False, blank=False, default='Learn More', max_length=50)

    tags = ClusterTaggableManager(through="expo.ExpoPageTag", blank=True)

    content_panels = Page.content_panels + [

        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("button_text"),
                FieldPanel("tags"),
            ],
            heading="Expo General Content",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [InlinePanel('gallery_images', label="Gallery Images",
                         help_text="max images are limited to 9, keep the sharp and catchy for the viewer")],
            heading="Gallery Images",
            classname="collapsible collapsed",
        ),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


class ExpoPageGalleryImage(Orderable):
    page = ParentalKey(ExpoPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class ExpoPageTag(TaggedItemBase):
    """tags"""
    content_object = ParentalKey("ExpoPage", related_name="expo_tags")