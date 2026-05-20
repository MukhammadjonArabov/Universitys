import os
import polib

def compile_po_to_mo(locale_dir):
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                po_path = os.path.join(root, file)
                mo_path = po_path[:-3] + '.mo'
                po = polib.pofile(po_path)
                po.save_as_mofile(mo_path)
                print(f"Compiled {po_path} -> {mo_path}")

if __name__ == "__main__":
    locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
    compile_po_to_mo(locale_dir)
