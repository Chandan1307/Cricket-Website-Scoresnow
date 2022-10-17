from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from scoresnow.base.models import FooterText, People
from scoresnow.series.models import SeriesIngredient, SeriesType, Country

"""
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see https://thegrouchy.dev/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at https://fontawesome.com/icons .
"""


class SeriesIngredientAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = SeriesIngredient
    search_fields = ("name",)


class SeriesTypeAdmin(ModelAdmin):
    model = SeriesType
    search_fields = ("title",)


class SeriesCountryAdmin(ModelAdmin):
    model = Country
    search_fields = ("title",)


class SeriesModelAdminGroup(ModelAdminGroup):
    menu_label = "Series Categories"
    menu_icon = "fa-suitcase"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (SeriesIngredientAdmin, SeriesTypeAdmin, SeriesCountryAdmin)


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = "People"  # ditch this to use verbose_name_plural from model
    menu_icon = "fa-users"  # change as required
    list_display = ("first_name", "last_name", "job_title", "thumb_image")
    list_filter = ("job_title",)
    search_fields = ("first_name", "last_name", "job_title")
    inspect_view_enabled = True


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ("body",)


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = "Bakery Misc"
    menu_icon = "fa-cutlery"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(SeriesModelAdminGroup)
modeladmin_register(BakeryModelAdminGroup)
