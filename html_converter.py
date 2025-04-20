"""
HTML Converter Module

This module provides functions to convert Markdown elements to HTML.
Each function focuses on a specific Markdown feature.
"""

import re
import html
from pathlib import Path


def convert_inline_code(line):
    """
    Convert Markdown inline code to HTML code tags.
    
    Args:
        line (str): A line of text that may contain inline code
        
    Returns:
        str: The line with inline code converted to HTML
    """
    pattern = re.compile(r"`([^`]*)`")
    for code in re.findall(pattern, line):
        line = line.replace('`' + code + '`', '<code>' + html.escape(code) + '</code>')
    return line


def convert_code_block(line, in_code_block):
    """
    Convert Markdown code blocks to HTML pre and code tags.
    
    Args:
        line (str): A line of text that may start or end a code block
        in_code_block (bool): Whether we're currently in a code block
        
    Returns:
        tuple: (modified_line, updated_in_code_block)
    """
    if "```" in line:
        if in_code_block:
            line = line.replace("```", "</code></pre>")
            in_code_block = False
        else:
            line = line.replace("```", "<pre><code>")
            in_code_block = True
    return (line, in_code_block)


def convert_comment_block(line, in_comment):
    """
    Convert Markdown comment blocks (using %%) to HTML comments.
    
    Args:
        line (str): A line of text that may start or end a comment block
        in_comment (bool): Whether we're currently in a comment block
        
    Returns:
        tuple: (modified_line, updated_in_comment)
    """
    if "%%" in line:
        if in_comment:
            line = line.replace("%%", "-->")
            in_comment = False
        else:
            line = line.replace("%%", "<!--")
            in_comment = True
    return (line, in_comment)


def convert_horizontal_rule(line):
    """
    Convert Markdown horizontal rule (---) to HTML hr tag.
    
    Args:
        line (str): A line of text that may be a horizontal rule
        
    Returns:
        str: The converted line
    """
    if line.startswith("---"):
        line = "<hr>"
    return line


def convert_link_in_text(line):
    """
    Convert Markdown links [text](url) to HTML a tags.
    
    Args:
        line (str): A line of text that may contain Markdown links
        
    Returns:
        str: The line with links converted to HTML
    """
    pattern = re.compile(r"\[([^\]]*)\]\(([^\)]*)\)")
    for (text, url) in re.findall(pattern, line):
        line = line.replace('[' + text + '](' + url + ')', '<a href="' + url + '">' + text + '</a>')
    return line


def convert_external_links(line):
    """
    Convert plain URLs to HTML a tags.
    
    Args:
        line (str): A line of text that may contain URLs
        
    Returns:
        str: The line with URLs converted to HTML links
    """
    pattern = re.compile(r"https?://[^\s]+")
    for url in re.findall(pattern, line):
        line = line.replace(url, '<a href="' + url + '">' + url + '</a>')
    return line


def convert_checkboxes(line):
    """
    Convert Markdown checkboxes to HTML input checkboxes.
    
    Args:
        line (str): A line of text that may contain Markdown checkboxes
        
    Returns:
        str: The line with checkboxes converted to HTML
    """
    # Unchecked boxes
    pattern = re.compile(r"- \[ \]")
    for checkbox in re.findall(pattern, line):
        line = line.replace(checkbox, '<input type="checkbox">')
    
    # Checked boxes
    pattern = re.compile(r"- \[x\]")
    for checkbox in re.findall(pattern, line):
        line = line.replace(checkbox, '<input type="checkbox" checked>')
    
    return line


def convert_bold_text(line):
    """
    Convert Markdown bold text (**text**) to HTML strong tags.
    
    Args:
        line (str): A line of text that may contain bold text
        
    Returns:
        str: The line with bold text converted to HTML
    """
    pattern = re.compile(r"\*\*([^\*]*)\*\*")
    for text in re.findall(pattern, line):
        line = line.replace('**' + text + '**', '<strong>' + text + '</strong>')
    return line


