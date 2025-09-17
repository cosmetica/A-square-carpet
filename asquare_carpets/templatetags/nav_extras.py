# asquare_carpets/templatetags/nav_extras.py
from django import template
from asquare_carpets.models import ProductsIndexPage

register = template.Library()

def chunk_columns(items, cols=3):
    items = list(items)
    if not items:
        return []
    per_col = max(1, (len(items) + cols - 1) // cols)
    return [items[i:i+per_col] for i in range(0, len(items), per_col)]

@register.simple_tag
def products_index():
    """คืนหน้า ProductsIndexPage (ถ้ามี)"""
    return ProductsIndexPage.objects.live().first()

@register.simple_tag
def product_columns(cols=3):
    """คืนรายการ ProductPage แบบแบ่งคอลัมน์"""
    index = ProductsIndexPage.objects.live().first()
    if not index:
        return []
    children = index.get_children().live()
    return chunk_columns(children, cols=int(cols))