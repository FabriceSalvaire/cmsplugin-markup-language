####################################################################################################

from pathlib import PurePath
import site

# from docutils.core import publish_parts
from docutils.io import StringInput, StringOutput
from docutils.parsers.rst import directives, roles
from docutils.writers.html4css1 import HTMLTranslator
from docutils.core import Publisher

####################################################################################################

extra_params = {
    'initial_header_level': '2',
    'syntax_highlight': 'short',
    'input_encoding': 'utf-8',
    'exit_status_level': 2,
    'embed_stylesheet': False,
    'report_level': 5, # Report system messages "info" or "1", "warning"/"2" (default), "error"/"3", "severe"/"4", "none"/"5"
    'my_settings': 'foobar',
}

DOCUTILS_RENDERER_SETTINGS = {
    'initial_header_level': 1,
    # important, to have even lone titles stay in the html fragment:
    'doctitle_xform': False,
    # we also disable the promotion of lone subsection title to a subtitle:
    'sectsubtitle_xform': False,
    'file_insertion_enabled': False,  # SECURITY MEASURE (file hacking)
    'raw_enabled': False, # SECURITY MEASURE (script tag)
    'report_level': 2, # report warnings and above, by default
}

####################################################################################################

class MyHTMLTranslator(HTMLTranslator):
    pass

####################################################################################################

class RstPublisher:

    ##############################################

    def __init__(self):

        self._publisher = Publisher(source_class=StringInput, destination_class=StringOutput)
        self._publisher.set_components('standalone', 'restructuredtext', 'html')
        self._publisher.writer.translator_class = MyHTMLTranslator
        self._publisher.process_programmatic_settings(None, extra_params, None)

    ##############################################

    def init_plugins(self, plugins):

        site.addsitedir(str(PurePath(__file__).parent / 'RstPlugins'))

        for plugin in plugins:
            print('Register {}'.format(plugin))
            plugin = __import__(plugin, globals(), locals(), str('module'))
            plugin.register(self)

    ##############################################

    def register_directive(self, directive_name, directive_class):

        directives.register_directive(directive_name, directive_class)

    ##############################################

    def register_role(self, role_name, role_class):

        roles.register_local_role(role_name, role_class)

    ##############################################

    def register_node(self, node_class, visit, depart):

        print(node_class.__name__, visit, depart)
        setattr(MyHTMLTranslator, 'visit_' + node_class.__name__, visit)
        setattr(MyHTMLTranslator, 'depart_' + node_class.__name__, depart)

    ##############################################

    def publish(self, source, header_level=None, report_level=None):

        settings_overrides = DOCUTILS_RENDERER_SETTINGS.copy()

        if header_level is not None: # starts from 1
            settings_overrides['initial_header_level'] = header_level
        if report_level is not None: # starts from 1 too
            settings_overrides['report_level'] = 0 # report_level

        self._publisher.set_source(source=source)
        self._publisher.publish(enable_exit_status=True)
        parts = self._publisher.writer.parts

        return parts['html_body'] # parts['body_pre_docinfo'] + parts['fragment']

####################################################################################################

#!# DOCUTILS_RENDERER_SETTINGS.update(get_cfg('SETTINGS_OVERRIDES', {}))
#!# get_cfg('WRITER_NAME', 'html4css1')

# parts = publish_parts(source=source, #!# force_bytes()
#                       writer_name=MyHTMLTranslator,
#                       settings_overrides=settings_overrides)

# http://docutils.sourceforge.net/docs/api/publisher.html

#!# if settings.DEBUG:
#!#     raise template.TemplateSyntaxError("Error in 'restructuredtext' filter: "
#!#                                        "The Python docutils library isn't installed.")
#!# return force_text(value)

