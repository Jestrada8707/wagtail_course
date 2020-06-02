""" Blog page """

from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


from streams import blocks


class BlogListingPage(RoutablePageMixin, Page):
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

    @route(r'^lastest/?$', name='latest_post')
    def get_latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request,*args,**kwargs)
        context['posts'] = context['posts'][:1]
        return render(request, 'blog/latest_post.html', context)


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
