""" Blog page """

from django.db import models
from django.shortcuts import render
from django import forms
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from streams import blocks


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more author for blog detail page"""

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ], heading='Name and Image'
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ], heading="Links"
        )
    ]

    def __str__(self):
        """String represent this class"""
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for snipped"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify posts by this category"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


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
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        paginator = Paginator(all_posts, 2)  # @todo change to 5 per page

        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context

    @route(r'^lastest/?$', name='latest_post')
    def get_latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:1]
        return render(request, 'blog/latest_post.html', context)

    def get_sitemap_urls(self, request):
        # uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_post'),
                'lastmod': (self.last_published_at or self.latest_revision_created_at),
                'priority': 0.9,
            }
        )

        return sitemap


class BlogDetailPage(Page):
    """ Blog detail page"""

    custom_title = models.CharField(max_length=120, blank=False, null=False, help_text='Overwrites the default title')

    banner_image = models.ForeignKey(
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

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        StreamFieldPanel('content'),
    ]

    # Update Cache when something is update
    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            'post_cache_test',
            [self.id]
        )
        cache.delete(key)
        return super().save(*args, **kwargs)


class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post for article"""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='The best size for this image is 1400 x 300'
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        ImageChooserPanel('intro_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        StreamFieldPanel('content'),
    ]


class VideoBlogPage(BlogDetailPage):
    """A video subclass page"""

    template = 'blog/video_blog_page.html'
    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        FieldPanel('youtube_video_id'),
        StreamFieldPanel('content'),
    ]
