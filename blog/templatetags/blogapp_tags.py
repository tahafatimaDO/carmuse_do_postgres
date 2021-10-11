from blog.models import BlogCategory as Category, Tag
from django.template import Library, loader

register = Library()


@register.inclusion_tag('blog/components/tags_list.html',
                        takes_context=True)
def tags_list(context):
    tags = Tag.objects.all()
    return {
        'request': context['request'],
        'blog_page': context['blog_page'],
        'tags': tags
    }


@register.inclusion_tag('blog/components/categories_list.html',
                        takes_context=True)
def categories_list(context):
    categories = Category.objects.all()
    return {
        'request': context['request'],
        'blog_page': context['blog_page'],
        'categories': categories
    }


@register.inclusion_tag("catalog/components/post_categories_list.html", takes_context=True)
def post_categories_list(context):
    page = context["page"]
    categories = page.painting_categories.all()
    return {
        "request": context["request"],
        "categories": categories,
    }