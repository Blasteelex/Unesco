import os
import re

files_dir = r"C:\Users\miodr\Desktop\Réalisation définitive des 3 pages codées passage au 2 pages supplémentaires"

langs = {
    'fr': {'src': 'Histoire_fr.html', 'title_frise': 'Projet Unesco - Frise', 'title_carte': 'Projet Unesco - Carte et réservations', 'h2_frise': 'Frise chronologique', 'h2_carte': 'Carte et réservations', 'p_frise': 'Contenu de la frise chronologique à venir...', 'p_carte': 'Contenu de la carte et des réservations à venir...', 'nav_frise': 'Frise_fr.html', 'nav_carte': 'Carte_fr.html'},
    'en': {'src': 'Nature_en.html', 'title_frise': 'Unesco Project - Timeline', 'title_carte': 'Unesco Project - Map & Booking', 'h2_frise': 'Timeline', 'h2_carte': 'Map & Booking', 'p_frise': 'Timeline content coming soon...', 'p_carte': 'Map and booking content coming soon...', 'nav_frise': 'Frise_en.html', 'nav_carte': 'Carte_en.html'},
    'sr': {'src': 'Histoire_sr.html', 'title_frise': 'Пројекат Унеско - Ере', 'title_carte': 'Пројекат Унеско - Мапе и резервације', 'h2_frise': 'Ере', 'h2_carte': 'Мапе и резервације', 'p_frise': 'Садржај ера ускоро...', 'p_carte': 'Садржај мапа и резервација ускоро...', 'nav_frise': 'Frise_sr.html', 'nav_carte': 'Carte_sr.html'}
}

for target in ['Frise', 'Carte']:
    for lang in ['fr', 'en', 'sr']:
        src_file = os.path.join(files_dir, langs[lang]['src'])
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Update <title>
        new_title = langs[lang][f'title_{target.lower()}']
        content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content, flags=re.IGNORECASE)
        
        # 2. Update <main>
        h2 = langs[lang][f'h2_{target.lower()}']
        p = langs[lang][f'p_{target.lower()}']
        new_main = f'''<main>
        <div class="titre-principal">
            <h2 class="police-dyno">{h2}</h2>
            <p class="police-cicle">{p}</p>
        </div>
        <div style="height: 50vh; display: flex; align-items: center; justify-content: center;">
            <p class="police-cicle" style="font-size: 1.5rem; text-align: center;">{p}</p>
        </div>
    </main>'''
        content = re.sub(r'<main>.*?</main>', new_main, content, flags=re.IGNORECASE | re.DOTALL)
        
        # 3. Update nav active class
        content = re.sub(r'\s*class="actif"', '', content)
        target_nav = langs[lang][f'nav_{target.lower()}']
        content = re.sub(f'(<a href="{target_nav}")', r'\1 class="actif"', content)
        
        # 4. Update language switcher
        def replace_lang_links(match):
            div_content = match.group(0)
            div_content = re.sub(r'href="[^"]*_fr\.html"', f'href="{target}_fr.html"', div_content)
            div_content = re.sub(r'href="[^"]*_en\.html"', f'href="{target}_en.html"', div_content)
            div_content = re.sub(r'href="[^"]*_sr\.html"', f'href="{target}_sr.html"', div_content)
            div_content = re.sub(r'href="index\.html"', f'href="{target}_fr.html"', div_content)
            return div_content

        content = re.sub(r'(<div class="calque-modal"[^>]*id="fenetre-langue".*?</div>\s*</div>\s*</div>)', replace_lang_links, content, flags=re.DOTALL)

        out_file = os.path.join(files_dir, f'{target}_{lang}.html')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Generation complete")
