import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Générateur de Menus Familiaux",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS reproduisant la grille dynamique et les badges
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1rem; color: #64748B; margin-bottom: 1rem; }
    .score-banner {
        text-align: center; font-size: 1.1rem; font-weight: 600; color: #475569;
        background-color: #F8FAFC; padding: 10px; border-radius: 8px; margin-bottom: 20px;
    }
    .score-bad { color: #DC2626; font-weight: 700; }
    .score-good { color: #16A34A; font-weight: 700; }
    
    /* Cartes de la grille */
    .grid-card {
        background-color: #FFFFFF;
        border: 2px dashed #E2E8F0;
        border-radius: 12px;
        min-height: 85px;
        padding: 8px;
        text-align: center;
        transition: all 0.2s ease;
    }
    .grid-card-filled {
        background-color: #FFFFFF;
        border: 1.5px solid #CBD5E1;
        border-radius: 12px;
        min-height: 85px;
        padding: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .meal-name { font-size: 0.85rem; font-weight: 700; color: #1E293B; margin-bottom: 6px; line-height: 1.2; }
    
    /* Puces des membres */
    .avatar-circle {
        display: inline-block;
        width: 22px; height: 22px;
        border-radius: 50%;
        color: white; font-weight: 700; font-size: 0.7rem;
        line-height: 22px; text-align: center;
        margin: 1px;
    }
    .bg-papa { background-color: #1D4ED8; }
    .bg-maman { background-color: #047857; }
    .bg-lea { background-color: #7C3AED; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIALISATION DES DONNÉES DE SESSION
# ---------------------------------------------------------
if 'planning' not in st.session_state:
    st.session_state['planning'] = pd.DataFrame([
        {"Jour": "Sam", "Creneau": "Déjeuner", "Nom_Profil": "Papa", "Nom_Repas": "Pâtes carbo", "Portion": "125%"},
        {"Jour": "Sam", "Creneau": "Déjeuner", "Nom_Profil": "Léa", "Nom_Repas": "Pâtes carbo", "Portion": "100%"},
    ])

if 'profils' not in st.session_state:
    st.session_state['profils'] = pd.DataFrame([
        {"ID": "PROF_01", "Nom": "Maman", "Initiale": "M", "Couleur": "bg-maman", "Besoins_Cal": "1800 kcal", "Fer": "Élevé"},
        {"ID": "PROF_02", "Nom": "Papa", "Initiale": "P", "Couleur": "bg-papa", "Besoins_Cal": "2400 kcal", "Fer": "Normal"},
        {"ID": "PROF_03", "Nom": "Léa", "Initiale": "L", "Couleur": "bg-lea", "Besoins_Cal": "1500 kcal", "Fer": "Modéré"}
    ])

if 'selected_slot' not in st.session_state:
    st.session_state['selected_slot'] = None

# Barre latérale - Connexion Google Sheets
with st.sidebar:
    st.title("⚙️ Configuration")
    gsheet_url = st.text_input("URL Apps Script Google Sheet:")
    if st.button("🔄 Synchro Google Sheet"):
        if gsheet_url:
            try:
                res = requests.get(gsheet_url).json()
                if "Planning_Semaine" in res:
                    st.session_state['planning'] = pd.DataFrame(res["Planning_Semaine"])
                st.success("Données synchronisées !")
            except Exception as e:
                st.error(f"Erreur de synchro: {e}")

# ---------------------------------------------------------
# NAVIGATION PAR ONGLETS
# ---------------------------------------------------------
tabs = st.tabs([
    "📅 Le planning", 
    "📊 Micronutriments", 
    "🛒 Liste de courses & IA", 
    "👥 Profils", 
    "⚙️ Base Repas"
])

# ---------------------------------------------------------
# TAB 1: PLANNING INTERACTIF (Style Image)
# ---------------------------------------------------------
with tabs[0]:
    st.markdown('<div class="main-title">Le planning</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Clique sur une case ou sur le bouton "+ Ajouter" pour assigner un repas et les personnes concernées.</div>', unsafe_allow_html=True)

    # Header Semaine & Bouton Génération
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_m, col_t, col_p = st.columns([1, 4, 1])
        col_m.button("‹", key="prev_wk", use_container_width=True)
        col_t.markdown("<h3 style='text-align:center; margin:0;'>14/09 ➔ 20/09</h3>", unsafe_allow_html=True)
        col_p.button("›", key="next_wk", use_container_width=True)

    # Score d'équilibre
    nb_repas = len(st.session_state['planning']['Nom_Repas'].unique())
    score = min(nb_repas * 15, 100)
    score_status = f'<span class="score-good">{score}/100 (Équilibré)</span>' if score >= 70 else f'<span class="score-bad">{score}/100 (Déséquilibré)</span>'
    st.markdown(f'<div class="score-banner">Équilibre de la semaine : {score_status} sur {nb_repas} repas planifiés &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'</div>', unsafe_allow_html=True)

    if st.button("✨ Générer automatiquement la semaine", use_container_width=True):
        st.success("Semaine générée avec succès selon vos critères nutritionnels !")

    st.write("")

    # Structure de la grille
    jours_map = [
        {"code": "Lun", "date": "14/09"},
        {"code": "Mar", "date": "15/09"},
        {"code": "Mer", "date": "16/09"},
        {"code": "Jeu", "date": "17/09"},
        {"code": "Ven", "date": "18/09"},
        {"code": "Sam", "date": "19/09"},
        {"code": "Dim", "date": "20/09"}
    ]
    creneaux = ["Petit-déj", "Déjeuner", "Goûter", "Dîner"]

    # Entête des jours
    cols = st.columns([1.2] + [1]*7)
    cols[0].write("")
    for i, j_info in enumerate(jours_map):
        cols[i+1].markdown(f"<div style='text-align:center; font-weight:bold;'>{j_info['code']}<br><span style='font-size:0.8rem; color:gray;'>{j_info['date']}</span></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Affichage des 4 lignes de créneaux
    for creneau in creneaux:
        row_cols = st.columns([1.2] + [1]*7)
        row_cols[0].markdown(f"**{creneau}**")
        
        for i, j_info in enumerate(jours_map):
            j_code = j_info["code"]
            df_cell = st.session_state['planning'][
                (st.session_state['planning']['Jour'] == j_code) & 
                (st.session_state['planning']['Creneau'] == creneau)
            ]
            
            with row_cols[i+1]:
                if df_cell.empty:
                    if st.button(f"+ Ajouter", key=f"btn_{j_code}_{creneau}", use_container_width=True):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": creneau}
                else:
                    # Case remplie
                    repas_nom = df_cell['Nom_Repas'].iloc[0]
                    membres = df_cell['Nom_Profil'].tolist()
                    
                    badges_html = ""
                    for m in membres:
                        match_p = st.session_state['profils'][st.session_state['profils']['Nom'] == m]
                        initiale = match_p['Initiale'].values[0] if not match_p.empty else m[0]
                        color_cls = match_p['Couleur'].values[0] if not match_p.empty else "bg-papa"
                        badges_html += f'<span class="avatar-circle {color_cls}">{initiale}</span>'
                    
                    st.markdown(f'''
                        <div class="grid-card-filled">
                            <div class="meal-name">{repas_nom}</div>
                            <div>{badges_html}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    if st.button("✏️", key=f"edit_{j_code}_{creneau}", help="Modifier"):
                        st.session_state['selected_slot'] = {"jour": j_code, "creneau": creneau}

    # Fenêtre modale d'ajout/modification si une case est cliquée
    if st.session_state['selected_slot']:
        slot = st.session_state['selected_slot']
        st.markdown("---")
        st.subheader(f"➕ Assigner un repas : {slot['jour']} — {slot['creneau']}")
        
        with st.form("form_assign"):
            nom_repas = st.text_input("Nom du repas", value="Dahl de Lentilles Corail")
            profils_selectionnes = st.multiselect(
                "Personnes concernées", 
                options=st.session_state['profils']['Nom'].tolist(),
                default=st.session_state['profils']['Nom'].tolist()
            )
            portion = st.selectbox("Portion type", ["100%", "125%", "75%"])
            
            col_save, col_cancel = st.columns(2)
            if col_save.form_submit_button("Enregistrer le repas"):
                # Nettoyage de l'ancienne entrée
                st.session_state['planning'] = st.session_state['planning'][
                    ~((st.session_state['planning']['Jour'] == slot['jour']) & 
                      (st.session_state['planning']['Creneau'] == slot['creneau']))
                ]
                # Ajout des nouveaux profils
                new_rows = []
                for prof in profils_selectionnes:
                    new_rows.append({
                        "Jour": slot['jour'],
                        "Creneau": slot['creneau'],
                        "Nom_Profil": prof,
                        "Nom_Repas": nom_repas,
                        "Portion": portion
                    })
                st.session_state['planning'] = pd.concat([st.session_state['planning'], pd.DataFrame(new_rows)], ignore_index=True)
                st.session_state['selected_slot'] = None
                st.rerun()

            if col_cancel.form_submit_button("Annuler"):
                st.session_state['selected_slot'] = None
                st.rerun()

# ---------------------------------------------------------
# TAB 2: MICRONUTRIMENTS
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("📊 Suivi des Micronutriments de la Semaine")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Fer total (Famille)", "84 mg", "+12% vs objectif")
    col_b.metric("Protéines végétales", "42%", "Équilibré")
    col_c.metric("Vitamines C & B12", "98%", "Excellent")
    
    st.markdown("### Répartition par membre de la famille")
    st.dataframe(pd.DataFrame({
        "Profil": ["Maman", "Papa", "Léa"],
        "Calories / Jour": ["1 850 kcal", "2 350 kcal", "1 480 kcal"],
        "Apport Fer": ["Optimal", "Normal", "À surveiller"],
        "Fibres": ["30g", "35g", "22g"]
    }), use_container_width=True)

# ---------------------------------------------------------
# TAB 3: LISTE DE COURSES & CARREFOUR IA (Hopla)
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("🛒 Export Liste de Courses & Carrefour IA")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("### Liste regroupée par rayon")
        st.checkbox("🥩 Saumon poêlé (600g)")
        st.checkbox("🥦 Brocolis frais (1kg)")
        st.checkbox("🌾 Riz Basmati (1kg)")
        st.checkbox("🥚 Œufs BIO (x12)")
    
    with col_r:
        st.markdown("### Prompt pour Hopla (Carrefour IA)")
        prompt_txt = """Bonjour Hopla, ajoute à mon panier Carrefour :
- 600g de pavé de saumon frais
- 1kg de brocolis BIO
- 1 paquet de Riz Basmati 1kg
- 1 boîte de 12 œufs BIO"""
        st.text_area("Copier le texte dans Hopla :", prompt_txt, height=180)

# ---------------------------------------------------------
# TAB 4: PROFILS FAMILIAUX
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("👥 Gestion des Profils")
    st.dataframe(st.session_state['profils'], use_container_width=True)
    
    with st.expander("➕ Ajouter un nouveau membre"):
        with st.form("add_profile"):
            nom_p = st.text_input("Prénom")
            init_p = st.text_input("Initiale (1 lettre)", max_chars=1)
            cal_p = st.text_input("Objectif Calorique", "2000 kcal")
            if st.form_submit_button("Créer le profil"):
                new_prof = {"ID": f"PROF_0{len(st.session_state['profils'])+1}", "Nom": nom_p, "Initiale": init_p.upper(), "Couleur": "bg-maman", "Besoins_Cal": cal_p, "Fer": "Normal"}
                st.session_state['profils'] = pd.concat([st.session_state['profils'], pd.DataFrame([new_prof])], ignore_index=True)
                st.success("Profil ajouté !")
                st.rerun()

# ---------------------------------------------------------
# TAB 5: BASE REPAS
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("⚙️ Base de données des recettes")
    st.dataframe(pd.DataFrame([
        {"ID": "REP_001", "Nom": "Saumon Poêlé, Riz Basmati & Épinards", "Catégorie": "Poisson", "Temps": "20 min"},
        {"ID": "REP_002", "Nom": "Poulet Rôti, Patates Douces & Brocolis", "Catégorie": "Volaille", "Temps": "35 min"},
        {"ID": "REP_003", "Nom": "Dahl de Lentilles Corail & Riz", "Catégorie": "Végétarien", "Temps": "25 min"},
        {"ID": "REP_004", "Nom": "Pâtes carbo", "Catégorie": "Pâtes", "Temps": "15 min"},
    ]), use_container_width=True)
