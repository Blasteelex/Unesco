import os

files = ['Nature_fr.html', 'Nature_en.html', 'Nature_sr.html']
base_dir = r"c:\Users\miodr\Desktop\resp²\V3 Responsive"

for filename in files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacements
    content = content.replace(
        '<div class="menu-escalier-nature" style="align-items: flex-start;">',
        '<div class="nature-layout">'
    )
    content = content.replace(
        '<div class="niveau-haut" onclick="ouvrirTiroir(\'tiroir-gauche\')">',
        '<div class="nature-layout-gauche" onclick="ouvrirTiroir(\'tiroir-gauche\')">'
    )
    content = content.replace(
        '<div class="conteneur-bulle-centre niveau-moyen" style="flex: 1; min-width: 300px; display: flex; justify-content: center;">',
        '<div class="nature-layout-centre">'
    )
    content = content.replace(
        '<div class="bulle-info-centre" style="margin: 0; width: 100%; max-width: 450px;">',
        '<div class="bulle-info-centre bulle-info-nature-layout" style="margin: 0;">'
    )
    content = content.replace(
        '<div class="niveau-bas" onclick="ouvrirTiroir(\'tiroir-droite\')">',
        '<div class="nature-layout-droite" onclick="ouvrirTiroir(\'tiroir-droite\')">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Patched {filepath}")
