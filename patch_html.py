import os
import glob

def patch_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched with burger
    if 'id="check-burger"' not in content:
        # Patch <body>
        body_patch = '<body>\n    <div id="ecran-fond" onclick="fermerTousTiroirs()"></div>\n    <input type="checkbox" id="check-burger" style="display:none;">'
        content = content.replace('<body>', body_patch, 1)

        # Patch <header>
        header_patch = '<header>\n        <label for="check-burger" class="btn-burger"></label>'
        content = content.replace('<header>', header_patch, 1)

    # Patch modals background click
    if 'class="label-fond-fermer"' not in content:
        # Replace '<div class="boite-modal">' with the label and then the div itself.
        boite_modal_str = '<div class="boite-modal">'
        boite_modal_patch = '<label for="fermer-tout" class="label-fond-fermer"></label>\n            <div class="boite-modal">'
        content = content.replace(boite_modal_str, boite_modal_patch)
    if 'id="modal-image-generique"' not in content:
        img_modal_html = """
    <!-- Modal générique pour les images -->
    <div class="calque-modal" id="modal-image-generique">
        <div class="label-fond-fermer" onclick="fermerModalImage()"></div>
        <div class="boite-modal boite-image-modal">
            <label class="btn-fermer" onclick="fermerModalImage()">✖</label>
            <img id="image-en-grand" src="" alt="Image agrandie">
        </div>
    </div>
    
    <script>
        function fermerModalImage() {
            document.getElementById('modal-image-generique').classList.remove('actif');
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            const images = document.querySelectorAll('img:not(#image-en-grand):not(.header-logo img):not(.conteneur-logo img):not(footer img)');
            images.forEach(img => {
                img.style.cursor = 'pointer';
                img.addEventListener('click', function(e) {
                    e.stopPropagation(); // Évite de déclencher d'autres clics
                    const modal = document.getElementById('modal-image-generique');
                    const imgEnGrand = document.getElementById('image-en-grand');
                    imgEnGrand.src = this.src;
                    modal.classList.add('actif');
                });
            });
        });
    </script>
</body>"""
        content = content.replace('</body>', img_modal_html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

base_dir = r"c:\Users\miodr\Desktop\resp²"
html_files = glob.glob(os.path.join(base_dir, "*.html")) + glob.glob(os.path.join(base_dir, "V3 Responsive", "*.html"))

for f in html_files:
    patch_html(f)
