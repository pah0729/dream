from django import template
import re

register = template.Library()

@register.filter
def add_link(value):
    hashtag = value.hashtag
    tags = value.tag_set.all()
    for tag in tags:
        hashtag = re.sub(r'\#'+tag.name+r'\b', '<a style="color:#aaaaaa" href="/notice/explore/tags/'+tag.name+'">#'+tag.name+'</a>', hashtag)
    return hashtag

@register.filter
def add_link_case(value):
    hashtag = value.hashtag
    tags = value.tag_set.all()
    for tag in tags:
        hashtag = re.sub(r'\#'+tag.name+r'\b', '<a style="color:#aaaaaa" href="/notice/explore_case/tags/'+tag.name+'">#'+tag.name+'</a>', hashtag)
    return hashtag