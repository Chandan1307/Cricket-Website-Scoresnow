from statistics import mode
from turtle import title
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalManyToManyField

from scoresnow.teams.models import TeamsPage

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from scoresnow.base.blocks import BaseStreamBlock


@register_snippet
class Country(models.Model):
    """
    A Django model to store set of countries of origin.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/series/country/) In the SeriesPage
    model you'll see we use a ForeignKey to create the relationship between
    Country and SeriesPage. This allows a single relationship (e.g only one
    Country can be added) that is one-way (e.g. Country will have no way to
    access related SeriesPage objects).
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Countries of Origin"



@register_snippet
class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



@register_snippet
class SeriesIngredient(models.Model):
    """
    Standard Django model that is displayed as a snippet within the admin due
    to the `@register_snippet` decorator. We use a new piece of functionality
    available to Wagtail called the ParentalManyToManyField on the SeriesPage
    model to display this. The Wagtail Docs give a slightly more detailed example
    https://docs.wagtail.org/en/stable/getting_started/tutorial.html#categories
    """

    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Series ingredients"


@register_snippet
class SeriesType(models.Model):
    """
    A Django model to define the series type
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI. In the SeriesPage model you'll see we use a ForeignKey
    to create the relationship between SeriesType and SeriesPage. This allows a
    single relationship (e.g only one SeriesType can be added) that is one-way
    (e.g. SeriesType will have no way to access related SeriesPage objects)
    """

    title = models.CharField(max_length=255)

    panels = [
        FieldPanel("title"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Series types"


class SeriesPage(Page):
    """
    Detail view for a specific series
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    origin = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # We include related_name='+' to avoid name collisions on relationships.
    # e.g. there are two FooPage models in two different apps,
    # and they both have a FK to series_type, they'll both try to create a
    # relationship called `foopage_objects` that will throw a valueError on
    # collision.
    series_type = models.ForeignKey(
        "series.SeriesType",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    ingredients = ParentalManyToManyField("SeriesIngredient", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("origin"),
        FieldPanel("series_type"),
        MultiFieldPanel(
            [
                FieldPanel(
                    "ingredients",
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Additional Metadata",
            classname="collapsible collapsed",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    parent_page_types = ["SeriesIndexPage"]


class SeriesIndexPage(Page):
    """
    Index page for series.

    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction", classname="full"),
        FieldPanel("image"),
    ]

    # Can only have SeriesPage children
    subpage_types = ["SeriesPage"]

    # Returns a queryset of SeriesPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_series(self):
        return (
            SeriesPage.objects.live().descendant_of(self).order_by("-first_published_at")
        )

    # Allows child objects (e.g. SeriesPage objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_series(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request):
        context = super(SeriesIndexPage, self).get_context(request)

        # SeriesPage objects (get_series) are passed through pagination
        series = self.paginate(request, self.get_series())

        context["series"] = series

        return context


class Stadium(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Which city it belongs to."
    )
    capacity = models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Stadium"


class MatchStatus(object):
    NOT_STARTED = 0
    IN_PLAY = 1
    FINISHED = 2
    ABANDONED = 3


class Match(models.Model):
    
    MATCHSTATUS_CHOICES = (
        (MatchStatus.NOT_STARTED, 'Not Started'),
        (MatchStatus.IN_PLAY, 'In Play'),
        (MatchStatus.FINISHED, 'Finished'),
        (MatchStatus.ABANDONED, 'Abandoned'),
    )

    title = models.CharField(max_length=255)
    key = models.CharField(max_length=255, blank=True, null=True)
    series = models.ForeignKey(
        SeriesPage,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Which series it belongs to."
    )
    team_1 = models.ForeignKey(
        TeamsPage,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Team 1 of the match."
    )
    
    team_2 = models.ForeignKey(
        TeamsPage,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        help_text="Team 2 of the match."
    )
    data_feed = models.TextField(blank=True, null=True)
    stadium = models.ForeignKey(Stadium, blank=True, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(blank=True, null=True, max_length=255)
    status = models.PositiveSmallIntegerField(choices=MATCHSTATUS_CHOICES, default=MatchStatus.NOT_STARTED)


    def __str__(self):
        return self.title



# Videos. ----> Blog.

# # New Models
# - Stadiums 
# - Cities
# - Country

# Series:- 
# > Teams

# >> LOW Priority
# - Players
# - Accounts


# API to store data in data_feed.
# Display scoreboard.
# Match Page.


