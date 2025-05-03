from docutils import nodes
from docutils.parsers.rst import Directive, directives


class corner_quote(nodes.General, nodes.Element):
    pass


def visit_corner_quote_html(self, node):
    justify = node.get('justify', 'right')
    mobile = node.get('mobile', False)
    
    classes = ['corner-quote']
    if justify == 'left':
        classes.append('corner-quote-left')
    if not mobile:
        classes.append('corner-quote-hide-mobile')
        
    self.body.append(f'<div class="{" ".join(classes)}">')


def depart_corner_quote_html(self, node):
    self.body.append('</div>')


class CornerQuoteDirective(Directive):
    has_content = True
    option_spec = {
        'text': directives.unchanged,
        'justify': directives.unchanged,
        'mobile': directives.flag,
    }

    def run(self):
        node = corner_quote()
        
        # Store the justification setting
        justify = self.options.get('justify', 'right')
        node['justify'] = justify
        
        # Store the mobile display setting (defaults to False if not present)
        node['mobile'] = 'mobile' in self.options
        
        # Get the quote text
        text = self.options.get('text', '')
        if text:
            # Add quotes around the text
            quoted_text = f'"{text}"'
            para = nodes.paragraph()
            para += nodes.Text(quoted_text)
            node += para
        
        return [node]


def setup(app):
    app.add_node(corner_quote,
                 html=(visit_corner_quote_html, depart_corner_quote_html))
    app.add_directive('corner-quote', CornerQuoteDirective)
    
    # Add custom CSS
    app.add_css_file('css/corner_quote.css')
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }