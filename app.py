import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(
    page_title="Menu Familial Kawaii 🍓",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CSS DESIGN PASTEL & KAWAII
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #FAF7F2; }
    
    .kawaii-header {
        background: linear-gradient(135deg, #FFD1DC 0%, #E6E6FA 50%, #D4F1F4 100%);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 209, 220, 0.4);
        margin-bottom: 20px;
    }
    .kawaii-title { font-size: 2.1rem; font-weight: 800; color: #4A3E3D; margin: 0; }
    
    .grid-slot-filled {
        border-radius: 14px;
        padding: 8px;
        min-height: 80px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .slot-petit-dej { background-color: #FFF9DB; border-left: 5px solid #FCC419; }
    .slot-dejeuner { background-color: #E6FCF5; border-left: 5px solid #20C997; }
    .slot-gouter { background-color: #FFF0F6; border-left: 5px solid #FAA2C1; }
    .slot-diner { background-color: #F3F0FF; border-left: 5px solid #845EF7; }
    
    .meal-title-text { font-size: 0.85rem; font-weight: 800; color: #343A40; margin-bottom: 4px; line-height: 1.2; }
    
    .avatar-chip {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 700;
        color: white;
        margin: 1px;
    }
    .chip-maman { background-color: #FF85A1; }
    .chip-papa { background-color: #4EA8DE; }
    .chip-lea { background-color: #B5179E; }
    .chip-default { background-color: #7209B7; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FONCTIONS SYNCHRO GSHEET
# ---------------------------------------------------------
def sync_load_from_gsheet(url):
    if not url:
        return False
    try:
        res = requests.get(url, timeout=5).json()
        if "Planning" in res and len(res["Planning"]) > 0:
            st.session_state['planning'] = pd.DataFrame(res["Planning"])
        if "Profils" in res and len(res["Profils"]) > 0:
            st.session_state['profils'] = pd.DataFrame(res["Profils"])
        if "Recettes" in res and len(res["Recettes"]) > 0:
            st.session_state['recettes'] = pd.DataFrame(res["Recettes"])
        return True
    except Exception as e:
        st.error(f"Erreur de chargement Google Sheet : {e}")
        return False

def save_to_gsheet(url, sheet_name, df):
    if not url:
        st.warning("⚠️ Ajoute l'URL de ton Google Sheet dans la barre latérale pour sauvegarder en ligne.")
        return False
    try:
        payload = {
            "sheet_name": sheet_name,
            "rows": df.to_dict(orient="records")
        }
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code == 200:
            st.toast(f"✅ Synchro Google Sheet ({sheet_name}) effectuée !", icon="🎉")
            return True
        else:
            st.error("Erreur lors de la sauvegarde.")
            return False
    except Exception as e:
        st.error(f"Erreur d'envoi vers Google Sheet : {e}")
        return False

# ---------------------------------------------------------
# INITIALISATION DES DONNÉES LOCALES
# ---------------------------------------------------------
if 'profils' not in st.session_state:
    st.session_state['profils'] = pd.DataFrame([
        {"Nom": "Maman", "Initiale": "M", "Couleur_Chip": "chip-maman", "Objectif_Cal": "1800 kcal", "Fer": "Élevé"},
        {"Nom": "Papa", "Initiale": "P", "Couleur_Chip": "chip-papa", "Objectif_Cal": "2400 kcal", "Fer": "Normal"},
        {"Nom": "Léa", "Initiale": "L", "Couleur_Chip": "chip-lea", "Objectif_Cal": "1500 kcal", "Fer": "Modéré"}
    ])

if 'recettes' not in st.session_state:
    st.session_state['recettes'] = pd.DataFrame([
        {"Nom": "Pâtes à la Carbonara", "Catégorie": "Pâtes", "Temps": "15 min", "Calories": "550 kcal", "Ingrédients": "400g spaghetti, 200g lardons, 4 œufs, 100g parmesan, poivre"},
        {"Nom": "Saumon Poêlé & Riz Basmati", "Catégorie": "Poisson", "Temps": "20 min", "Calories": "480 kcal", "Ingrédients": "4 pavés de saumon, 300g riz basmati, 1 citron, aneth, huile d'olive"},
        {"Nom": "Dahl de Lentilles Corail", "Catégorie": "Végétarien", "Temps": "25 min", "Calories": "380 kcal", "Ingrédients": "300g lentilles corail, 1 brique lait de coco, 1 oignon, épices curry, 400g tomates concassées"},
        {"Nom": "Bowl Açaï & Fruits Frais", "Catégorie": "Petit-déj", "Temps": "10 min", "Calories": "310 kcal", "Ingrédients": "2 bananes, 150g fruits rouges, 20cl lait d'amande, granola, graines de chia"},
        {"Nom": "Pancakes Banane & Miel", "Catégorie": "Goûter", "Temps": "15 min", "Calories": "280 kcal", "Ingrédients": "200g farine, 2 bananes, 2 œufs, 25cl lait, miel"},
        {"Nom": "Poulet Rôti & Patates Douces", "Catégorie": "Volaille", "Temps": "35 min", "Calories": "520 kcal", "Ingrédients": "1 poulet entier, 800g patates douces, herbes de provence, huile d'olive"},
        {"Nom": "Omelette BIO & Avocat", "Catégorie": "Végétarien", "Temps": "10 min", "Calories": "340 kcal", "Ingrédients": "6 œufs bio, 2 avocats, salade verte, beurre"}
    ])

if 'planning' not in st.session_state:
    st.session_state['planning'] = pd.DataFrame([
        {"Jour": "Sam", "Creneau": "Déjeuner", "Nom_Profil": "Papa", "Nom_Repas": "Pâtes à la Carbonara", "Portion": "125%"},
        {"Jour": "Sam", "Creneau": "Déjeuner", "Nom_Profil": "Léa", "Nom_Repas": "Pâtes à la Carbonara", "Portion": "100%"},
        {"Jour": "Lun", "Creneau": "Dîner", "Nom_Profil": "Maman", "Nom_Repas": "Dahl de Lentilles Corail", "Portion": "100%"},
        {"Jour": "Lun", "Creneau": "Dîner", "Nom_Profil": "Papa", "Nom_Repas": "Dahl de Lentilles Corail", "Portion": "125%"}
    ])

if 'selected_slot' not in st.session_state:
    st.session_state['selected_slot'] = None

# Header Kawaii
st.markdown("""
<div class="kawaii-header">
    <div class="kawaii-title">🌸 Mon Menu Familial Kawaii 🍓</div>
</div>
""", unsafe_allow_html=True)

# Barre latérale & Synchronisation
with st.sidebar:
    st.title("⚙️ Synchronisation")
    gsheet_url = st.text_input("URL Google Apps Script :", key="gsheet_url_input")
    
    st.markdown("---")
    if st.button("🔄 Rafraîchir tout depuis Google Sheet", use_container_width=True):
        if sync_load_from_gsheet(gsheet_url):
            st.success("Toutes les données ont été rechargées !")
            st.rerun()

    if st.button("💾 Sauvegarder TOUT sur Google Sheet", use_container_width=True):
        save_to_gsheet(gsheet_url, "Planning", st.session_state['planning'])
        save_to_gsheet(gsheet_url, "Profils", st.session_state['profils'])
        save_to_gsheet(gsheet_url, "Recettes", st.session_state['recettes'])

# Navigation par Onglets
tabs = st.tabs([
    "🗓️ Le Planning", 
    "👥 Profils Familiaux", 
    "🍱 Base de Recettes", 
    "📊 Micronutriments", 
    "🛒 Liste de Courses & IA"
])

jours_map = [
    {"code": "Lun", "date": "14/09"}, {"code": "Mar", "date": "15/09"},
    {"code": "Mer", "date": "16/09"}, {"code": "Jeu", "date": "17/09"},
    {"code": "Ven", "date": "18/09"}, {"code": "Sam", "date": "19/09"},
    {"code": "Dim", "date": "20/09"}
]

# ---------------------------------------------------------
# TAB 1: PLANNING
# ---------------------------------------------------------
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cm, ct, cp = st.columns([1, 4, 1])
        cm.button("‹", key="prev_wk", use_container_width=True)
        ct.markdown("<h3 style='text-align:center; color:#4A3E3D; margin:0;'>14/09 ➔ 20/09</h3>", unsafe_allow_html=True)
        cp.button("›", key="next_wk", use_container_width=True)

    if st.button("✨ Générer automatiquement TOUTE la semaine", use_container_width=True):
        recettes_dispo = st.session_state['recettes']['Nom'].tolist()
        profils_dispo = st.session_state['profils']['Nom'].tolist()
        
        if len(recettes_dispo) > 0 and len(profils_dispo) > 0:
            nouvelles_entrées = []
            creneaux_a_generer = ["Petit-déj", "Déjeuner", "Goûter", "Dîner"]
            
            for j in jours_map:
                for cr in creneaux_a_generer:
                    plat = random.choice(recettes_dispo)
                    for prof in profils_dispo:
                        nouvelles_entrées.append({
                            "Jour": j["code"],
                            "Creneau": cr,
                            "Nom_Profil": prof,
                            "Nom_Repas": plat,
                            "Portion": "100%"
                        })
            
            st.session_state['planning'] = pd.DataFrame(nouvelles_entrées)
            save_to_gsheet(gsheet_url, "Planning", st.session_state['planning'])
            st.balloons()
            st.success("Toute la semaine a été générée avec succès sur tous les créneaux !")
            st.rerun()

    st.write("")

    creneaux_info = [
        {"nom": "Petit-déj", "css": "slot-petit-dej"},
        {"nom": "Déjeuner", "css": "slot-dejeuner"},
        {"nom": "Goûter", "css": "slot-gouter"},
        {"nom": "Dîner", "css": "slot-diner"}
    ]

    cols_header = st.columns([1.2] + [1]*7)
    cols_header[0].write("")
    for i, j in enumerate(jours_map):
        cols_header[i+1].markdown(f"<div style='text-align:center; font-weight:800; color:#5C4B51;'>{j['code']}<br><span style='font-size:0.8rem; color:#A799B7;'>{j['date']}</span></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #FFE5EC;'>", unsafe_allow_html=True)

    for c_info in creneaux_info:
        c_nom = c_info["nom"]
        c_css = c_info["css"]
        
        row_cols = st.columns([1.2] + [1]*7)
        row_cols[0].markdown(f"<p style='font-weight:800; color:#4A3E3D; margin-top:15px;'>{c_nom}</p>", unsafe_allow_html=True)
        
        for i, j in enumerate(jours_map):
            j_code = j["code"]
            df_cell = st.session_state['planning'][
                (st.session_state['planning']['Jour'] == j_code) & 
                (st.session_state['planning']['Creneau'] == c_nom)
            ]
            
            with row_cols[i+1]:
                if df_cell.empty:
                    if st.button("➕", key=f"btn_{j_code}_{c_nom}", use_container_width=True):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": c_nom}
                        st.rerun()
                else:
                    nom_repas = df_cell['Nom_Repas'].iloc[0]
                    membres = df_cell['Nom_Profil'].tolist()
                    
                    chips_html = ""
                    for m in membres:
                        match_p = st.session_state['profils'][st.session_state['profils']['Nom'] == m]
                        chip_cls = match_p['Couleur_Chip'].values[0] if not match_p.empty else "chip-default"
                        initiale = match_p['Initiale'].values[0] if not match_p.empty else m[0]
                        chips_html += f'<span class="avatar-chip {chip_cls}">{initiale}</span>'
                    
                    st.markdown(f'''
                        <div class="grid-slot-filled {c_css}">
                            <div class="meal-title-text">{nom_repas}</div>
                            <div>{chips_html}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    if st.button("✏️", key=f"edit_{j_code}_{c_nom}"):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": c_nom}
                        st.rerun()

    if st.session_state['selected_slot']:
        slot = st.session_state['selected_slot']
        st.markdown("<hr style='border:1px solid #FFD1DC;'>", unsafe_allow_html=True)
        st.subheader(f"🌸 Modifier : {slot['jour']} — {slot['creneau']}")
        
        with st.form("form_slot_edit"):
            repas_choisi = st.selectbox("Choisir une recette :", options=st.session_state['recettes']['Nom'].tolist())
            repas_custom = st.text_input("Ou saisir un repas personnalisé :", value="")
            repas_final = repas_custom if repas_custom.strip() != "" else repas_choisi
            
            profils_sel = st.multiselect("Membres :", options=st.session_state['profils']['Nom'].tolist(), default=st.session_state['profils']['Nom'].tolist())
            portion = st.selectbox("Portion :", ["100%", "125%", "75%"])
            
            b1, b2, b3 = st.columns([1, 1, 2])
            if b1.form_submit_button("💾 Enregistrer"):
                st.session_state['planning'] = st.session_state['planning'][
                    ~((st.session_state['planning']['Jour'] == slot['jour']) & 
                      (st.session_state['planning']['Creneau'] == slot['creneau']))
                ]
                new_r = []
                for p in profils_sel:
                    new_r.append({"Jour": slot['jour'], "Creneau": slot['creneau'], "Nom_Profil": p, "Nom_Repas": repas_final, "Portion": portion})
                st.session_state['planning'] = pd.concat([st.session_state['planning'], pd.DataFrame(new_r)], ignore_index=True)
                save_to_gsheet(gsheet_url, "Planning", st.session_state['planning'])
                st.session_state['selected_slot'] = None
                st.rerun()
                
            if b2.form_submit_button("🗑️ Effacer"):
                st.session_state['planning'] = st.session_state['planning'][
                    ~((st.session_state['planning']['Jour'] == slot['jour']) & 
                      (st.session_state['planning']['Creneau'] == slot['creneau']))
                ]
                save_to_gsheet(gsheet_url, "Planning", st.session_state['planning'])
                st.session_state['selected_slot'] = None
                st.rerun()

            if b3.form_submit_button("❌ Annuler"):
                st.session_state['selected_slot'] = None
                st.rerun()

# ---------------------------------------------------------
# TAB 2: PROFILS
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("👥 Éditeur des Profils Familiaux")
    
    edited_profils = st.data_editor(st.session_state['profils'], num_rows="dynamic", use_container_width=True)
    if st.button("💾 Sauvegarder les Profils sur Google Sheet"):
        st.session_state['profils'] = edited_profils
        save_to_gsheet(gsheet_url, "Profils", edited_profils)

# ---------------------------------------------------------
# TAB 3: RECETTES & INGRÉDIENTS
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("🍱 Base de Recettes & Ingrédients")
    st.info("💡 Ajoute ou modifie le détail des ingrédients pour chaque recette ci-dessous.")
    
    edited_recettes = st.data_editor(st.session_state['recettes'], num_rows="dynamic", use_container_width=True)
    if st.button("💾 Sauvegarder les Recettes sur Google Sheet"):
        st.session_state['recettes'] = edited_recettes
        save_to_gsheet(gsheet_url, "Recettes", edited_recettes)

# ---------------------------------------------------------
# TAB 4: MICRONUTRIMENTS
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("📊 Bilan Nutritionnel")
    st.dataframe(st.session_state['profils'][['Nom', 'Objectif_Cal', 'Fer']], use_container_width=True)

# ---------------------------------------------------------
# TAB 5: LISTES DE COURSES (MAGASIN VS IA CARREFOUR)
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("🛒 Vos Listes de Courses")
    
    # Extraire les recettes planifiées
    repas_planifies = st.session_state['planning']['Nom_Repas'].unique().tolist()
    
    # Récupérer les ingrédients associés aux repas planifiés
    dict_ingredients = {}
    for repas in repas_planifies:
        match = st.session_state['recettes'][st.session_state['recettes']['Nom'] == repas]
        if not match.empty and 'Ingrédients' in match.columns:
            ing_str = str(match['Ingrédients'].values[0])
            items = [item.strip() for item in ing_str.split(',') if item.strip()]
            dict_ingredients[repas] = items
        else:
            dict_ingredients[repas] = ["Ingrédients non renseignés"]

    sub_tab1, sub_tab2 = st.tabs(["🛍️ Liste à cocher (Achats en magasin)", "🤖 Prompt pour IA Carrefour (Hopla / Drive)"])
    
    # -----------------------------------------------------
    # SUB-TAB 1: LISTE EN MAGASIN
    # -----------------------------------------------------
    with sub_tab1:
        st.markdown("### 📋 Liste de courses par plat (à cocher en magasin)")
        if not repas_planifies:
            st.info("Aucun repas planifié pour l'instant.")
        else:
            for repas, ing_list in dict_ingredients.items():
                st.markdown(f"**🍲 {repas}**")
                for ing in ing_list:
                    st.checkbox(ing, key=f"mag_{repas}_{ing}")
                st.write("")

    # -----------------------------------------------------
    # SUB-TAB 2: PROMPT IA CARREFOUR / HOPLA
    # -----------------------------------------------------
    with sub_tab2:
        st.markdown("### 🤖 Prompt prêt à copier pour Hopla (Carrefour Drive)")
        st.write("Copie ce texte structuré directement dans le chatbot Hopla de Carrefour pour remplir ton panier automatiquement :")
        
        # Génération du texte enrichi d'ingrédients
        prompt_hopla = "Bonjour Hopla ! Peux-tu ajouter à mon panier Carrefour tous les ingrédients suivants pour mes recettes de la semaine :\n\n"
        
        if not repas_planifies:
            prompt_hopla += "(Aucun repas planifié pour le moment)"
        else:
            all_ing_flat = []
            for repas, ing_list in dict_ingredients.items():
                prompt_hopla += f"📌 Pour {repas} :\n"
                for ing in ing_list:
                    prompt_hopla += f"  - {ing}\n"
                    all_ing_flat.append(ing)
                prompt_hopla += "\n"
            
            prompt_hopla += "Merci de me proposer les produits correspondants dans mon magasin !"

        st.text_area("Prompt à copier-coller :", value=prompt_hopla, height=350)
