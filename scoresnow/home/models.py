from tabnanny import verbose
from django.db import models
from tinymce.models import HTMLField
from wagtail.core.fields import RichTextField

from wagtail.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

class HomePage(Page):
    templates = "home/home_page.html"
    max_count=1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = HTMLField()                   #models.CharField(max_length=1000, blank=False, null=True)
    # content = HTMLField()
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",

    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("banner_cta"),
    ]

# def something(self):
    #     return self.banner_title
