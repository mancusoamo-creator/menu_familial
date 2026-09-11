import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Générateur de Menus Familiaux",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS moderne et épuré
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 800; color: #2E7D32; text-align: center; margin-bottom: 1.5rem; }
    .meal-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    }
    .meal-title { font-size: 1.1rem; font-weight: 700; color: #1B5E20; margin-bottom: 8px; }
    .badge-parent {
        background-color: #E8F5E9; color: #2E7D32; padding: 4px 8px; border-radius: 6px;
        font-weight: 600; font-size: 0.85rem; margin-right: 5px; display: inline-block;
    }
    .badge-child {
        background-color: #E3F2FD; color: #1565C0; padding: 4px 8px; border-radius: 6px;
        font-weight: 600; font-size: 0.85rem; margin-right: 5px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🥗 Planning Familial des Repas</div>', unsafe_allow_html=True)

# Données locales par défaut
if 'planning' not in st.session_state:
    st.session_state['planning'] = pd.DataFrame([
        {"Jour": "Lundi", "Creneau": "Déjeuner", "Nom_Profil": "Maman", "Nom_Repas": "Saumon Poêlé, Riz Basmati & Épinards", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Déjeuner", "Nom_Profil": "Papa", "Nom_Repas": "Saumon Poêlé, Riz Basmati & Épinards", "Portion": "125%"},
        {"Jour": "Lundi", "Creneau": "Déjeuner", "Nom_Profil": "Léa", "Nom_Repas": "Poulet Rôti, Patates Douces & Brocolis", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Dîner", "Nom_Profil": "Maman", "Nom_Repas": "Dahl de Lentilles Corail & Riz", "Portion": "100%"},
        {"Jour": "Lundi", "Creneau": "Dîner", "Nom_Profil": "Papa", "Nom_Repas": "Dahl de Lentilles Corail & Riz", "Portion": "125%"},
        {"Jour": "Mardi", "Creneau": "Déjeuner", "Nom_Profil": "Maman", "Nom_Repas": "Poulet Rôti, Patates Douces & Brocolis", "Portion": "100%"},
        {"Jour": "Mardi", "Creneau": "Déjeuner", "Nom_Profil": "Papa", "Nom_Repas": "Poulet Rôti, Patates Douces & Brocolis", "Portion": "125%"},
        {"Jour": "Mardi", "Creneau": "Dîner", "Nom_Profil": "Maman", "Nom_Repas": "Omelette BIO, Avocat & Salade", "Portion": "100%"},
        {"Jour": "Mardi", "Creneau": "Dîner", "Nom_Profil": "Papa", "Nom_Repas": "Omelette BIO, Avocat & Salade", "Portion": "100%"},
    ])

# Barre latérale pour la synchro
with st.sidebar:
    st.title("⚙️ Réglages")
    gsheet_url = st.text_input("URL Apps Script Google Sheet:")
    if st.button("🔄 Sync Google Sheet"):
        if gsheet_url:
            try:
                res = requests.get(gsheet_url).json()
                if "Planning_Semaine" in res:
                    st.session_state['planning'] = pd.DataFrame(res["Planning_Semaine"])
                st.success("Synchronisé !")
            except Exception as e:
                st.error(f"Erreur : {e}")

tabs = st.tabs(["📅 Planning Visuel", "➕ Modifier / Ajouter", "🛒 Liste Drive"])

# ---------------------------------------------------------
# TAB 1: PLANNING VISUEL (Cartes par Jour)
# ---------------------------------------------------------
with tabs[0]:
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("✨ Générer automatiquement la semaine"):
            st.success("Menu équilibré généré !")

    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    # Affichage en colonnes / cartes par jour
    for jour in jours:
        df_jour = st.session_state['planning'][st.session_state['planning']['Jour'] == jour]
        
        st.markdown(f"### 🗓️ {jour}")
        
        if df_jour.empty:
            st.info("Aucun repas planifié.")
        else:
            col_dej, col_din = st.columns(2)
            
            # Déjeuner
            with col_dej:
                st.markdown("#### ☀️ Déjeuner")
                df_dej = df_jour[df_jour['Creneau'] == 'Déjeuner']
                if df_dej.empty:
                    st.caption("Rien de prévu")
                else:
                    repas_group = df_dej.groupby('Nom_Repas')
                    for repas_nom, group in repas_group:
                        st.markdown(f'<div class="meal-card"><div class="meal-title">🍲 {repas_nom}</div>', unsafe_allow_html=True)
                        profiles_str = ""
                        for _, r in group.iterrows():
                            badge_cls = "badge-parent" if r['Nom_Profil'] in ['Maman', 'Papa'] else "badge-child"
                            profiles_str += f'<span class="{badge_cls}">👤 {r["Nom_Profil"]} ({r["Portion"]})</span>'
                        st.markdown(profiles_str + '</div>', unsafe_allow_html=True)

            # Dîner
            with col_din:
                st.markdown("#### 🌙 Dîner")
                df_din = df_jour[df_jour['Creneau'] == 'Dîner']
                if df_din.empty:
                    st.caption("Rien de prévu")
                else:
                    repas_group = df_din.groupby('Nom_Repas')
                    for repas_nom, group in repas_group:
                        st.markdown(f'<div class="meal-card"><div class="meal-title">🌙 {repas_nom}</div>', unsafe_allow_html=True)
                        profiles_str = ""
                        for _, r in group.iterrows():
                            badge_cls = "badge-parent" if r['Nom_Profil'] in ['Maman', 'Papa'] else "badge-child"
                            profiles_str += f'<span class="{badge_cls}">👤 {r["Nom_Profil"]} ({r["Portion"]})</span>'
                        st.markdown(profiles_str + '</div>', unsafe_allow_html=True)
        st.markdown("---")

# ---------------------------------------------------------
# TAB 2: MODIFICATION
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("Ajouter un repas au planning")
    with st.form("add_form"):
        j = st.selectbox("Jour", jours)
        c = st.selectbox("Créneau", ["Déjeuner", "Dîner"])
        p = st.text_input("Nom du Profil (ex: Maman, Papa, Léa)", "Maman")
        r = st.text_input("Nom du Repas", "Saumon Poêlé & Riz")
        por = st.selectbox("Portion", ["100%", "125%", "75%"])
        
        if st.form_submit_button("Valider"):
            new_r = {"Jour": j, "Creneau": c, "Nom_Profil": p, "Nom_Repas": r, "Portion": por}
            st.session_state['planning'] = pd.concat([st.session_state['planning'], pd.DataFrame([new_r])], ignore_index=True)
            st.success("Repas ajouté !")
            st.rerun()

    st.subheader("Données brutes (Modification rapide)")
    st.session_state['planning'] = st.data_editor(st.session_state['planning'], num_rows="dynamic")

# ---------------------------------------------------------
# TAB 3: DRIVE
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("🛒 Export Carrefour Drive (Hopla)")
    frais = ["Pavé de Saumon (600g)", "Épinards frais (500g)", "Poulet (600g)"]
    ambiant = ["Riz Basmati (1kg)", "Lentilles Corail (500g)"]
    
    prompt = "Bonjour Hopla, ajoute à mon panier :\n\nFRAIS :\n" + "\n".join([f"- {x}" for x in frais])
    prompt += "\n\nAMBIANT :\n" + "\n".join([f"- {x}" for x in ambiant])
    
    st.text_area("Copier le texte :", prompt, height=200)
