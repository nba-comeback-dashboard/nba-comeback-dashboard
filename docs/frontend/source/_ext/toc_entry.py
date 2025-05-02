from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective
from docutils.nodes import Node
import os

class toc_entry_container(nodes.General, nodes.Element):
    pass

class toc_entry_link(nodes.General, nodes.Element):
    pass

class toc_entry_image(nodes.General, nodes.Element):
    pass

class TocEntryDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'title': directives.unchanged,
        'link': directives.unchanged,
        'subtitle': directives.unchanged,
        'date': directives.unchanged,
        'image': directives.unchanged,
    }

    def run(self):
        title = self.options.get('title', '')
        link = self.options.get('link', '')
        subtitle = self.options.get('subtitle', '')
        date = self.options.get('date', '')
        image_path = self.options.get('image', '')
        
        # Create the main container
        container = toc_entry_container()
        
        # Process the link to handle .rst extension
        # If the link ends with .rst, convert it to .html for the output
        if link.endswith('.rst'):
            link_for_html = link[:-4] + '.html'
        # If link doesn't have an extension, assume it's a document name and add .html
        elif '.' not in link.split('/')[-1]:
            link_for_html = link + '.html'
        else:
            link_for_html = link
            
        # Extract title from RST file if not provided
        if not title and link and link.endswith('.rst'):
            try:
                # Get the source directory path
                source_dir = self.env.srcdir
                
                # Determine if the link is relative to the current document or absolute
                if link.startswith('/'):
                    rst_path = link
                else:
                    # Get the directory of the current document
                    current_doc_dir = os.path.dirname(self.env.doc2path(self.env.docname))
                    # Create path relative to the current document
                    rst_path = os.path.join(current_doc_dir, link)
                
                # Read the RST file to extract the title
                with open(rst_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Look for a title line (indicated by a line with underlines or overlines+underlines)
                for i in range(len(lines)):
                    # Skip empty lines
                    if not lines[i].strip():
                        continue
                    
                    # Check for overline pattern (line with ===, ---, etc. followed by text then same pattern)
                    if i < len(lines) - 2 and lines[i].strip() and all(c == lines[i].strip()[0] for c in lines[i].strip()):
                        if all(c == lines[i+2].strip()[0] for c in lines[i+2].strip()) and len(lines[i].strip()) == len(lines[i+2].strip()):
                            title = lines[i+1].strip()
                            break
                    
                    # Check for underline pattern (text followed by a line of ===, ---, etc.)
                    if i < len(lines) - 1 and lines[i].strip() and all(c == lines[i+1].strip()[0] for c in lines[i+1].strip()):
                        if len(lines[i].strip()) <= len(lines[i+1].strip()):
                            title = lines[i].strip()
                            break
                
                pass  # Successfully extracted title
            except Exception:
                # If extraction fails, continue with empty title
                pass
                
        # If title is still empty, use the link name as a fallback
        if not title and link:
            title = os.path.splitext(os.path.basename(link))[0].replace('_', ' ').title()
            
        # Add title with link
        if title and link:
            title_para = nodes.paragraph(classes=['toc-entry-title'])
            
            # Create a custom link node instead of reference
            title_link = toc_entry_link()
            title_link['href'] = link_for_html
            title_link['title'] = title
            title_link += nodes.Text(title)
            
            title_para += title_link
            container += title_para
        
        # Add subtitle
        if subtitle:
            subtitle_para = nodes.paragraph(classes=['toc-entry-subtitle'])
            subtitle_para += nodes.Text(subtitle)
            container += subtitle_para
        
        # Add date - if not provided, try to find a published-date directive in the linked RST file
        if date:
            date_para = nodes.paragraph(classes=['toc-entry-date'])
            date_para += nodes.Text(date)
            container += date_para
        elif link and link.endswith('.rst'):
            try:
                # Determine the path to the linked RST file
                source_dir = self.env.srcdir
                if link.startswith('/'):
                    rst_path = link
                else:
                    current_doc_dir = os.path.dirname(self.env.doc2path(self.env.docname))
                    rst_path = os.path.join(current_doc_dir, link)
                
                # Read the RST file to look for a published-date directive
                with open(rst_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for published-date directive
                import re
                # Extract just the date value from the published field - more robust pattern
                match = re.search(r'\.\.\s+published-date::.*?:published:\s+([^:\n]+?)(?:\s*\n|$)', content, re.DOTALL)
                if match:
                    published_date = match.group(1).strip()
                    date_para = nodes.paragraph(classes=['toc-entry-date'])
                    date_para += nodes.Text(f"{published_date}")
                    container += date_para
            except Exception:
                # If extraction fails, continue without a date
                pass
        
        # Add image - place all images in _static/toc directory
        if image_path:
            # If the image path is already an absolute web path or URL, use it as is
            if image_path.startswith('http'):
                final_path = image_path
            # If it's a root-relative path that starts with /, use it as is
            elif image_path.startswith('/'):
                final_path = image_path
            # If it already includes _static but not root-relative, make it root-relative
            elif image_path.startswith('_static/'):
                final_path = f"/{image_path}"
            # Otherwise, prepend /_static/toc/ to the filename (root-relative)
            else:
                # Get just the base filename without any path
                base_filename = os.path.basename(image_path)
                final_path = f"/_static/toc/{base_filename}"
            
            # Use a custom image node to avoid the reference+image issue
            img = toc_entry_image()
            img['uri'] = final_path
            img['alt'] = title or 'TOC entry image'
            container += img
        
        return [container]

# HTML Visitor methods for custom nodes
def visit_toc_entry_container_html(self, node):
    self.body.append('<div class="toc-entry-container">')
    self.body.append('<div class="toc-entry-content">')

def depart_toc_entry_container_html(self, node):
    self.body.append('</div></div>')

def visit_toc_entry_link_html(self, node):
    self.body.append(f'<a href="{node["href"]}">')

def depart_toc_entry_link_html(self, node):
    self.body.append('</a>')

def visit_toc_entry_image_html(self, node):
    self.body.append('</div><div class="toc-entry-image-container">')
    self.body.append(f'<img src="{node["uri"]}" alt="{node["alt"]}" class="toc-entry-image"/>')

def depart_toc_entry_image_html(self, node):
    self.body.append('</div>')

class TocEntriesWrapper(SphinxDirective):
    """A directive for wrapping multiple toc-entry directives in a parent container."""
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    
    def run(self):
        # Parse the content as RST
        node = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, node)
        
        # Create a container for all entries
        wrapper = nodes.container(classes=['toc-entries-wrapper'])
        wrapper.extend(node.children)
        
        return [wrapper]

def setup(app):
    app.add_directive('toc-entry', TocEntryDirective)
    app.add_directive('toc-entries', TocEntriesWrapper)
    
    # Register custom nodes
    app.add_node(
        toc_entry_container,
        html=(visit_toc_entry_container_html, depart_toc_entry_container_html)
    )
    app.add_node(
        toc_entry_link,
        html=(visit_toc_entry_link_html, depart_toc_entry_link_html)
    )
    app.add_node(
        toc_entry_image,
        html=(visit_toc_entry_image_html, depart_toc_entry_image_html)
    )
    
    # Add custom CSS
    app.add_css_file('css/toc_entry.css')
    
    # Add JavaScript for auto-wrapping toc-entry directives
    # This will wrap all consecutive toc-entry elements in a wrapper div
    app.add_js_file('js/toc_entry_wrapper.js')
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }