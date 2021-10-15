"""menus/templatetags/menus_tags.py"""
from django import template
from home.models import CompanyLogo

from ..models import Menu

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.filter(slug=slug).first()


@register.simple_tag()
def company_logo():
    return CompanyLogo.objects.first()
