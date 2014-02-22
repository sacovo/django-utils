from creole import creole2html

from django.utils.safestring import mark_safe
from django import template
from django.template.base import Node, TemplateSyntaxError
from django.conf import settings
from django.utils.encoding import force_text

register = template.Library()


# Render creole markup to html
@register.filter(is_safe=True)
def markup(value):
    return mark_safe(creole2html(value))


class StepNode(Node):

    def __init__(self, start, stop, step, varname, nodelist_loop=None):
        self.start = start
        self.stop = stop
        self.step = step
        self.varname = varname
        self.nodelist_loop = nodelist_loop

    def render(self, context):
        if self not in context.render_context:
            context.render_context[self] = range(self.start, self.stop,
                                                 self.step)
        range_iter = context.render_context[self]
        nodelist = []
        loop_dict = context['forloop'] = {
            'parentloop': context.get('forloop', None)
        }
        len_values = len(range_iter)
        for i, x in enumerate(range_iter):
            # Shortcuts for current loop iteration number
            loop_dict['counter0'] = i
            loop_dict['counter'] = i + 1
            # Reverse counter iteration numbers
            loop_dict['revcounter'] = len_values - i
            loop_dict['revcounter0'] = len_values - i - 1
            # Boolean values designating first an last times through loop.
            loop_dict['first'] = (i == 0)
            loop_dict['last'] = (i == len_values - 1)
            # Put the item in the context
            context[self.varname] = x
            if settings.TEMPLATE_DEBUG:
                for node in self.nodelist_loop:
                    try:
                        nodelist.append(node.render(context))
                    except Exception as e:
                        if not hasattr(e, 'django_template_source'):
                            e.django_template_source = node.source
                        raise
            else:
                for node in self.nodelist_loop:
                    nodelist.append(node.render(context))
        return mark_safe(''.join(force_text(n) for n in nodelist))


@register.tag('range')
def do_for(parser, token):
    """
    Loops over a range object.
    For example, to display the odd numbers from 1 to 10:

        {% range i in 1 10 2 %}
            {{i}}
        {% endrange %}

    You can loop backwords with negative step sizes:

        {% range i in 10 1 -1 %}
            {{i}}
        {% endrange %}

    The range loop sets the same variables as the builtin for loop.
    """
    bits = token.split_contents()
    if len(bits) < 4:
        raise TemplateSyntaxError("'range' statments should have at"
                                  " least four words: %s" % token.contents)
    in_index = 2
    if bits[in_index] != 'in':
        raise TemplateSyntaxError("'range' statements should use the format"
                                  " 'range x in y': %s" % token.contents)
    varname = bits[1]
    start = bits[3]
    stop = bits[4]
    step = bits[5]
    nodelist_loop = parser.parse('endrange')
    parser.next_token()
    return StepNode(start, stop, step, varname, nodelist_loop)
