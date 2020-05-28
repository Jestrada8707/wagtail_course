from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text nothing else"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title and Text'


class CardBlock(blocks.StructBlock):
    """ Cards with image and text and button(s)"""

    title = blocks.CharBlock(required=True, help_text="Add some title for block of cards")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = 'streams/cards.html'
        icon = 'placeholder'
        label = 'Staff Cards'


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features"""

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features"""

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
            "embed",
        ]

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple  RichText"


class CTABlock(blocks.StructBlock):
    """ A simple call to action section"""

    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic', 'link', 'embed'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to action"
