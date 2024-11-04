from django import template

register = template.Library()

@register.filter
def make_range(value):
    return range(1, value + 1)

@register.filter
def make_year_range(start, end):
    return range(start, end + 1)

@register.filter
def format_two_digits(value):
    return f"{value:02}" 