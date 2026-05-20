import os
import shutil

# 1. Create directories
dirs = ['layouts', 'pages', 'auth', 'includes']
for d in dirs:
    os.makedirs(os.path.join('templates', d), exist_ok=True)

# 2. Define file mappings
file_moves = {
    'base.html': 'layouts/base.html',
    'home.html': 'pages/home.html',
    'universities.html': 'pages/universities.html',
    'university_detail.html': 'pages/university_detail.html',
    'resources.html': 'pages/resources.html',
    'test_intro.html': 'pages/test_intro.html',
    'test_process.html': 'pages/test_process.html',
    'test_result.html': 'pages/test_result.html',
    'login_telegram.html': 'auth/login_telegram.html',
    '_sidebar_filters.html': 'includes/_sidebar_filters.html',
    '_university_card.html': 'includes/_university_card.html'
}

# 3. Move files
for old, new in file_moves.items():
    src = os.path.join('templates', old)
    dest = os.path.join('templates', new)
    if os.path.exists(src):
        shutil.move(src, dest)
        print(f"Moved {old} to {new}")

# 4. Update file contents to reflect new paths
def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_str, new_str in replacements.items():
        content = content.replace(old_str, new_str)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

template_replacements = {
    '{% extends "base.html" %}': '{% extends "layouts/base.html" %}',
    "{% extends 'base.html' %}": '{% extends "layouts/base.html" %}',
    '{% include "_sidebar_filters.html"': '{% include "includes/_sidebar_filters.html"',
    '{% include "_university_card.html"': '{% include "includes/_university_card.html"'
}

for root, _, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            replace_in_file(os.path.join(root, file), template_replacements)
            print(f"Updated paths inside {file}")

# 5. Update views.py
views_replacements = {
    '"home.html"': '"pages/home.html"',
    "'home.html'": "'pages/home.html'",
    '"universities.html"': '"pages/universities.html"',
    "'universities.html'": "'pages/universities.html'",
    '"university_detail.html"': '"pages/university_detail.html"',
    "'university_detail.html'": "'pages/university_detail.html'",
    '"resources.html"': '"pages/resources.html"',
    "'resources.html'": "'pages/resources.html'",
    '"test_intro.html"': '"pages/test_intro.html"',
    "'test_intro.html'": "'pages/test_intro.html'",
    '"test_process.html"': '"pages/test_process.html"',
    "'test_process.html'": "'pages/test_process.html'",
    '"test_result.html"': '"pages/test_result.html"',
    "'test_result.html'": "'pages/test_result.html'",
    '"login_telegram.html"': '"auth/login_telegram.html"',
    "'login_telegram.html'": "'auth/login_telegram.html'",
}

replace_in_file(os.path.join('university', 'views.py'), views_replacements)
print("Updated views.py")

# 6. Update test_templates.py to prevent it from crashing when trying to render the base template.
# test_templates.py shouldn't render 'base.html' directly if it requires context.
test_replacements = {
    '"base.html"': '"layouts/base.html"',
    '"home.html"': '"pages/home.html"',
    '"universities.html"': '"pages/universities.html"',
    '"university_detail.html"': '"pages/university_detail.html"',
    '"resources.html"': '"pages/resources.html"',
    '"test_intro.html"': '"pages/test_intro.html"',
    '"test_process.html"': '"pages/test_process.html"',
    '"test_result.html"': '"pages/test_result.html"',
    '"login_telegram.html"': '"auth/login_telegram.html"'
}
replace_in_file('test_templates.py', test_replacements)
print("Updated test_templates.py")
