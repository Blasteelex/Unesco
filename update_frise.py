import os
import re

files_dir = r"C:\Users\miodr\Desktop\Réalisation définitive des 3 pages codées passage au 2 pages supplémentaires"

html_template = '''<main class="frise-main">
        <div class="encart-central-frise">
            <div class="btn-gros-frise" onclick="ouvrirBande('geo')">{btn_geo}</div>
            <div class="titre-centre-frise">{titre_centre}</div>
            <div class="btn-gros-frise" onclick="ouvrirBande('histo')">{btn_histo}</div>
        </div>

        <!-- Bande Géologie -->
        <div id="bande-geo" class="bande-frise bande-frise-geo">
            <div class="bande-frise-titre">{bande_geo_titre}</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 6, '{lang}', event)">6</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 5, '{lang}', event)">5</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 4, '{lang}', event)">4</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 3, '{lang}', event)">3</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 2, '{lang}', event)">2</div>
            <div class="point-frise" onclick="ouvrirDetail('geo', 1, '{lang}', event)">1</div>
        </div>

        <!-- Bande Histoire -->
        <div id="bande-histo" class="bande-frise bande-frise-histo">
            <div class="point-frise" onclick="ouvrirDetail('histo', 1, '{lang}', event)">1</div>
            <div class="point-frise" onclick="ouvrirDetail('histo', 2, '{lang}', event)">2</div>
            <div class="point-frise" onclick="ouvrirDetail('histo', 3, '{lang}', event)">3</div>
            <div class="point-frise" onclick="ouvrirDetail('histo', 4, '{lang}', event)">4</div>
            <div class="point-frise" onclick="ouvrirDetail('histo', 5, '{lang}', event)">5</div>
            <div class="point-frise" onclick="ouvrirDetail('histo', 6, '{lang}', event)">6</div>
            <div class="bande-frise-titre">{bande_histo_titre}</div>
        </div>

        <!-- Panneau de détail -->
        <div id="panneau-detail" class="panneau-detail-frise">
            <div class="btn-fermer-detail" onclick="fermerDetail()">✖</div>
            <div class="detail-entete">
                <div id="detail-dates" class="dates"></div>
                <div id="detail-titre" class="titre-evenement"></div>
            </div>
            <div class="detail-corps" id="detail-texte"></div>
        </div>
    </main>'''