def convert_headings(line):
    """
    Convert Markdown headings to HTML heading tags.
    
    Args:
        line (str): A line of text that may be a heading
        
    Returns:
        str: The line with headings converted to HTML
    """
    pattern = re.compile(r"^#+ (.*)")
    for text in re.findall(pattern, line):
        level = len(line.split(" ")[0])
        line = line.replace('#' * level + ' ' + text, 
                           f'<h{level}>{text}</h{level}>')
    return line


def convert_list_items(line):
    """
    Convert Markdown list items to HTML li tags.
    
    Args:
        line (str): A line of text that may be a list item
        
    Returns:
        str: The line with list items converted to HTML
    """
    if line.startswith("- "):
        line = line.replace("- ", "<li>") + "</li>"
    return line


def insert_paragraphs(line):
    """
    Insert HTML paragraph tags for empty lines.
    
    Args:
        line (str): A line of text
        
    Returns:
        str: The line with paragraph tags if empty
    """
    if line.strip() == "":
        line = "<p>"
    return line


def generate_html_head(title=None):
    """
    Generate the HTML head section with appropriate CSS and JavaScript.
    
    Args:
        title (str, optional): The title for the HTML document
        
    Returns:
        str: The HTML head section as a string
    """
    head = "<!DOCTYPE html>\n<html>\n<head>\n"
    head += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n'
    
    # Add title if provided
    if title:
        head += f"<title>{title}</title>\n"
    
    # Code highlighting with highlight.js
    head += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">\n'
    head += '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>\n'
    head += '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/languages/go.min.js"></script>\n'
    head += '<script>hljs.initHighlightingOnLoad();</script>\n'
    
    # CSS styles
    head += "<style>\n"
    head += "\timg { max-width:900px; }\n"
    head += "\t.codeblock { \n\tbackground: #B0B0B0; padding:1px 10px 0px 10px; border-radius: 5px; overflow-x:auto; \n\t}\n"
    head += "\tcode {\n font-family: monospace; font-size: inherit; color: #202020; \n\t}\n"
    head += "\t.inlineCoed {\n font-family: monospace; font-size: inherit; color: #202020; \n\t}\n"
    head += "</style>\n"
    head += "</head>\n"
    
    return head


def generate_html_body_start(has_sidebar=True):
    """
    Generate the HTML body opening and main container.
    
    Args:
        has_sidebar (bool): Whether to include space for a sidebar
        
    Returns:
        str: The HTML body opening as a string
    """
    body = '<body style="background: #F0F0F0;">\n'
    body += '<div style="margin: 0 auto; width:1380px; position: relative;">\n'
    
    if has_sidebar:
        body += '<div style="width:1000px; padding:20px; margin:0px; z-index: 5; text-align:left; background-color: #DCDCDC; border-radius: 5px; position:absolute; top:0; left:340px;">\n'
    else:
        body += '<div style="width:1000px; padding:20px; margin:0 auto; text-align:left; background-color: #DCDCDC; border-radius: 5px;">\n'
    
    return body


def generate_html_body_end(sidebar_content=None):
    """
    Generate the HTML body closing and optional sidebar.
    
    Args:
        sidebar_content (str, optional): HTML content for the sidebar
        
    Returns:
        str: The HTML body closing as a string
    """
    body_end = "</div>\n"  # Close main content div
    
    if sidebar_content:
        body_end += '<div style="width:345px; padding-top: 20px; position:absolute; top:0; left:0; overflow:auto;">\n'
        body_end += sidebar_content
        body_end += "</div>\n"
    
    body_end += "</div>\n"  # Close container div
    body_end += "</body>\n</html>\n"
    
    return body_end


def generate_index_html(target_file):
    """
    Generate a simple index.html that redirects to the main HTML file.
    
    Args:
        target_file (str): The path to the main HTML file
        
    Returns:
        str: The HTML content for the index file
    """
    return f'<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<meta http-equiv="Refresh" content="0; url=\'./{target_file}.html\'" />\n\t</head>\n</html>' 