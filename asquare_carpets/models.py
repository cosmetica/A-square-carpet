from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks as wagtail_blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey

from . import blocks as site_blocks

# ---------- Settings ----------
@register_setting
class CompanySettings(BaseSiteSetting):
    brand_name = models.CharField(max_length=120, default="A‑Square Carpets")
    tagline = models.CharField(max_length=250, blank=True, default="Exhibition & Commercial Flooring, Done Fast.")
    email = models.EmailField(blank=True, default="hello@asquarecarpets.com")
    phone = models.CharField(max_length=50, blank=True, default="+66 0000 0000")
    address = models.CharField(max_length=255, blank=True, default="Bangkok, Thailand")
    line_id = models.CharField(max_length=100, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    panels = [
        FieldPanel("brand_name"),
        FieldPanel("tagline"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("address"),
        FieldPanel("line_id"),
        FieldPanel("facebook"),
        FieldPanel("instagram"),
    ]

# ---------- Home ----------
class HomePage(Page):
    template = "asquare_carpets/home_page.html"

    hero_title = models.CharField(max_length=180, default="Flooring that makes events effortless.")
    hero_text = models.TextField(blank=True, default="From mega‑expos to retail fit‑outs, we supply & install quality carpets, vinyl and grass—on time, every time.")
    hero_ctas = StreamField([("button", site_blocks.CTAButton())], blank=True, use_json_field=True)

    stats = StreamField([("stat", site_blocks.StatBlock())], blank=True, use_json_field=True)

    services_intro = RichTextField(blank=True, features=["bold","italic","link","ol","ul"])
    featured_services = StreamField([("pages", site_blocks.PageListBlock())], blank=True, use_json_field=True)

    products_intro = RichTextField(blank=True, features=["bold","italic","link","ol","ul"])
    featured_products = StreamField([("pages", site_blocks.PageListBlock())], blank=True, use_json_field=True)

    gallery_intro = RichTextField(blank=True, features=["bold","italic","link","ol","ul"])
    gallery_images = StreamField([("image", site_blocks.GalleryImageBlock())], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_text"),
        FieldPanel("hero_ctas"),
        FieldPanel("stats"),
        FieldPanel("services_intro"),
        FieldPanel("featured_services"),
        FieldPanel("products_intro"),
        FieldPanel("featured_products"),
        FieldPanel("gallery_intro"),
        FieldPanel("gallery_images"),
    ]

# ---------- Services ----------
class ServicesIndexPage(Page):
    template = "asquare_carpets/services_index_page.html"
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("intro")]

class ServicePage(Page):
    template = "asquare_carpets/service_page.html"
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text="Optional emoji or icon, e.g., 🧰")
    content_panels = Page.content_panels + [FieldPanel("icon"), FieldPanel("intro"), FieldPanel("body")]

# ---------- Products ----------
class ProductsIndexPage(Page):
    template = "asquare_carpets/product_index_page.html"
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("intro")]

class ProductPage(Page):
    template = "asquare_carpets/product_page.html"
    summary = models.TextField(blank=True)
    body = RichTextField(blank=True)
    swatches = StreamField([
        ("swatch", wagtail_blocks.StructBlock([
            ("name", wagtail_blocks.CharBlock()),
            ("image", ImageChooserBlock(required=False)),
        ]))
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("swatches")
    ]

# ---------- Gallery ----------
class GalleryIndexPage(Page):
    template = "asquare_carpets/gallery_index_page.html"
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

class GalleryImage(Orderable):
    page = ParentalKey(GalleryIndexPage, related_name="images", on_delete=models.CASCADE)
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=255, blank=True)

    panels = [FieldPanel("image"), FieldPanel("caption")]

# ---------- About ----------
class AboutPage(Page):
    template = "asquare_carpets/about_page.html"
    body = RichTextField(blank=True)
    highlights = StreamField([("card", site_blocks.CardBlock())], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel("body"), FieldPanel("highlights")]

# ---------- Contact (Form) ----------
class ContactFormField(AbstractFormField):
    page = ParentalKey("ContactPage", related_name="form_fields", on_delete=models.CASCADE)

class ContactPage(AbstractEmailForm):
    template = "asquare_carpets/contact_page.html"
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel([
            FieldPanel("to_address"),
            FieldPanel("from_address"),
            FieldPanel("subject"),
        ], heading="Email settings"),
        FieldPanel("thank_you_text"),
    ]
