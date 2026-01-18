from django import template
from django.utils.safestring import mark_safe
from wagtail.models import Site

register = template.Library()


@register.inclusion_tag('includes/site_nav.html', takes_context=True)
def render_site_nav(context):
    request = context.get('request')
    try:
        site = None
        if request is not None:
            try:
                site = Site.find_for_request(request)
            except Exception:
                site = None
        if site is None:
            site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        root = site.root_page if site is not None else None
    except Exception:
        root = None

    # current page may or may not be present in the template context
    current_page = context.get('page')

    nav_items = []
    home_item = None
    if root is not None:
        # build a separate `home_item` for the site root (brand link)
        try:
            show_root = getattr(root, 'show_in_menus', True)
        except Exception:
            show_root = True
        if show_root:
            root_active = False
            try:
                if current_page is not None:
                    root_active = (current_page.id == root.id) or current_page.is_descendant_of(root)
            except Exception:
                root_active = False

            home_item = {
                'item': root,
                'children': [c for c in root.get_children().live() if getattr(c, 'show_in_menus', True)],
                'active': root_active,
            }

        for item in root.get_children().live():
            try:
                show = getattr(item, 'show_in_menus', True)
            except Exception:
                show = True
            if not show:
                continue

            # collect visible children
            children = []
            for child in item.get_children().live():
                if getattr(child, 'show_in_menus', True):
                    children.append(child)

            # determine active state (current page is descendant of this top item)
            active = False
            try:
                if current_page is not None:
                    active = (current_page.id == item.id) or current_page.is_descendant_of(item)
            except Exception:
                active = False

            nav_items.append({
                'item': item,
                'children': children,
                'active': active,
            })

    return {
        'home_item': home_item,
        'nav_items': nav_items,
        'request': request,
    }
