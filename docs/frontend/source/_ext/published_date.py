from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective

class published_date_container(nodes.General, nodes.Element):
    pass

class PublishedDateDirective(SphinxDirective):
    has_content = True  # Allow content to support both indentation styles
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'published': directives.unchanged_required,
        'updated': directives.unchanged,
    }

    def run(self):
        # Handle options from content if present
        published_date = ''
        updated_date = ''
        
        if self.content:
            content_str = '\n'.join(self.content)
            # Look for published and updated in content
            import re
            published_match = re.search(r':published:\s*(.*?)(?:\n\s*:|$)', content_str, re.DOTALL)
            updated_match = re.search(r':updated:\s*(.*?)(?:\n\s*:|$)', content_str, re.DOTALL)
            
            if published_match:
                published_date = published_match.group(1).strip()
            else:
                published_date = self.options.get('published', '')
                
            if updated_match:
                updated_date = updated_match.group(1).strip()
            else:
                updated_date = self.options.get('updated', '')
        else:
            # Get the published and (optional) updated dates from options
            published_date = self.options.get('published', '')
            updated_date = self.options.get('updated', '')
        
        # Create a custom node for the date information
        container = published_date_container()
        container['published'] = published_date
        container['updated'] = updated_date
        
        # Create the text content - just show the date without "Published:" prefix
        text_content = f"{published_date}"
        if updated_date:
            text_content += f" | Last Updated: {updated_date}"
        
        # Add the text to the container
        container += nodes.Text(text_content)
        
        return [container]

# HTML Visitor methods for the date container
def visit_published_date_container_html(self, node):
    self.body.append('<div class="published-date">')

def depart_published_date_container_html(self, node):
    self.body.append('</div>')

def setup(app):
    app.add_directive('published-date', PublishedDateDirective)
    
    app.add_node(
        published_date_container,
        html=(visit_published_date_container_html, depart_published_date_container_html)
    )
    
    # Add custom CSS with the same styling as toc-entry-date
    app.add_css_file('css/published_date.css')
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }