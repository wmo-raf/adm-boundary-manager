import json

from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from shapely import geometry, unary_union
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Orderable

from adminboundarymanager.countries import get_country_info


class AdminBoundary(models.Model):
    name_0 = models.CharField(max_length=100, blank=True, null=True)
    name_1 = models.CharField(max_length=100, blank=True, null=True)
    name_2 = models.CharField(max_length=100, blank=True, null=True)
    name_3 = models.CharField(max_length=100, blank=True, null=True)
    name_4 = models.CharField(max_length=100, blank=True, null=True)
    gid_0 = models.CharField(max_length=100, blank=True, null=True)
    gid_1 = models.CharField(max_length=100, blank=True, null=True)
    gid_2 = models.CharField(max_length=100, blank=True, null=True)
    gid_3 = models.CharField(max_length=100, blank=True, null=True)
    gid_4 = models.CharField(max_length=100, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)

    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = _("Administrative Boundaries")

    def __str__(self):
        level = self.level

        if level == 0:
            return f"Level {level} - {self.name_0}"

        if level == 1:
            return f"Level {level} - {self.name_1}"

        if level == 2:
            return f"Level {level} - {self.name_2}"

        if level == 3:
            return f"Level {level} - {self.name_3}"

        return f"Level {level} - {self.pk}"

    @property
    def bbox(self):
        min_x, min_y, max_x, max_y = self.geom.envelope.extent
        bbox = [min_x, min_y, max_x, max_y]
        return bbox

    @property
    def info(self):
        info = {"iso": self.gid_0}

        if self.level == 0:
            info.update({"name": self.name_0})

        if self.level == 1:
            gid_1 = self.gid_1.split(".")[1].split("_")[0]
            info.update({"id1": gid_1, "name": self.name_1})

        if self.level == 2:
            gid_1 = self.gid_1.split(".")[1].split("_")[0]
            gid_2 = self.gid_1.split(".")[1].split("_")[1]
            info.update({"id1": gid_1, "id2": gid_2, "name": self.name_2})

        return info


@register_setting
class AdminBoundarySettings(BaseSiteSetting, ClusterableModel):
    BOUNDARY_TYPE_CHOICES = []

    panels = [
        InlinePanel("countries", heading=_("Countries"), label=_("Country")),
    ]

    @cached_property
    def countries_list(self):
        countries = []
        for country in self.countries.all():
            countries.append({
                "name": country.country.name,
                "code": country.country.code,
                "alpha3": country.country.alpha3,
                **country.country_info
            })

        return countries

    @cached_property
    def combined_countries_bounds(self):
        polygons = []
        for country in self.countries_list:
            if country.get("bbox"):
                bbox = country.get("bbox")
                polygon = geometry.box(*bbox, ccw=True)
                polygons.append(polygon)

        combined_polygon = unary_union(polygons)
        return list(combined_polygon.bounds)

    @cached_property
    def boundary_tiles_url(self):
        return reverse("admin_boundary_tiles", args=[0, 0, 0]).replace("/0/0/0", r"/{z}/{x}/{y}")


class Countries(Orderable):
    parent = ParentalKey(AdminBoundarySettings, on_delete=models.CASCADE, related_name='countries')
    country = CountryField(blank_label=_("Select Country"), verbose_name=_("country"))

    panels = [
        FieldPanel("country", widget=CountrySelectWidget()),
    ]

    @cached_property
    def country_info(self):
        country_info = get_country_info(self.country.alpha3)
        return country_info

    @cached_property
    def country_info_str(self):
        country_info = get_country_info(self.country.alpha3)
        if country_info:
            return json.dumps(country_info)
        return {}
