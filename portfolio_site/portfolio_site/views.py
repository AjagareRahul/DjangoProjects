from django.shortcuts import render
from django.http import HttpResponse
import os

def home(request):
    """
    Serve the portfolio homepage - reads HTML from rajeev_rahul_portfolio folder
    and serves it with corrected static file paths
    """
    # Find the portfolio HTML file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Try different possible paths
    possible_paths = [
        os.path.join(base_dir, '..', 'djangoprojects', 'rajeev_rahul_portfolio', 'index.html'),
        os.path.join(base_dir, 'djangoprojects', 'rajeev_rahul_portfolio', 'index.html'),
        os.path.join('d:', 'djangoprojects', 'rajeev_rahul_portfolio', 'index.html'),
    ]
    
    html_content = None
    
    for path in possible_paths:
        normalized_path = os.path.normpath(path)
        if os.path.exists(normalized_path):
            with open(normalized_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            break
    
    if html_content:
        # Replace relative paths with Django static file paths
        html_content = html_content.replace('css/style.css', '/static/css/style.css')
        html_content = html_content.replace('js/script.js', '/static/js/script.js')
        
        return HttpResponse(html_content)
    else:
        # Show error message
        return HttpResponse("""
        <html>
        <head>
            <title>Error - Portfolio Not Found</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 50px; text-align: center; background: #B8E3E9; }
                h1 { color: #0B2E33; }
                p { color: #4F7C82; }
            </style>
        </head>
        <body>
            <h1>Portfolio Files Not Found</h1>
            <p>Please ensure rajeev_rahul_portfolio/index.html exists.</p>
            <p>Base dir: {}</p>
        </body>
        </html>
        """.format(base_dir), status=404)
