from django import template
from django.utils.html import format_html_join, escape

register = template.Library()

@register.simple_tag
def meta_generator(title="Default Title", description="Default Description", image_url=None, url=None, site_name=None, object_type="website", twitter_card="summary_large_image", twitter_site=None, canonical_url=None):
    meta_tags = [
        ('name', 'description', escape(description)),
        ('property', 'og:title', escape(title)),
        ('property', 'og:description', escape(description)),
        ('property', 'og:type', object_type),
        ('name', 'twitter:card', twitter_card),
    ]

    if site_name:
        meta_tags.append(('property', 'og:site_name', escape(site_name)))
    if image_url:
        meta_tags.append(('property', 'og:image', escape(image_url)))
        meta_tags.append(('name', 'twitter:image', escape(image_url)))
    if url:
        meta_tags.append(('property', 'og:url', escape(url)))
    if twitter_site:
        meta_tags.append(('name', 'twitter:site', escape(twitter_site)))

    # Generate meta tags
    meta_html = format_html_join('\n', '<meta {0}="{1}" content="{2}" />', meta_tags)

    # Add canonical link if provided
    if canonical_url:
        meta_html += f'\n<link rel="canonical" href="{escape(canonical_url)}" />'

    return meta_html
