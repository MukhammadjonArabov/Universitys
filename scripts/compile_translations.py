"""
Compile all .po files to .mo files.
Run from project root: python scripts/compile_translations.py
"""
import sys
import os

# Setup Django path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
import polib

LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'locale')

# New strings to add before compilation
NEW_STRINGS = {
    'ru': [
        ("Oxirgi natijamni ko'rish", "Посмотреть мой последний результат"),
        ("Natija", "Результат"),
    ],
    'en': [
        ("Oxirgi natijamni ko'rish", "View My Last Result"),
        ("Natija", "Result"),
    ],
}

def add_missing_strings():
    for lang, strings in NEW_STRINGS.items():
        po_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
        if not os.path.exists(po_path):
            print(f"  SKIP: {po_path} not found")
            continue
        po = polib.pofile(po_path)
        existing = {e.msgid for e in po}
        added = 0
        for msgid, msgstr in strings:
            if msgid not in existing:
                entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
                po.append(entry)
                added += 1
        po.save(po_path)
        print(f"  Updated {po_path} (+{added} new entries)")

def compile_all():
    for lang in ('uz', 'ru', 'en'):
        po_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.mo')
        if not os.path.exists(po_path):
            print(f"  SKIP: {po_path} not found")
            continue
        with open(po_path, 'rb') as f:
            catalog = read_po(f)
        with open(mo_path, 'wb') as f:
            write_mo(f, catalog)
        print(f"  Compiled: {mo_path} ({len(catalog)} entries)")

if __name__ == '__main__':
    print("=== Adding missing strings ===")
    add_missing_strings()
    print("\n=== Compiling .mo files ===")
    compile_all()
    print("\nDone!")
