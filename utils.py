import os
def load_payload_templates(template_root="templates"):
    templates = []

    for root, dirs, files in os.walk(template_root):
        for file in files:
            if file.endswith((".py", ".sh", ".c", ".ps1")):
                rel_path = os.path.relpath(os.path.join(root, file), template_root)
                templates.append(rel_path)
    return sorted(templates)