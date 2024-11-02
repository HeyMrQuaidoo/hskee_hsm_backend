import os

# Templates
# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Build the path to the templates directory
template_path = os.path.join(current_dir, "..", "templates")

# Normalize the path (replace backslashes with forward slashes)
template_path = os.path.normpath(template_path)
