"""flexible page"""
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from streams import blocks
from wagtail.core.blocks import StructBlock #blocks as streamfield_blocks
from wagtail_blocks.blocks import ListBlock, HeaderBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock, ChartBlock, MapBlock, ImageSliderBlock
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel
)


class FormField(AbstractFormField):
    page = ParentalKey(
        'FlexPage',
        on_delete=models.CASCADE,
        related_name='custom_form_fields',
    )


class FlexPage(AbstractEmailForm, Page):
    """flexible page class"""
    template = "flex/flex_page.html"

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            #("full_richtext", blocks.RichTextBlock()),
            #("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)
    body = StreamField([
        ('header', HeaderBlock()),
        ('list', ListBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('cropped_images_with_text', CroppedImagesWithTextBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
        ('chart', ChartBlock()),
        ('map', MapBlock()),
        ('image_slider', ImageSliderBlock()),
    ], blank=True)

    ## form
    # form = StreamField([
    #     ('description', models.CharField(max_length=255, blank=True)),
    #     ('thank_you_text', RichTextField(blank=True)),
    # ],
    #     template = "contact/contact_page.html",
    #     landing_page_template = "contact/contact_page_landing.html"
    # )

    #
    description = models.CharField(max_length=255, blank=True, )
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [
        FieldPanel('description', classname="full"),
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ],
        heading="Email Notification Config",
        #template="contact/contact_page.html",
        ),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()


    class Meta: # noga
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"