script_js = '''
    <script>
        const donneesFrise = {
            'fr': {
                'geo': [
                    {dates: '-2 milliards d\\'années :', titre: 'Les roches les plus anciennes', texte: 'Formation du socle métamorphique (Vishnu Basement Rocks).<br>Pression + chaleur -> gneiss, schistes, granites.<br>Base du canyon.'},
                    {dates: '-1,2 à -0,7 milliard d\\'années :', titre: 'Le Grand Canyon Supergroup', texte: 'Dépôts sédimentaires inclinés.<br>Anciennes mers peu profondes, boues, sables -> roches sédimentaires.<br>Failles + soulèvement -> couches penchées.'},
                    {dates: '-525 à -270 millions d\\'années :', titre: 'Les couches paléozoïques', texte: '40 couches horizontales.<br>Alternance de :<br>- mers peu profondes (calcaires)<br>- plages (grès)<br>- déserts fossiles (dunes -> grès cross-bedding)<br>Formation des grandes couleurs du canyon.'},
                    {dates: '-70 à -10 millions d\\'années :', titre: 'Soulèvement du plateau du Colorado', texte: 'Montée progressive du plateau -> augmentation<br>de la pente des rivières.<br>Le futur canyon est prêt à être creusé.'},
                    {dates: '-6 millions d\\'années :', titre: 'Le fleuve Colorado commence à tailler', texte: 'L\\'eau + les débris transportés = érosion massive.<br>Creusement vertical ultra rapide.'},
                    {dates: '-2 millions d\\'années à aujourd\\'hui :', titre: 'Sculptures finales', texte: 'Gel/dégel, pluie, ruissellement, effondrements.<br>Les parois se creusent et s\\'élargissent.<br>Apparition du canyon actuel.'}
                ],
                'histo': [
                    {dates: '-12 000 ans :', titre: 'Premières présences humaines', texte: 'Arrivée de groupes paléo-indiens.<br>Campements de chasseurs-cueilleurs dans les plateaux et vallées autour du canyon.'},
                    {dates: '-4 000 à -1 000 ans :', titre: 'Les cultures archaïques', texte: 'Développement de techniques de survie adaptées au climat sec.<br>Premiers paniers, outils, habitats simples.<br>Début d\\'une occupation plus stable.'},
                    {dates: '-1 000 à 700 ans :', titre: 'Les Anasazis / Ancestral Puebloans', texte: 'Construction de villages, greniers, poteries.<br>Agriculture (maïs, haricots, courges).<br>Traces visibles dans les grottes et falaises du canyon.<br>Culture avancée et structurée.'},
                    {dates: '700 à 200 ans :', titre: 'Hopis, Païutes, Navajos', texte: 'Les peuples autochtones actuels s\\'implantent autour du canyon.<br>Traditions, mythes, pratiques spirituelles liées aux lieux.<br>Le canyon comme territoire sacré.'},
                    {dates: '1540-1850 :', titre: 'Explorateurs européens', texte: '1540 : arrivée de Garcia Lopez de Cardenas (expédition espagnole).<br>Peu d\\'explorations ensuite : terrain trop difficile.<br>Quelques missions et repérages à partir du XIXe siècle.'},
                    {dates: '1869 à aujourd\\'hui :', titre: 'Expéditions scientifiques -> Parc National', texte: '1869 : expédition de John Wesley Powell, première navigation complète du Colorado.<br>Études géologiques + cartographie -> reconnaissance mondiale.<br>1919 : création du Grand Canyon National Park.<br>Aujourd\\'hui : site UNESCO, millions de visiteurs/an, protection renforcée.'}
                ]
            },
            'en': {
                'geo': [
                    {dates: '-2 billion years:', titre: 'The Oldest Rocks', texte: 'Formation of the metamorphic basement (Vishnu Basement Rocks).<br>Pressure + heat -> gneiss, schists, granites.<br>Base of the canyon.'},
                    {dates: '-1.2 to -0.7 billion years:', titre: 'Grand Canyon Supergroup', texte: 'Tilted sedimentary deposits.<br>Ancient shallow seas, muds, sands -> sedimentary rocks.<br>Faults + uplift -> tilted layers.'},
                    {dates: '-525 to -270 million years:', titre: 'Paleozoic Layers', texte: '40 horizontal layers.<br>Alternation of:<br>- shallow seas (limestones)<br>- beaches (sandstones)<br>- fossil deserts (dunes -> cross-bedding sandstone)<br>Formation of the great canyon colors.'},
                    {dates: '-70 to -10 million years:', titre: 'Colorado Plateau Uplift', texte: 'Progressive uplift of the plateau -> increase<br>in river steepness.<br>The future canyon is ready to be carved.'},
                    {dates: '-6 million years:', titre: 'The Colorado River Begins to Carve', texte: 'Water + transported debris = massive erosion.<br>Ultra-fast vertical carving.'},
                    {dates: '-2 million years to present:', titre: 'Final Sculptures', texte: 'Freeze/thaw, rain, runoff, collapses.<br>The walls deepen and widen.<br>Appearance of the current canyon.'}
                ],
                'histo': [
                    {dates: '-12,000 years:', titre: 'First Human Presences', texte: 'Arrival of Paleo-Indian groups.<br>Hunter-gatherer camps in the plateaus and valleys around the canyon.'},
                    {dates: '-4,000 to -1,000 years:', titre: 'Archaic Cultures', texte: 'Development of survival techniques adapted to the dry climate.<br>First baskets, tools, simple habitats.<br>Beginning of more stable occupation.'},
                    {dates: '-1,000 to 700 years:', titre: 'Anasazi / Ancestral Puebloans', texte: 'Construction of villages, granaries, pottery.<br>Agriculture (corn, beans, squash).<br>Visible traces in the caves and cliffs of the canyon.<br>Advanced and structured culture.'},
                    {dates: '700 to 200 years:', titre: 'Hopi, Paiute, Navajo', texte: 'Current indigenous peoples settle around the canyon.<br>Traditions, myths, spiritual practices tied to the locations.<br>The canyon as a sacred territory.'},
                    {dates: '1540-1850:', titre: 'European Explorers', texte: '1540: arrival of Garcia Lopez de Cardenas (Spanish expedition).<br>Few explorations afterward: terrain too difficult.<br>Some missions and scouting from the 19th century.'},
                    {dates: '1869 to present:', titre: 'Scientific Expeditions -> National Park', texte: '1869: John Wesley Powell expedition, first complete navigation of the Colorado.<br>Geological studies + mapping -> worldwide recognition.<br>1919: creation of Grand Canyon National Park.<br>Today: UNESCO site, millions of visitors/year, reinforced protection.'}
                ]
            },
            'sr': {
                'geo': [
                    {dates: '-2 милијарде година:', titre: 'Најстарије стене', texte: 'Формација метаморфног подрума (Vishnu Basement Rocks).<br>Притисак + топлота -> гнајс, шкриљци, гранити.<br>База кањона.'},
                    {dates: '-1.2 до -0.7 милијарди година:', titre: 'Grand Canyon Supergroup', texte: 'Нагнути седиментни депозити.<br>Древна плитка мора, муљ, песак -> седиментне стене.<br>Раседи + издизање -> нагнути слојеви.'},
                    {dates: '-525 до -270 милиона година:', titre: 'Палеозојски слојеви', texte: '40 хоризонталних слојева.<br>Алтернација:<br>- плитка мора (кречњаци)<br>- плаже (пешчари)<br>- фосилне пустиње (дине -> укрштени пешчари)<br>Формација великих боја кањона.'},
                    {dates: '-70 до -10 милиона година:', titre: 'Издизање Колорадо платоа', texte: 'Прогресивно издизање платоа -> повећање<br>нагиба река.<br>Будући кањон је спреман за клесање.'},
                    {dates: '-6 милиона година:', titre: 'Река Колорадо почиње да клеше', texte: 'Вода + транспортовани остаци = масивна ерозија.<br>Изузетно брзо вертикално клесање.'},
                    {dates: '-2 милиона година до данас:', titre: 'Финалне скулптуре', texte: 'Замрзавање/одмрзавање, киша, отицање, урушавања.<br>Зидови се продубљују и шире.<br>Изглед тренутног кањона.'}
                ],
                'histo': [
                    {dates: '-12,000 година:', titre: 'Прво људско присуство', texte: 'Долазак палео-индијанских група.<br>Кампови ловаца-сакупљача на платоима и долинама око кањона.'},
                    {dates: '-4,000 до -1,000 година:', titre: 'Архаичне културе', texte: 'Развој техника преживљавања прилагођених сувој клими.<br>Прве корпе, алати, једноставна станишта.<br>Почетак стабилније окупације.'},
                    {dates: '-1,000 до 700 година:', titre: 'Анасази / Ancestral Puebloans', texte: 'Изградња села, житница, грнчарије.<br>Пољопривреда (кукуруз, пасуљ, тиквице).<br>Видљиви трагови у пећинама и литицама кањона.<br>Напредна и структурирана култура.'},
                    {dates: '700 до 200 година:', titre: 'Хопи, Пајути, Навахо', texte: 'Тренутни аутохтони народи се насељавају око кањона.<br>Традиције, митови, духовне праксе везане за локације.<br>Кањон као света територија.'},
                    {dates: '1540-1850:', titre: 'Европски истраживачи', texte: '1540: долазак Гарсије Лопеза де Карденаса (шпанска експедиција).<br>Мало истраживања након тога: терен превише тежак.<br>Неке мисије и извиђања од 19. века.'},
                    {dates: '1869 до данас:', titre: 'Научне експедиције -> Национални парк', texte: '1869: експедиција Џона Веслија Пауела, прва комплетна навигација Колорада.<br>Геолошке студије + мапирање -> светско признање.<br>1919: стварање Националног парка Велики кањон.<br>Данас: УНЕСКО сајт, милиони посетилаца/годишње, појачана заштита.'}
                ]
            }
        };

        let bandeActive = null;

        function ouvrirBande(type) {
            fermerDetail();
            document.querySelectorAll('.point-frise').forEach(p => p.classList.remove('selectionne'));
            
            const bandeGeo = document.getElementById('bande-geo');
            const bandeHisto = document.getElementById('bande-histo');

            if (type === 'geo') {
                if(bandeActive === 'geo') {
                    bandeGeo.classList.remove('actif');
                    bandeActive = null;
                } else {
                    bandeHisto.classList.remove('actif');
                    bandeGeo.classList.add('actif');
                    bandeActive = 'geo';
                }
            } else if (type === 'histo') {
                if(bandeActive === 'histo') {
                    bandeHisto.classList.remove('actif');
                    bandeActive = null;
                } else {
                    bandeGeo.classList.remove('actif');
                    bandeHisto.classList.add('actif');
                    bandeActive = 'histo';
                }
            }
        }

        function ouvrirDetail(type, index, lang, event) {
            const donnees = donneesFrise[lang][type][index - 1]; 
            
            document.getElementById('detail-dates').innerText = donnees.dates;
            document.getElementById('detail-titre').innerText = donnees.titre;
            document.getElementById('detail-texte').innerHTML = donnees.texte;

            document.getElementById('panneau-detail').classList.add('actif');

            document.querySelectorAll('.point-frise').forEach(p => p.classList.remove('selectionne'));
            event.target.classList.add('selectionne');
        }

        function fermerDetail() {
            document.getElementById('panneau-detail').classList.remove('actif');
            document.querySelectorAll('.point-frise').forEach(p => p.classList.remove('selectionne'));
        }
    </script>
'''

