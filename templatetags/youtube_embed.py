'''
Created on 26/07/2012

@author: Johnny
'''
from django.template.defaultfilters import stringfilter
from django import template
import re

register = template.Library()

@register.filter
@stringfilter
def youtube(url):
    
    r = re.compile(r'(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=v\/)[^&\n]+(?=\?)|(?<=v=)[^&\n]+|(?<=youtu.be/)[^&\n]+')
    
    video_id = r.findall(url)    

    
    if not video_id: return "url"
      
    return r'http://www.youtube.com/embed/' + video_id[0]
    #""" http://www.youtube.com/embed/%s""" % (video_id)
youtube.is_safe = True # Don't escape HTML

@register.filter
@stringfilter
def youthumbnail(url,args):
    r = re.compile(r'(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=v\/)[^&\n]+(?=\?)|(?<=v=)[^&\n]+|(?<=youtu.be/)[^&\n]+')
    
    video_id = r.findall(url)    
    
    
    if not video_id: return None
    
    if args == 'small':
        return "http://img.youtube.com/vi/%s/2.jpg" % video_id[0]
    elif args == 'large':
        return "http://img.youtube.com/vi/%s/0.jpg" % video_id[0]
    else:
        return None

youthumbnail.is_safe = True # Don't escape HTML