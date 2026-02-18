from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.

def home(request):
    """
    Serve the portfolio homepage
    """
    # Direct path to portfolio HTML
    html_path = 'd:/djangoprojects/rajeev_rahul_portfolio/index.html'
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace relative paths with Django static file paths
        html_content = html_content.replace('css/style.css', '/static/css/style.css')
        html_content = html_content.replace('js/script.js', '/static/js/script.js')
        
        return HttpResponse(html_content)
    else:
        return HttpResponse("<h1>Portfolio Not Found</h1><p>Please ensure the portfolio files exist.</p>", status=404)
