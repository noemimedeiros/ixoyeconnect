import os
from django import template

from posts.models import Curtida, Salvo

register = template.Library()

@register.filter
def icons_arquivos(ext):
    print(ext)
    if ext in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']:
        return 'fa-image text-danger'
    if ext in ['.xls', '.xlsx']:
        return 'fa-file-excel text-success'
    if ext in ['.doc', '.docx']:
        return 'fa-file-word text-info'
    if ext in ['.pdf']:
        return 'fa-file-pdf text-danger'
    if ext in ['.zip', '.rar', '.Z', '.tar', '.gz']:
        return 'fa-file-zipper text-muted'
    if ext in ['.csv']:
        return 'fa-file-csv text-success'
    if ext in ['.ppt', '.pptm', '.pptx']:
        return 'fa-file-powerpoint text-warning'
    if ext in ['.mp3', '.wav', '.wma']:
        return 'fa-file-audio text-danger'
    if ext in ['.mp4', '.mov', '.avi', '.mpg', '.wmv']:
        return 'fa-file-video text-danger'
    else:
        return 'fa-file text-info'
    
@register.filter
def file_ext(value):
    return os.path.splitext(value.name)[1]

@register.filter
def curtido(post, user):
    if Curtida.objects.filter(post=post, user=user).exists():
        return True
    else:
        return False
    
@register.filter
def salvo(post, user):
    if Salvo.objects.filter(post=post, user=user).exists():
        return True
    else:
        return False