config = {
    'fr': {
        'btn_geo': 'Géologie',
        'titre_centre': 'La frise',
        'btn_histo': 'Histoire',
        'bande_geo_titre': 'Flèche géologique',
        'bande_histo_titre': 'FRISE'
    },
    'en': {
        'btn_geo': 'Geology',
        'titre_centre': 'The Timeline',
        'btn_histo': 'History',
        'bande_geo_titre': 'Geological Arrow',
        'bande_histo_titre': 'TIMELINE'
    },
    'sr': {
        'btn_geo': 'Геологија',
        'titre_centre': 'Ере',
        'btn_histo': 'Историја',
        'bande_geo_titre': 'Геолошка стрелица',
        'bande_histo_titre': 'ЕРЕ'
    }
}

for lang in ['fr', 'en', 'sr']:
    file_path = os.path.join(files_dir, f'Frise_{lang}.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace <main>
    html_filled = html_template.format(
        btn_geo=config[lang]['btn_geo'],
        titre_centre=config[lang]['titre_centre'],
        btn_histo=config[lang]['btn_histo'],
        bande_geo_titre=config[lang]['bande_geo_titre'],
        bande_histo_titre=config[lang]['bande_histo_titre'],
        lang=lang
    )
    content = re.sub(r'<main>.*?</main>', html_filled, content, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Add background image class to body if not exist
    if 'style="background:' not in content:
        content = re.sub(r'<body[^>]*>', '<body style="background: url(\\'images/Grand_Canyon.jpg\\') no-repeat center center fixed; background-size: cover;">', content)
    
    # 3. Add script at the end
    if 'const donneesFrise =' not in content:
        content = content.replace('</body>', script_js + '\\n</body>')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{lang} done')
