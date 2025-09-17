from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class StatBlock(blocks.StructBlock):
    value = blocks.CharBlock(required=True, help_text="e.g., 10k+")
    label = blocks.CharBlock(required=True, help_text="e.g., sqm installed / month")

    class Meta:
        icon = "placeholder"
        label = "Stat"

class CTAButton(blocks.StructBlock):
    text = blocks.CharBlock()
    url = blocks.URLBlock(required=False)
    page = blocks.PageChooserBlock(required=False, help_text="Use URL or Page")
    style = blocks.ChoiceBlock(choices=[("primary", "Primary"), ("ghost", "Ghost")], default="primary")

class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)

class PageListBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    pages = blocks.ListBlock(blocks.PageChooserBlock())

class GalleryImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)
