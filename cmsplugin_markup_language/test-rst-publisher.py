####################################################################################################

from RstPublisher import RstPublisher
import RstPlugins

####################################################################################################

rst_publisher = RstPublisher()
rst_publisher.init_plugins(RstPlugins.PLUGINS)

source = """
Title
-----

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis dictum purus. Nulla consectetur
nec mi at rutrum. Donec eget mollis ex. Nullam nec facilisis metus. Cum sociis natoque penatibus et
magnis dis parturient montes, nascetur ridiculus mus. Ut tristique tortor purus, id hendrerit turpis
vulputate non. Ut sed turpis vel tellus molestie auctor ut molestie arcu.

Pygments test
-------------

.. sourcecode:: python

  def my_function():
      "just a test"
      print 8/2

Microdata itemscope test
------------------------

.. itemscope:: Person

    My name is :itemprop:`John Doe <name>`
"""

print(rst_publisher.publish(source))
