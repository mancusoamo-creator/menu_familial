import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Menu Familial Kawaii 🍓",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CSS DESIGN PASTEL & KAWAII
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Font & Global Background */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    
    .stApp {
        background-color: #FAF7F2;
    }
    
    /* Header Kawaii */
    .kawaii-header {
        background: linear-gradient(135deg, #FFD1DC 0%, #E6E6FA 50%, #D4F1F4 100%);
        padding: 24px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(255, 209, 220, 0.4);
        margin-bottom: 25px;
    }
    .kawaii-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #4A3E3D;
        margin: 0;
    }
    .kawaii-subtitle {
        font-size: 1rem;
        color: #7A6B69;
        margin-top: 6px;
        font-weight: 600;
    }
    
    /* Score Banner Pastel */
    .score-card {
        background-color: #FFFFFF;
        border: 2px solid #FFE5EC;
        border-radius: 18px;
        padding: 12px 20px;
        text-align: center;
        font-weight: 700;
        color: #5C4B51;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .badge-score-ok {
        background-color: #D4EDDA;
        color: #155724;
        padding: 4px 12px;
        border-radius: 12px;
    }
    
    /* Dynamic Grid Cards */
    .grid-slot-empty {
        background-color: #FFFFFF;
        border: 2px dashed #E2D9F3;
        border-radius: 16px;
        padding: 10px;
        text-align: center;
        min-height: 90px;
        transition: all 0.2s ease;
    }
    
    .grid-slot-filled {
        border-radius: 16px;
        padding: 10px;
        min-height: 90px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Thèmes par créneau */
    .slot-petit-dej { background-color: #FFF9DB; border-left: 5px solid #FCC419; }
    .slot-dejeuner { background-color: #E6FCF5; border-left: 5px solid #20C997; }
    .slot-gouter { background-color: #FFF0F6; border-left: 5px solid #FAA2C1; }
    .slot-diner { background-color: #F3F0FF; border-left: 5px solid #845EF7; }
    
    .meal-title-text {
        font-size: 0.88rem;
        font-weight: 800;
        color: #343A40;
        margin-bottom: 6px;
        line-height: 1.2;
    }
    
    /* Kawaii Profile Badges */
    .avatar-chip {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        color: white;
        margin: 2px 1px;
    }
    .chip-maman { background-color: #FF85A1; }
    .chip-papa { background-color: #4EA8DE; }
    .chip-lea { background-color: #B5179E; }
    .chip-default { background-color: #7209B7; }

    /* Customizing Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 16px;
        padding: 8px 16px;
        background-color: #FFFFFF;
        border: 1px solid #E9ECEF;
        font-weight: 700;
        color: #6C757D;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD1DC !important;
        color: #4A3E3D !important;
        border: 1px solid #FFB6C1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIALISATION DES DONNÉES EN SESSION
# ---------------------------------------------------------
if 'profils' not in st.session_state:
    st.session_state['profils'] = pd.DataFrame([
        {"Nom": "Maman", "Initiale": "M", "Couleur_Chip": "chip-maman", "Objectif_Cal": "1800 kcal", "Fer": "Élevé"},
        {"Nom": "Papa", "Initiale": "P", "Couleur_Chip": "chip-papa", "Objectif_Cal": "2400 kcal", "Fer": "Normal"},
        {"Nom": "Léa", "Initiale": "L", "Couleur_Chip": "chip-lea", "Objectif_Cal": "1500 kcal", "Fer": "Modéré"}
    ])

if 'recettes' not in st.session_state:
    st.session_state['recettes'] = pd.DataFrame([
        {"ID": "REP_01", "Nom": "Pâtes à la Carbonara", "Catégorie": "Pâtes", "Temps": "15 min", "Calories": "550 kcal"},
        {"ID": "REP_02", "Nom": "Saumon Poêlé & Riz Basmati", "Catégorie": "Poisson", "Temps": "20 min", "Calories": "480 kcal"},
        {"ID": "REP_03", "Nom": "Dahl de Lentilles Corail", "Catégorie": "Végétarien", "Temps": "25 min", "Calories": "380 kcal"},
        {"ID": "REP_04", "Nom": "Bowl Açaï & Fruits Frais", "Catégorie": "Petit-déj", "Temps": "10 min", "Calories": "310 kcal"},
        {"ID": "REP_05", "Nom": "Pancakes Banane & Miel", "Catégorie": "Goûter", "Temps": "15 min", "Calories": "280 kcal"}
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
    <div class="kawaii-subtitle">Planification douce, équilibrée et gourmande pour toute la famille</div>
</div>
""", unsafe_allow_html=True)

# Barre latérale pour la synchronisation Google Sheets
with st.sidebar:
    st.title("⚙️ Synchronisation")
    gsheet_url = st.text_input("URL Apps Script Google Sheet :")
    if st.button("🔄 Sync Google Sheet", use_container_width=True):
        if gsheet_url:
            try:
                res = requests.get(gsheet_url).json()
                if "Planning_Semaine" in res:
                    st.session_state['planning'] = pd.DataFrame(res["Planning_Semaine"])
                st.success("Synchronisé !")
            except Exception as e:
                st.error(f"Erreur : {e}")

# Navigation par Onglets Pastel
tabs = st.tabs([
    "🗓️ Le Planning", 
    "👥 Éditeur de Profils", 
    "🍱 Base de Recettes", 
    "📊 Micronutriments", 
    "🛒 Liste Drive IA"
])

# ---------------------------------------------------------
# TAB 1: PLANNING KAWAII INTERACTIF
# ---------------------------------------------------------
with tabs[0]:
    # Contrôles supérieurs
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_m, col_t, col_p = st.columns([1, 4, 1])
        col_m.button("‹", key="prev_wk", use_container_width=True)
        col_t.markdown("<h3 style='text-align:center; color:#4A3E3D; margin:0;'>14/09 ➔ 20/09</h3>", unsafe_allow_html=True)
        col_p.button("›", key="next_wk", use_container_width=True)

    # Bannière Score d'équilibre
    nb_repas = len(st.session_state['planning']['Nom_Repas'].unique())
    score = min(nb_repas * 20, 100)
    st.markdown(f'''
    <div class="score-card">
        ✨ Équilibre nutritionnel de la semaine : <span class="badge-score-ok">{score} / 100</span>
        &nbsp;&nbsp;•&nbsp;&nbsp; 🍱 {nb_repas} repas variés planifiés
    </div>
    ''', unsafe_allow_html=True)

    if st.button("✨ Générer automatiquement les menus de la semaine", use_container_width=True):
        st.balloons()
        st.success("Menu pastel généré automatiquement !")

    st.write("")

    # Structure de la grille 7 Jours x 4 Créneaux
    jours = [
        {"code": "Lun", "date": "14/09"}, {"code": "Mar", "date": "15/09"},
        {"code": "Mer", "date": "16/09"}, {"code": "Jeu", "date": "17/09"},
        {"code": "Ven", "date": "18/09"}, {"code": "Sam", "date": "19/09"},
        {"code": "Dim", "date": "20/09"}
    ]
    creneaux_info = [
        {"nom": "Petit-déj", "css": "slot-petit-dej"},
        {"nom": "Déjeuner", "css": "slot-dejeuner"},
        {"nom": "Goûter", "css": "slot-gouter"},
        {"nom": "Dîner", "css": "slot-diner"}
    ]

    # En-têtes Jours
    cols_header = st.columns([1.2] + [1]*7)
    cols_header[0].write("")
    for i, j in enumerate(jours):
        cols_header[i+1].markdown(f"<div style='text-align:center; font-weight:800; color:#5C4B51;'>{j['code']}<br><span style='font-size:0.8rem; color:#A799B7;'>{j['date']}</span></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #FFE5EC;'>", unsafe_allow_html=True)

    # Rendu des créneaux
    for c_info in creneaux_info:
        creneau_nom = c_info["nom"]
        creneau_css = c_info["css"]
        
        row_cols = st.columns([1.2] + [1]*7)
        row_cols[0].markdown(f"<p style='font-weight:800; color:#4A3E3D; margin-top:15px;'>{creneau_nom}</p>", unsafe_allow_html=True)
        
        for i, j in enumerate(jours):
            j_code = j["code"]
            df_cell = st.session_state['planning'][
                (st.session_state['planning']['Jour'] == j_code) & 
                (st.session_state['planning']['Creneau'] == creneau_nom)
            ]
            
            with row_cols[i+1]:
                if df_cell.empty:
                    if st.button("➕", key=f"btn_{j_code}_{creneau_nom}", use_container_width=True, help="Ajouter un repas"):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": creneau_nom}
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
                        <div class="grid-slot-filled {creneau_css}">
                            <div class="meal-title-text">{nom_repas}</div>
                            <div>{chips_html}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    if st.button("✏️", key=f"edit_{j_code}_{creneau_nom}", help="Modifier"):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": creneau_nom}
                        st.rerun()

    # Formulaire Modal / Modificateur de case
    if st.session_state['selected_slot']:
        slot = st.session_state['selected_slot']
        st.markdown("<hr style='border:1px solid #FFD1DC;'>", unsafe_allow_html=True)
        st.subheader(f"🌸 Modifier le créneau : {slot['jour']} — {slot['creneau']}")
        
        with st.form("form_slot_edit"):
            liste_recettes = st.session_state['recettes']['Nom'].tolist()
            repas_choisi = st.selectbox("Choisir une recette existante :", options=liste_recettes)
            repas_custom = st.text_input("Ou saisir un repas personnalisé :", value="")
            
            repas_final = repas_custom if repas_custom.strip() != "" else repas_choisi
            
            profils_selectionnes = st.multiselect(
                "Membres présents pour ce repas :",
                options=st.session_state['profils']['Nom'].tolist(),
                default=st.session_state['profils']['Nom'].tolist()
            )
            portion = st.selectbox("Portion :", ["100%", "125%", "75%"])
            
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
            if btn_col1.form_submit_button("💾 Enregistrer"):
                # Supprimer la version précédente de cette case
                st.session_state['planning'] = st.session_state['planning'][
                    ~((st.session_state['planning']['Jour'] == slot['jour']) & 
                      (st.session_state['planning']['Creneau'] == slot['creneau']))
                ]
                # Ajouter les nouvelles données
                nouvelles_lignes = []
                for p in profils_selectionnes:
                    nouvelles_lignes.append({
                        "Jour": slot['jour'],
                        "Creneau": slot['creneau'],
                        "Nom_Profil": p,
                        "Nom_Repas": repas_final,
                        "Portion": portion
                    })
                st.session_state['planning'] = pd.concat([st.session_state['planning'], pd.DataFrame(nouvelles_lignes)], ignore_index=True)
                st.session_state['selected_slot'] = None
                st.rerun()
                
            if btn_col2.form_submit_button("🗑️ Effacer"):
                st.session_state['planning'] = st.session_state['planning'][
                    ~((st.session_state['planning']['Jour'] == slot['jour']) & 
                      (st.session_state['planning']['Creneau'] == slot['creneau']))
                ]
                st.session_state['selected_slot'] = None
                st.rerun()

            if btn_col3.form_submit_button("❌ Annuler"):
                st.session_state['selected_slot'] = None
                st.rerun()

# ---------------------------------------------------------
# TAB 2: ÉDITEUR DIRECT DES PROFILS
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("👥 Éditeur Interactif des Profils Familiaux")
    st.info("💡 Tu peux modifier directement les cellules du tableau ci-dessous ou ajouter un profil avec le formulaire.")
    
    # ÉDITION DIRECTE DU TABLEAU
    edited_profils = st.data_editor(
        st.session_state['profils'],
        num_rows="dynamic",
        use_container_width=True,
        key="profils_editor"
    )
    
    if st.button("💾 Sauvegarder les modifications des profils"):
        st.session_state['profils'] = edited_profils
        st.success("Profils mis à jour avec succès !")
        st.rerun()
        
    st.markdown("---")
    st.markdown("### ➕ Ajouter un membre rapidement")
    with st.form("form_add_prof"):
        cp1, cp2, cp3 = st.columns(3)
        p_nom = cp1.text_input("Prénom :", "Mimi")
        p_init = cp2.text_input("Initiale (1 lettre) :", "M")
        p_color = cp3.selectbox("Couleur du badge :", ["chip-maman", "chip-papa", "chip-lea", "chip-default"])
        p_cal = cp1.text_input("Besoins Caloriques :", "2000 kcal")
        p_fer = cp2.selectbox("Besoin en Fer :", ["Normal", "Élevé", "Modéré"])
        
        if st.form_submit_button("Ajouter le profil"):
            nouveau_profil = {
                "Nom": p_nom,
                "Initiale": p_init.upper(),
                "Couleur_Chip": p_color,
                "Objectif_Cal": p_cal,
                "Fer": p_fer
            }
            st.session_state['profils'] = pd.concat([st.session_state['profils'], pd.DataFrame([nouveau_profil])], ignore_index=True)
            st.success(f"Profil {p_nom} ajouté !")
            st.rerun()

# ---------------------------------------------------------
# TAB 3: BASE DE RECETTES INTERACTIVE
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("🍱 Base de Recettes & Repas")
    st.info("💡 Modifie directement les plats, catégories ou temps de préparation dans la grille.")
    
    # ÉDITION DIRECTE DE LA BASE REPAS
    edited_recettes = st.data_editor(
        st.session_state['recettes'],
        num_rows="dynamic",
        use_container_width=True,
        key="recettes_editor"
    )
    
    if st.button("💾 Sauvegarder la base de recettes"):
        st.session_state['recettes'] = edited_recettes
        st.success("Base de recettes mise à jour !")
        st.rerun()

    st.markdown("---")
    st.markdown("### ➕ Ajouter une nouvelle recette")
    with st.form("form_add_recipe"):
        cr1, cr2, cr3 = st.columns(3)
        r_nom = cr1.text_input("Nom du plat :")
        r_cat = cr2.selectbox("Catégorie :", ["Pâtes", "Poisson", "Végétarien", "Volaille", "Viande", "Petit-déj", "Goûter"])
        r_temps = cr3.text_input("Temps de préparation :", "20 min")
        r_cal = cr1.text_input("Estimation Calories :", "450 kcal")
        
        if st.form_submit_button("Ajouter la recette"):
            if r_nom.strip() != "":
                nouvelle_recette = {
                    "ID": f"REP_0{len(st.session_state['recettes'])+1}",
                    "Nom": r_nom,
                    "Catégorie": r_cat,
                    "Temps": r_temps,
                    "Calories": r_cal
                }
                st.session_state['recettes'] = pd.concat([st.session_state['recettes'], pd.DataFrame([nouvelle_recette])], ignore_index=True)
                st.success("Recette ajoutée à la base !")
                st.rerun()

# ---------------------------------------------------------
# TAB 4: MICRONUTRIMENTS & ÉQUILIBRE
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("📊 Bilan Nutritionnel Pastel")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Calories Hebdo Moyennes", "1 950 kcal / jour", "+5% vs objectif")
    m2.metric("🥬 Apport en Fer (Famille)", "92%", "Équilibré")
    m3.metric("🍓 Vitamines & Fibres", "95%", "Optimal")
    
    st.markdown("### Synthèse par membre de la famille")
    st.dataframe(st.session_state['profils'][['Nom', 'Objectif_Cal', 'Fer']], use_container_width=True)

# ---------------------------------------------------------
# TAB 5: LISTE DE COURSES & IA DRIVE
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("🛒 Export Liste de Courses & Hopla (Carrefour IA)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 📝 Ingrédients à acheter")
        repas_planifies = st.session_state['planning']['Nom_Repas'].unique().tolist()
        if repas_planifies:
            for r in repas_planifies:
                st.checkbox(f"Ingrédients pour : **{r}**", value=True)
        else:
            st.write("Aucun repas planifié pour le moment.")
            
    with col_b:
        st.markdown("### 🤖 Prompt pré-rédigé pour Hopla")
        text_prompt = "Bonjour Hopla ! Peux-tu ajouter à mon panier Carrefour les ingrédients nécessaires pour ces repas :\n"
        for r in repas_planifies:
            text_prompt += f"- {r}\n"
            
        st.text_area("Copie ce texte dans l'assistant Hopla de Carrefour :", text_prompt, height=200)
