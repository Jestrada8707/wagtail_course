""" Blog page """

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks


class BlogListingPage(Page):
    """ Listing all blog pages"""

    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(max_length=120, blank=False, null=False, help_text='Overwrites the default title')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""

        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        return context


class BlogDetailPage(Page):
    """ Blog detail page"""

    custom_title = models.CharField(max_length=120, blank=False, null=False, help_text='Overwrites the default title')

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

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

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]
