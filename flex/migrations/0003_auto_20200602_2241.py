# Generated by Django 3.0.6 on 2020-06-02 22:41

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0002_auto_20200528_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexpage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Add additional text', required=True))])), ('RichText_Tool', streams.blocks.RichtextBlock()), ('Simple_RichText_Tool', streams.blocks.SimpleRichtextBlock()), ('Cards', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add some title for block of cards', required=True)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=40, required=True)), ('text', wagtail.core.blocks.TextBlock(max_length=200, required=True)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=False))])))])), ('Call_to_action', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'embed'], required=True)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(required=True))])), ('Button_Url', wagtail.core.blocks.StructBlock([('button_page', wagtail.core.blocks.PageChooserBlock(help_text='Use for internal link example home or about page', required=False)), ('button_url', wagtail.core.blocks.URLBlock(help_text='Use for external link, for example google or facebook', required=False))]))], blank=True, null=True),
        ),
    ]
