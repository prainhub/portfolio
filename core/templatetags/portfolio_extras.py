from django import template

register = template.Library()


@register.filter
def initials(value):
    """'Prajin S' -> 'PS'"""
    if not value:
        return ""
    parts = str(value).split()
    return "".join(p[0].upper() for p in parts[:2] if p)


@register.filter
def split_paragraphs(value):
    """Split a summary field on blank lines into a list of paragraphs."""
    if not value:
        return []
    return [p.strip() for p in str(value).split("\n\n") if p.strip()]


@register.filter
def get_item(mapping, key):
    """Look up a dict value by a variable key (skills_by_category|get_item:key)."""
    if not mapping:
        return []
    return mapping.get(key, [])
