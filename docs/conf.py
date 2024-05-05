import sys
import os


sys.path.insert(0, os.path.abspath(".."))

project = "PhotoBank by Drujba"
copyright = "2024, Drujba team"
author = "Drujba team"


extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "bizstyle"
html_static_path = ["_static"]
