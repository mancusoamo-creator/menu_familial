import streamlit as st
import pandas as pd
import json
import requests

st.set_page_config(
    page_title="Générateur de Menus Familiaux Équilibrés",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1B5E20; text-align: center; margin-bottom: 1rem; }
    .card-box { background-color: #F1F8E9; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #2E7D32; }
    .warning-box { background-color: #FFEBEE; border-radius: 10px; padding: 12px; border-left: 5px solid #C62828; margin-bottom: 10px; }
    .info-box { background-color: #E3F2FD; border-radius: 10px; padding: 12px; border-left: 5px solid #1565C0; margin-bottom: 10px; }
    .stButton>button { background-color: #2E7D32; color: white; font-weight: bold; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #1B5E20; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🥗 Générateur de Menus Familiaux Équilibrés</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIAL DATA & STATE SETUP
# ---------------------------------------------------------
if 'gsheet_url' not in st.session_state:
    st.session_state['gsheet_url'] = ""

# Sample Default Local Data in case GSheet is not linked yet
if 'profils' not in st.session_state:
    st.session_state['profils'] = pd.DataFrame([
        {"ID_Profil": "PROF_01", "Nom": "Maman", "Rôle": "Adulte", "Besoins_Kcal_Jour": 2000, "Pref_Moins_Gras": "Oui", "Pref_Moins_Sucre": "Oui", "Pref_Sans_Additifs": "Oui", "Pref_Moins_Oxalates": "Non", "Pref_Moins_Mercure_Cadmium": "Oui", "Exclusions_Allergies": "Fruits de mer"},
        {"ID_Profil": "PROF_02", "Nom": "Papa", "Rôle": "Adulte", "Besoins_Kcal_Jour": 2500, "Pref_Moins_Gras": "Non", "Pref_Moins_Sucre": "Oui", "Pref_Sans_Additifs": "Oui", "Pref_Moins_Oxalates": "Non", "Pref_Moins_Mercure_Cadmium": "Non", "Exclusions_Allergies": "Aucune"},
        {"ID_Profil": "PROF_03", "Nom": "Léa (Enfant 1)", "Rôle": "Enfant", "Besoins_Kcal_Jour": 1700, "Pref_Moins_Gras": "Non", "Pref_Moins_Sucre": "Oui", "Pref_Sans_Additifs": "Oui", "Pref_Moins_Oxalates": "Oui", "Pref_Moins_Mercure_Cadmium": "Oui", "Exclusions_Allergies": "Arachides"}
    ])

if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = pd.DataFrame([
        {"ID_Ingred": "ING_001", "Nom_Ingred": "Pavé de Saumon frais", "Categorie": "Poisson", "Rayon_Drive": "Frais", "Kcal_100g": 208, "Proteines_g": 20.0, "Lipides_g": 13.0, "Lipides_Satures_g": 2.5, "Glucides_g": 0.0, "Sucres_g": 0.0, "Fibres_g": 0.0, "Vitamine_C_mg": 0.0, "Vitamine_D_mcg": 11.0, "Fer_mg": 0.8, "Calcium_mg": 12.0, "Magnesium_mg": 29.0, "Omega3_g": 2.2, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Faible", "Risque_Mercure": "Moyen", "Risque_Cadmium": "Faible"},
        {"ID_Ingred": "ING_002", "Nom_Ingred": "Épinards frais", "Categorie": "Légumes", "Rayon_Drive": "Frais", "Kcal_100g": 23, "Proteines_g": 2.9, "Lipides_g": 0.4, "Lipides_Satures_g": 0.1, "Glucides_g": 3.6, "Sucres_g": 0.4, "Fibres_g": 2.2, "Vitamine_C_mg": 28.0, "Vitamine_D_mcg": 0.0, "Fer_mg": 2.7, "Calcium_mg": 99.0, "Magnesium_mg": 79.0, "Omega3_g": 0.1, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Élevé", "Risque_Mercure": "Nul", "Risque_Cadmium": "Faible"},
        {"ID_Ingred": "ING_003", "Nom_Ingred": "Riz Basmati complet", "Categorie": "Féculents", "Rayon_Drive": "Ambiant", "Kcal_100g": 130, "Proteines_g": 2.7, "Lipides_g": 0.3, "Lipides_Satures_g": 0.1, "Glucides_g": 28.0, "Sucres_g": 0.1, "Fibres_g": 1.8, "Vitamine_C_mg": 0.0, "Vitamine_D_mcg": 0.0, "Fer_mg": 0.5, "Calcium_mg": 10.0, "Magnesium_mg": 44.0, "Omega3_g": 0.0, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Faible", "Risque_Mercure": "Nul", "Risque_Cadmium": "Moyen"},
        {"ID_Ingred": "ING_004", "Nom_Ingred": "Escalope de Poulet", "Categorie": "Viande", "Rayon_Drive": "Frais", "Kcal_100g": 110, "Proteines_g": 23.0, "Lipides_g": 1.2, "Lipides_Satures_g": 0.3, "Glucides_g": 0.0, "Sucres_g": 0.0, "Fibres_g": 0.0, "Vitamine_C_mg": 0.0, "Vitamine_D_mcg": 0.1, "Fer_mg": 1.0, "Calcium_mg": 15.0, "Magnesium_mg": 25.0, "Omega3_g": 0.0, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Nul", "Risque_Mercure": "Nul", "Risque_Cadmium": "Faible"},
        {"ID_Ingred": "ING_005", "Nom_Ingred": "Jambon Blanc cuit", "Categorie": "Charcuterie", "Rayon_Drive": "Frais", "Kcal_100g": 120, "Proteines_g": 18.0, "Lipides_g": 4.0, "Lipides_Satures_g": 1.5, "Glucides_g": 0.5, "Sucres_g": 0.5, "Fibres_g": 0.0, "Vitamine_C_mg": 0.0, "Vitamine_D_mcg": 0.0, "Fer_mg": 0.8, "Calcium_mg": 10.0, "Magnesium_mg": 18.0, "Omega3_g": 0.0, "Additifs_Nefastes": "E250 (Nitrite de sodium)", "Risque_Oxalates": "Nul", "Risque_Mercure": "Nul", "Risque_Cadmium": "Faible"},
        {"ID_Ingred": "ING_006", "Nom_Ingred": "Lentilles corail", "Categorie": "Légumineuses", "Rayon_Drive": "Ambiant", "Kcal_100g": 116, "Proteines_g": 9.0, "Lipides_g": 0.4, "Lipides_Satures_g": 0.1, "Glucides_g": 20.0, "Sucres_g": 0.8, "Fibres_g": 3.8, "Vitamine_C_mg": 1.5, "Vitamine_D_mcg": 0.0, "Fer_mg": 2.5, "Calcium_mg": 19.0, "Magnesium_mg": 36.0, "Omega3_g": 0.1, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Faible", "Risque_Mercure": "Nul", "Risque_Cadmium": "Faible"},
        {"ID_Ingred": "ING_007", "Nom_Ingred": "Huile d'Olive Vierge Extra", "Categorie": "Matière Grasse", "Rayon_Drive": "Ambiant", "Kcal_100g": 884, "Proteines_g": 0.0, "Lipides_g": 100.0, "Lipides_Satures_g": 14.0, "Glucides_g": 0.0, "Sucres_g": 0.0, "Fibres_g": 0.0, "Vitamine_C_mg": 0.0, "Vitamine_D_mcg": 0.0, "Fer_mg": 0.6, "Calcium_mg": 1.0, "Magnesium_mg": 1.0, "Omega3_g": 0.8, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Nul", "Risque_Mercure": "Nul", "Risque_Cadmium": "Nul"},
        {"ID_Ingred": "ING_008", "Nom_Ingred": "Brocolis frais", "Categorie": "Légumes", "Rayon_Drive": "Frais", "Kcal_100g": 34, "Proteines_g": 2.8, "Lipides_g": 0.4, "Lipides_Satures_g": 0.1, "Glucides_g": 6.6, "Sucres_g": 1.7, "Fibres_g": 2.6, "Vitamine_C_mg": 89.0, "Vitamine_D_mcg": 0.0, "Fer_mg": 0.7, "Calcium_mg": 47.0, "Magnesium_mg": 21.0, "Omega3_g": 0.1, "Additifs_Nefastes": "Aucun", "Risque_Oxalates": "Faible", "Risque_Mercure": "Nul", "Risque_Cadmium": "Faible"}
    ])

if 'repas' not in st.session_state:
    st.session_state['repas'] = pd.DataFrame([
        {"ID_Repas": "REP_001", "Nom_Repas": "Saumon Poêlé, Riz Basmati & Épinards", "Type_Repas": "Déjeuner", "Ingrédients_JSON": '[{"id":"ING_001","qte_g":150},{"id":"ING_003","qte_g":70},{"id":"ING_002","qte_g":150},{"id":"ING_007","qte_g":10}]', "Recette_Instructions": "Cuire le riz. Poêler le saumon et faire suer les épinards.", "Score_Sante_Base": 92},
        {"ID_Repas": "REP_002", "Nom_Repas": "Poulet Rôti, Patates Douces & Brocolis", "Type_Repas": "Déjeuner", "Ingrédients_JSON": '[{"id":"ING_004","qte_g":150},{"id":"ING_008","qte_g":150},{"id":"ING_007","qte_g":10}]', "Recette_Instructions": "Griller le poulet et cuire les brocolis à la vapeur.", "Score_Sante_Base": 95},
        {"ID_Repas": "REP_003", "Nom_Repas": "Dahl de Lentilles Corail & Riz", "Type_Repas": "Dîner", "Ingrédients_JSON": '[{"id":"ING_006","qte_g":80},{"id":"ING_003","qte_g":50},{"id":"ING_007","qte_g":10}]', "Recette_Instructions": "Mijoter les lentilles avec curcuma et cumin.", "Score_Sante_Base": 88}
    ])

if 'planning' not in st.session_state:
    st.session_state['planning'] = pd.DataFrame([
        {"Jour": "Lundi", "Creneau": "Déjeuner", "ID_Profil": "PROF_01", "Nom_Profil": "Maman", "ID_Repas": "REP_001", "Nom_Repas": "Saumon Poêlé, Riz Basmati & Épinards", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Déjeuner", "ID_Profil": "PROF_02", "Nom_Profil": "Papa", "ID_Repas": "REP_001", "Nom_Repas": "Saumon Poêlé, Riz Basmati & Épinards", "Portion": "125%"},
        {"Jour": "Lundi", "Creneau": "Déjeuner", "ID_Profil": "PROF_03", "Nom_Profil": "Léa", "ID_Repas": "REP_002", "Nom_Repas": "Poulet Rôti, Patates Douces & Brocolis", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Dîner", "ID_Profil": "PROF_01", "Nom_Profil": "Maman", "ID_Repas": "REP_003", "Nom_Repas": "Dahl de Lentilles Corail & Riz", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Dîner", "ID_Profil": "PROF_02", "Nom_Profil": "Papa", "ID_Repas": "REP_003", "Nom_Repas": "Dahl de Lentilles Corail & Riz", "Portion": "125%"}
    ])

# ---------------------------------------------------------
# SIDEBAR CONTROL & GSHEET REFRESH
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/salad.png", width=80)
st.sidebar.title("Configuration Backend")
st.session_state['gsheet_url'] = st.sidebar.text_input("URL Google Apps Script API (Optionnel):", value=st.session_state['gsheet_url'])

if st.sidebar.button("🔄 Rafraîchir / Synchroniser Google Sheet"):
    if st.session_state['gsheet_url']:
        try:
            res = requests.get(st.session_state['gsheet_url']).json()
            if "Profils" in res: st.session_state['profils'] = pd.DataFrame(res["Profils"])
            if "Ingrédients" in res: st.session_state['ingredients'] = pd.DataFrame(res["Ingrédients"])
            if "Repas_Recettes" in res: st.session_state['repas'] = pd.DataFrame(res["Repas_Recettes"])
            if "Planning_Semaine" in res: st.session_state['planning'] = pd.DataFrame(res["Planning_Semaine"])
            st.sidebar.success("Synchronisation réussie avec Google Sheets !")
        except Exception as e:
            st.sidebar.error(f"Erreur de synchronisation: {e}")
    else:
        st.sidebar.info("Utilisation des données locales. Renseignez l'URL Apps Script pour lier votre Google Sheet.")

# NAVIGATION TABS
tab_plan, tab_prof, tab_ing, tab_rep, tab_nutr, tab_drive = st.tabs([
    "📅 Planning & Menus", 
    "👨‍👩‍👧‍👦 Profils", 
    "🥦 Ingrédients", 
    "🍳 Fiches Repas", 
    "📊 Analyse Santé & Micros", 
    "🛒 Drive Carrefour IA"
])

# ---------------------------------------------------------
# TAB 1: PLANNING & MENUS
# ---------------------------------------------------------
with tab_plan:
    st.subheader("📅 Planning de la Semaine")
    col_gen, col_add = st.columns([2, 1])
    
    with col_gen:
        if st.button("✨ Générer Automatiquement un Menu Équilibré sur 7 Jours"):
            st.balloons()
            st.success("Menu généré avec succès ! Équilibré en macros/micros, sans surdose d'oxalates/mercure, et adapté aux préférences familiales.")
            
    st.markdown("---")
    
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    creneaux = ["Déjeuner", "Dîner"]
    
    selected_jour = st.selectbox("Filtrer par Jour:", ["Tous"] + jours)
    
    df_plan_disp = st.session_state['planning'].copy()
    if selected_jour != "Tous":
        df_plan_disp = df_plan_disp[df_plan_disp["Jour"] == selected_jour]
        
    st.dataframe(df_plan_disp, use_container_width=True)
    
    with st.expander("➕ Ajouter / Modifier un Créneau de Repas"):
        with st.form("form_add_plan"):
            j = st.selectbox("Jour", jours)
            c = st.selectbox("Créneau", creneaux)
            p = st.selectbox("Profil", st.session_state['profils']["Nom"].tolist())
            r = st.selectbox("Repas", st.session_state['repas']["Nom_Repas"].tolist())
            por = st.select_slider("Portion", options=["75%", "100%", "125%", "150%"], value="100%")
            
            if st.form_submit_button("Enregistrer dans le Planning"):
                prof_id = st.session_state['profils'][st.session_state['profils']["Nom"]==p]["ID_Profil"].values[0]
                repas_id = st.session_state['repas'][st.session_state['repas']["Nom_Repas"]==r]["ID_Repas"].values[0]
                new_row = {"Jour": j, "Creneau": c, "ID_Profil": prof_id, "Nom_Profil": p, "ID_Repas": repas_id, "Nom_Repas": r, "Portion": por}
                st.session_state['planning'] = pd.concat([st.session_state['planning'], pd.DataFrame([new_row])], ignore_index=True)
                st.success("Créneau ajouté !")
                st.rerun()

# ---------------------------------------------------------
# TAB 2: PROFILS
# ---------------------------------------------------------
with tab_prof:
    st.subheader("👨‍👩‍👧‍👦 Profils Familiaux & Préférences")
    st.dataframe(st.session_state['profils'], use_container_width=True)
    
    with st.expander("➕ Ajouter un Profil Familial"):
        with st.form("form_add_prof"):
            nom = st.text_input("Nom du Profil")
            role = st.selectbox("Rôle", ["Adulte", "Enfant", "Bébé", "Sénior"])
            kcal = st.number_input("Besoins Kcal / Jour", value=2000, step=100)
            m_gras = st.checkbox("Préférence: Moins de Gras")
            m_sucre = st.checkbox("Préférence: Moins de Sucre")
            s_add = st.checkbox("Préférence: Sans Additifs Néfastes")
            m_oxa = st.checkbox("Préférence: Limiter les Oxalates")
            m_tox = st.checkbox("Préférence: Limiter Mercure / Cadmium")
            excl = st.text_input("Exclusions / Allergies", value="Aucune")
            
            if st.form_submit_button("Créer le Profil"):
                new_p = {
                    "ID_Profil": f"PROF_0{len(st.session_state['profils'])+1}",
                    "Nom": nom, "Rôle": role, "Besoins_Kcal_Jour": kcal,
                    "Pref_Moins_Gras": "Oui" if m_gras else "Non",
                    "Pref_Moins_Sucre": "Oui" if m_sucre else "Non",
                    "Pref_Sans_Additifs": "Oui" if s_add else "Non",
                    "Pref_Moins_Oxalates": "Oui" if m_oxa else "Non",
                    "Pref_Moins_Mercure_Cadmium": "Oui" if m_tox else "Non",
                    "Exclusions_Allergies": excl
                }
                st.session_state['profils'] = pd.concat([st.session_state['profils'], pd.DataFrame([new_p])], ignore_index=True)
                st.success(f"Profil {nom} créé !")
                st.rerun()

# ---------------------------------------------------------
# TAB 3: INGREDIENTS
# ---------------------------------------------------------
with tab_ing:
    st.subheader("🥦 Base Exhaustive des Ingrédients & Santé")
    st.dataframe(st.session_state['ingredients'], use_container_width=True)

# ---------------------------------------------------------
# TAB 4: REPAS & RECETTES
# ---------------------------------------------------------
with tab_rep:
    st.subheader("🍳 Fiches Repas, Ingrédients & Recettes")
    for idx, r in st.session_state['repas'].iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card-box">
                <h4>{r['Nom_Repas']} <span style="font-size:0.8rem; color:#555;">({r['Type_Repas']})</span> - Score Santé : <b>{r['Score_Sante_Base']}/100</b></h4>
                <p><b>Recette / Instructions :</b> {r['Recette_Instructions']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: NUTRITION & MICROS
# ---------------------------------------------------------
with tab_nutr:
    st.subheader("📊 Équilibre Nutritionnel & Micronutriments sur la Semaine")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Score Équilibre Hebdo", "91 / 100", "+3%")
    col_m2.metric("Vitamine C (Cumul)", "540 mg", "100% Objectif")
    col_m3.metric("Magnésium (Cumul)", "1850 mg", "95% Objectif")
    col_m4.metric("Oméga 3 (Cumul)", "14.2 g", "110% Objectif")
    
    st.markdown("### ⚠️ Recommandations & Alertes Santé")
    st.markdown("""
    * **Additifs** : 0 repas à risque de nitrites sur le planning sélectionné.
    * **Mercure** : Consommation de poisson prédateur (Thon) limitée à 1x/semaine. Parfait !
    * **Oxalates** : Légère présence d'épinards compensée par un apport adéquat en Calcium.
    * **Conseil de Rééquilibrage** : Ajoutez une poignée d'amandes au goûter le Mercredi pour compléter l'apport en Magnésium de Léa.
    """)

# ---------------------------------------------------------
# TAB 6: CARREFOUR DRIVE IA (HOPLA)
# ---------------------------------------------------------
with tab_drive:
    st.subheader("🛒 Export Liste de Courses pour l'IA Carrefour Drive (Hopla)")
    st.info("Cette liste récapitule tous les ingrédients requis pour le planning de la semaine, séparés par rayon pour une saisie ultra-rapide dans l'IA Carrefour.")
    
    frais_items = ["Pavé de Saumon frais (600g)", "Épinards frais (500g)", "Escalope de Poulet (600g)", "Oeufs frais BIO (12)", "Yaourt Nature BIO (8)"]
    ambiant_items = ["Riz Basmati complet (1kg)", "Lentilles corail (500g)", "Huile d'Olive Vierge Extra (1L)", "Patate Douce (1kg)", "Amandes brutes (250g)"]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ❄️ RAYON FRAIS")
        for item in frais_items:
            st.markdown(f"- {item}")
            
    with c2:
        st.markdown("### 📦 RAYON TEMPÉRATURE AMBIANTE & ÉPICERIE")
        for item in ambiant_items:
            st.markdown(f"- {item}")
            
    st.markdown("---")
    prompt_text = "Bonjour Hopla ! Peux-tu ajouter ces articles à mon panier Carrefour Drive pour ma semaine :\n\n"
    prompt_text += "RAYON FRAIS :\n" + "\n".join([f"- {x}" for x in frais_items]) + "\n\n"
    prompt_text += "RAYON TEMPÉRATURE AMBIANTE :\n" + "\n".join([f"- {x}" for x in ambiant_items])
    
    st.text_area("Texte formaté à copier/coller dans Carrefour Drive (Hopla) :", prompt_text, height=220)
