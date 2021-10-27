"""about/models.py"""
from django.db import models
from django import forms
from django.shortcuts import render

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import CharBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from streams import blocks



class FormField(AbstractFormField):
    page = ParentalKey('About', related_name='custom_form_fields')


class About(AbstractEmailForm, Page):
    """code for About page"""
    template = "about/about_page.html"
    landing_page_template = "about/contact_page_landing.html"

    #max_count = 1

    our_mission = RichTextField(null=True, blank=True, help_text='Describe your mission')
    contact_section_title = RichTextField(blank=True)
    contact_subtitle = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)


    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [
        #FieldPanel("about_subtitle"),
        FieldPanel('our_mission'),
        FieldPanel('contact_section_title'),
        FieldPanel("contact_subtitle"),
        InlinePanel('custom_form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()
