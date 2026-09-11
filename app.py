import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Le Planning Familial", page_icon="🥗", layout="wide")

# CSS pour répliquer le design exact de l'image (cartes arrondies, boutons discrets, puces de profils)
st.markdown("""
<style>
    .title-main { font-family: 'serif'; font-size: 2.3rem; font-weight: 700; color: #1C1917; margin-bottom: 0px; }
    .subtitle { color: #78716C; font-size: 0.95rem; margin-bottom: 20px; }
    .score-box { text-align: center; color: #78716C; font-size: 0.9rem; margin-bottom: 25px; }
    .score-val { color: #DC2626; font-weight: 700; }
    
    /* Grille et cartes */
    div[data-testid="column"] { padding: 3px !important; }
    
    .meal-box {
        border: 2px dashed #E7E5E4;
        border-radius: 12px;
        padding: 12px 8px;
        min-height: 80px;
        background-color: #FAFAF9;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .meal-box-filled {
        border: 1px solid #E7E5E4;
        border-radius: 12px;
        padding: 10px 8px;
        min-height: 80px;
        background-color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        position: relative;
    }
    .meal-title { font-weight: 700; font-size: 0.85rem; color: #1C1917; margin-bottom: 6px; }
    
    /* Puces circulaires pour les profils */
    .avatar-container { display: flex; gap: 4px; justify-content: center; align-items: center; }
    .avatar-p { background-color: #1E40AF; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 0.7rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; }
    .avatar-i { background-color: #065F46; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 0.7rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; }
    .avatar-m { background-color: #9D174D; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 0.7rem; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; }
    .badge-e { border: 1px dashed #DC2626; color: #DC2626; border-radius: 50%; width: 18px; height: 18px; font-size: 0.65rem; font-weight: 700; position: absolute; top: 4px; right: 4px; display: flex; align-items: center; justify-content: center; }
    
    /* Header des jours */
    .day-header { text-align: center; font-weight: 600; font-size: 0.9rem; color: #44403C; }
    .day-date { text-align: center; font-size: 0.75rem; color: #A8A29E; margin-bottom: 10px; }
    .row-label { font-weight: 600; font-size: 0.85rem; color: #44403C; display: flex; align-items: center; height: 80px; }
</style>
""", unsafe_allow_html=True)

# Initialisation des données d'exemple
if 'grid_data' not in st.session_state:
    st.session_state['grid_data'] = {
        ("Samedi", "Déjeuner"): {
            "repas": "Pâtes carbo",
            "profils": ["P", "I"],
            "equilibre": "E"
        }
    }

# Entête
st.markdown('<div class="title-main">Le planning</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Clique une case pour assigner un repas et les personnes concernées.</div>', unsafe_allow_html=True)

# Navigation semaine & Score
c_left, c_mid, c_right = st.columns([4, 3, 4])
with c_mid:
    st.markdown("<h3 style='text-align: center; margin: 0;'>‹ &nbsp;&nbsp; 14/09 → 20/09 &nbsp;&nbsp; ›</h3>", unsafe_allow_html=True)

nb_repas = len(st.session_state['grid_data'])
st.markdown(f'<div class="score-box">Équilibre de la semaine : <span class="score-val">0/100 (Déséquilibré)</span> sur {nb_repas} repas planifiés</div>', unsafe_allow_html=True)

jours = [
    ("Lun", "14/09", "Lundi"),
    ("Mar", "15/09", "Mardi"),
    ("Mer", "16/09", "Mercredi"),
    ("Jeu", "17/09", "Jeudi"),
    ("Ven", "18/09", "Vendredi"),
    ("Sam", "19/09", "Samedi"),
    ("Dim", "20/09", "Dimanche")
]
creneaux = ["Petit-déj", "Déjeuner", "Goûter", "Dîner"]

# Entêtes de colonnes (Jours)
cols = st.columns([1.2] + [1]*7)
with cols[0]:
    st.write("")
for i, (j_short, date, _) in enumerate(jours):
    with cols[i+1]:
        st.markdown(f'<div class="day-header">{j_short}</div><div class="day-date">{date}</div>', unsafe_allow_html=True)

# Grille interactive
for creneau in creneaux:
    cols = st.columns([1.2] + [1]*7)
    with cols[0]:
        st.markdown(f'<div class="row-label">{creneau}</div>', unsafe_allow_html=True)
    
    for i, (_, _, j_long) in enumerate(jours):
        with cols[i+1]:
            key = (j_long, creneau)
            item = st.session_state['grid_data'].get(key)
            
            if item:
                # Affichage du repas configuré
                avatars_html = "".join([f'<span class="avatar-{p.lower()}">{p}</span>' for p in item['profils']])
                badge_html = f'<div class="badge-e">{item["equilibre"]}</div>' if item.get("equilibre") else ""
                
                st.markdown(f'''
                    <div class="meal-box-filled">
                        {badge_html}
                        <div class="meal-title">{item["repas"]}</div>
                        <div class="avatar-container">{avatars_html}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button("✏️", key=f"edit_{j_long}_{creneau}", help="Modifier"):
                    st.session_state['selected_cell'] = key
            else:
                # Case vide avec bouton "+ Ajouter"
                if st.button("+ Ajouter", key=f"add_{j_long}_{creneau}", use_container_width=True):
                    st.session_state['selected_cell'] = key

# Dialogue pour ajouter/modifier un repas
if 'selected_cell' in st.session_state and st.session_state['selected_cell']:
    j_sel, c_sel = st.session_state['selected_cell']
    
    @st.dialog(f"Assigner un repas — {j_sel} ({c_sel})")
    def assign_meal():
        curr = st.session_state['grid_data'].get((j_sel, c_sel), {})
        
        repas_nom = st.text_input("Nom du repas", value=curr.get("repas", ""))
        profils_sel = st.multiselect("Personnes concernées", ["P", "I", "M"], default=curr.get("profils", ["P", "I"]))
        equilibre = st.checkbox("Marquer comme équilibré (E)", value=bool(curr.get("equilibre")))
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("Enregistrer", use_container_width=True, type="primary"):
                if repas_nom:
                    st.session_state['grid_data'][(j_sel, c_sel)] = {
                        "repas": repas_nom,
                        "profils": profils_sel,
                        "equilibre": "E" if equilibre else ""
                    }
                st.session_state['selected_cell'] = None
                st.rerun()
        with col_act2:
            if st.button("Supprimer", use_container_width=True):
                st.session_state['grid_data'].pop((j_sel, c_sel), None)
                st.session_state['selected_cell'] = None
                st.rerun()

    assign_meal()
