import os
import sys
import django
from django.conf import settings

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_dir)
sys.path.insert(0, parent_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuildKart.settings')
django.setup()

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
