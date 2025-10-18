from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


ICON_TEMPLATE = '<svg class="{classes}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{contents}</svg>'

ICONS = {
    "heroicons:phone": '<path d="M2.25 5.25c0-1.243 1.007-2.25 2.25-2.25h2.152c.98 0 1.828.703 2.007 1.667l.498 2.656c.148.79-.266 1.572-.993 1.93l-1.21.605a.75.75 0 0 0-.255 1.174 11.77 11.77 0 0 0 3.743 3.743.75.75 0 0 0 1.174-.254l.605-1.212a1.5 1.5 0 0 1 1.93-.992l2.656.498A2.25 2.25 0 0 1 20.999 17.6V19.5A2.25 2.25 0 0 1 18.75 21.75H18c-8.837 0-15.75-6.913-15.75-15.75v-.75Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:envelope": '<path d="M20.25 7.5 12 13.5 3.75 7.5m.75 10.5h15a1.5 1.5 0 0 0 1.5-1.5V7.5A1.5 1.5 0 0 0 19.5 6h-15A1.5 1.5 0 0 0 3 7.5v9a1.5 1.5 0 0 0 1.5 1.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:globe-alt": '<path d="M12 1.5c-5.799 0-10.5 4.701-10.5 10.5s4.701 10.5 10.5 10.5 10.5-4.701 10.5-10.5S17.799 1.5 12 1.5Zm0 0c2.485 0 4.5 4.701 4.5 10.5s-2.015 10.5-4.5 10.5m0-21c-2.485 0-4.5 4.701-4.5 10.5s2.015 10.5 4.5 10.5m-9-10.5h18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:bolt": '<path d="M3.75 13.5 12 1.5v8h8.25L12 22.5v-9h-8.25Z" fill="currentColor"/>',
    "heroicons:sparkles": '<path d="M9 7.5 6.75 3 4.5 7.5 0 9.75 4.5 12 6.75 16.5 9 12l4.5-2.25L9 7.5Zm12.75 0L21 3l-1.5 4.5L15 9.75 19.5 12 21 16.5 22.5 12 27 9.75 21.75 7.5Zm-6.375 7.125-1.125-2.625-1.125 2.625-2.625 1.125 2.625 1.125 1.125 2.625 1.125-2.625 2.625-1.125-2.625-1.125Z" fill="currentColor"/>',
    "heroicons:shield-check": '<path d="M12 21.75a.75.75 0 0 1-.348-.085c-3.44-1.764-5.653-4.114-6.977-6.863-1.271-2.636-1.675-5.458-1.675-8.552a.75.75 0 0 1 .39-.657l7.5-4.125a.75.75 0 0 1 .72 0l7.5 4.125a.75.75 0 0 1 .39.657c0 3.094-.404 5.916-1.675 8.552-1.324 2.75-3.537 5.099-6.977 6.863A.75.75 0 0 1 12 21.75ZM9.53 11.47a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.06 0l4.5-4.5a.75.75 0 1 0-1.06-1.06L11.25 13.19l-1.72-1.72Z" fill="currentColor"/>',
    "heroicons:map-pin": '<path d="M12 21.75a1.125 1.125 0 0 1-.994-.592l-2.253-4.226a9.75 9.75 0 1 1 6.494 0l-2.253 4.226a1.125 1.125 0 0 1-.994.592Zm0-9a2.25 2.25 0 1 0 0-4.5 2.25 2.25 0 0 0 0 4.5Z" fill="currentColor"/>',
    "heroicons:clock": '<path d="M12 21.75c5.385 0 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25 2.25 6.615 2.25 12 6.615 21.75 12 21.75Zm.75-9.75h3a.75.75 0 0 1 0 1.5h-3.75a.75.75 0 0 1-.75-.75V7.5a.75.75 0 0 1 1.5 0v4.5Z" fill="currentColor"/>',
    "heroicons:banknotes": '<path d="M3.75 7.5h14.5a1.75 1.75 0 0 1 1.75 1.75v6a1.75 1.75 0 0 1-1.75 1.75H3.75A1.75 1.75 0 0 1 2 15.25v-6A1.75 1.75 0 0 1 3.75 7.5Zm12.25 5.25a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Zm4-5.5V6a1.5 1.5 0 0 0-1.5-1.5H5A1.5 1.5 0 0 0 3.5 6v.515" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:lifebuoy": '<path d="M12 22.5a10.5 10.5 0 1 1 0-21 10.5 10.5 0 0 1 0 21Zm0-7.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-7.716-4.5A7.473 7.473 0 0 1 9 4.284M4.284 15a7.473 7.473 0 0 1 4.5 4.716M15 4.284A7.473 7.473 0 0 1 19.716 9M15 19.716A7.473 7.473 0 0 1 9 19.716" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:car": '<path d="M3.75 15.75h-.75a.75.75 0 1 0 0 1.5h.75v.75a1.5 1.5 0 0 0 1.5 1.5h1.5a1.5 1.5 0 0 0 1.5-1.5v-.75h3v.75a1.5 1.5 0 0 0 1.5 1.5h1.5a1.5 1.5 0 0 0 1.5-1.5v-.75h.75a.75.75 0 1 0 0-1.5h-.75l-.938-4.219A2.25 2.25 0 0 0 14.312 9H6.438a2.25 2.25 0 0 0-2.199 1.781L3.75 15.75Zm3.75-1.5a1.125 1.125 0 1 1-2.25 0 1.125 1.125 0 0 1 2.25 0Zm6.75 0a1.125 1.125 0 1 1-2.25 0 1.125 1.125 0 0 1 2.25 0Zm-8.28-4.219a.75.75 0 0 1 .717-.531h7.874a.75.75 0 0 1 .717.531l.469 2.094H5.72l.5-2.094Z" fill="currentColor"/>',
    "heroicons:truck": '<path d="M2.25 6.75A1.5 1.5 0 0 1 3.75 5.25h9.75v9H12a3 3 0 0 0-5.83.75H5.25a3 3 0 0 0-3 3v.75h1.636a3 3 0 0 0 5.478 0h3.128a3 3 0 0 0 5.478 0H21v-3.176a1.5 1.5 0 0 0-.33-.935l-1.92-2.56a1.5 1.5 0 0 0-1.2-.584h-2.4V5.25h-1.5v9h-.75V5.25H3.75a1.5 1.5 0 0 0-1.5 1.5v0Zm3.75 11.25a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm9 0a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm1.5-6.75h2.4l1.92 2.56V18h-1.02a3 3 0 0 0-5.58 0H16.5v-6.75Z" fill="currentColor"/>',
    "heroicons:scale": '<path d="M11.25 3a1.5 1.5 0 0 1 3 0v.75h2.25a.75.75 0 0 1 0 1.5h-.75v5.835a4.348 4.348 0 0 1 1.787 2.665h1.463m-4.5 4.5A3.75 3.75 0 0 1 12 21.75a3.75 3.75 0 0 1-3.75-3.75h7.5ZM6.75 3.75H5.25a.75.75 0 0 0 0 1.5h.75v5.835a4.348 4.348 0 0 0-1.787 2.665H2.75m6 4.5A3.75 3.75 0 0 1 5 21.75a3.75 3.75 0 0 1-3.75-3.75h7.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:key": '<path d="M15.75 2.25a6.75 6.75 0 1 0 3.745 12.474.75.75 0 0 1 .755.044l2.25 1.5a.75.75 0 0 1 .33.624v3.858a.75.75 0 0 1-.22.53l-1.5 1.5a.75.75 0 0 1-.53.22h-2.25v-2.25h-2.25v-2.25h-2.25l-.309-.005a6.75 6.75 0 0 0-0.216-13.979ZM13.5 9.75a2.25 2.25 0 1 0-4.5 0 2.25 2.25 0 0 0 4.5 0Z" fill="currentColor"/>',
    "heroicons:check": '<path d="M4.5 12.75 9 16.5l10.5-9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:bars-3": '<path d="M3.75 6.75h16.5a.75.75 0 0 0 0-1.5H3.75a.75.75 0 0 0 0 1.5Zm0 6h16.5a.75.75 0 0 0 0-1.5H3.75a.75.75 0 0 0 0 1.5Zm0 6h16.5a.75.75 0 0 0 0-1.5H3.75a.75.75 0 0 0 0 1.5Z" fill="currentColor"/>',
    "heroicons:chevron-right": '<path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:magnifying-glass": '<path d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:shopping-cart": '<path d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "heroicons:heart": '<path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
}


@register.simple_tag
def marketing_icon(name: str, classes: str = "w-6 h-6") -> str:
    """Render an inline SVG icon with Tailwind utility classes."""

    svg_contents = ICONS.get(name)
    if not svg_contents:
        return ""
    return mark_safe(ICON_TEMPLATE.format(classes=classes, contents=svg_contents))
