"""Flexible page"""

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from streams import blocks


class FlexPage(Page):
    """Flexible page class"""

    template = 'flex/flex_page.html'

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("RichText_Tool", blocks.RichtextBlock()),
            ("Simple_RichText_Tool", blocks.SimpleRichtextBlock()),
            ("Cards", blocks.CardBlock()),
            ("Call_to_action", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('content'),
    ]

    class Meta:  # noqa

        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
