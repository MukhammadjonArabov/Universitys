import os

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('UzUniversitets', 'UzOTM').replace('UzUniversitet', 'UzOTM').replace('Uzuniversitet', 'UzOTM')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            replace_in_file(os.path.join(root, file))

replace_in_file('config/settings.py')
