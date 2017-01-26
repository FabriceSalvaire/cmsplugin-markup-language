####################################################################################################

from django import template
from django.conf import settings
from django.utils.encoding import force_text, force_bytes
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import MarkupLanguagePluginForm
from .models import MarkupLanguagePluginModel, MarkupLanguageImageModel

from .RstPublisher import RstPublisher
from . import RstPlugins

#!# from .utils import postprocess, get_cfg, french_insecable

####################################################################################################

rst_publisher = RstPublisher()
rst_publisher.init_plugins(RstPlugins.PLUGINS)

####################################################################################################

def render_rich_text(source, language_code='', header_level=None, report_level=None):

    # rst = get_cfg('CONTENT_PREFIX', '') + '\n'
    # rst += source
    # rst += '\n' + get_cfg('CONTENT_SUFFIX', '')
    # rst = rst.replace('{{ MEDIA_URL }}', settings.MEDIA_URL)
    # rst = rst.replace('{{ STATIC_URL }}', settings.STATIC_URL)

    content = rst_publisher.publish(source, header_level=header_level, report_level=report_level)

    # content = content.replace('{{ BR }}', '<br/>')
    # content = content.replace('{{ NBSP }}', '&nbsp;')

    # if language_code.lower().startswith('fr'): # ONLY french codes should start like that
    #     content = french_insecable(content)

    # content = postprocess(content)

    return content

####################################################################################################

class MarkupLanguageImagePlugin(CMSPluginBase):

    model = MarkupLanguageImageModel
    module = _('Markup Language')
    name = _("RST Image")
    require_parent = True
    # parent_classes = ['MarkupLanguagePlugin']

    # render_template = template.Template('') # Issue: 'dict' object has no attribute 'render_context'
    # render_plugin = False # Issue: cannot edit
    render_template = 'cmsplugin_markup_language/fake.html' # Hack

    # Editor fieldsets
    fieldsets = (
        (None, {
            'fields': ('svg_image',
                       'tag_type',
                       'height', 'width',
                       'alignment',
                       'caption_text',
                       'alt_text')
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'additional_class_names',
                'label',
                'id_name',
            ),
        }),
    )

####################################################################################################

class MarkupLanguagePlugin(CMSPluginBase):

    name = _('Restructured Text Plugin')
    module = _('Markup Language')
    # render_template = 'cms/content.html'
    render_template = 'cmsplugin_markup_language/content.html'
    model = MarkupLanguagePluginModel
    form = MarkupLanguagePluginForm
    allow_children = True
    child_classes = ['MarkupLanguageImagePlugin', 'SvgImagePlugin']

    ##############################################

    def render(self, context, instance, placeholder):

        print('MarkupLanguageImagePlugin.render')

        source = instance.body

        if instance.child_plugin_instances is not None:
            for child in instance.child_plugin_instances:
                if isinstance(child, MarkupLanguageImageModel):
                    print(child.svg_image.url)
                    source = source.replace('{{ image1 }}', child.svg_image.url)
                # call render_plugin
                content_renderer = context['cms_content_renderer']
                content = content_renderer.render_plugin(
                    instance=child,
                    context=context,
                    editable=content_renderer.user_is_on_edit_mode(),
                )
                print(child, content)

        # We lookup cms page language, else i18n language
        language_code = context.get('lang', '') or context.get('LANGUAGE_CODE', '')
        content = render_rich_text(source,
                                   language_code=language_code,
                                   header_level=instance.header_level,
                                   report_level=None) # not set ATM
        context.update({'content': mark_safe(content)})
        return context

####################################################################################################

plugin_pool.register_plugin(MarkupLanguageImagePlugin)
plugin_pool.register_plugin(MarkupLanguagePlugin)
