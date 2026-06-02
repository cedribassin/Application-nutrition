import pandas as pd

def load_ciqual_to_dataframe(file_path):
    try:
        # 1. Chargement du fichier Excel
        # On utilise engine='openpyxl' pour le format .xlsx
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # 2. Nettoyage technique initial
        # Supprime les espaces en début/fin de nom de colonne
        df.columns = df.columns.str.strip()
        
        # 3. Conversion des types (Optionnel)
        # S'assurer que le code aliment est traité comme une chaîne pour éviter de perdre les zéros non significatifs
        if 'alim_code' in df.columns:
            df['alim_code'] = df['alim_code'].astype(str)
            
        print(f"✅ Chargement réussi : {df.shape[0]} lignes et {df.shape[1]} colonnes détectées.")
        return df

    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return None

# Utilisation
path = 'ciqual.xlsx'
df_ciqual_original = load_ciqual_to_dataframe(path)

# Visualisation des 5 premières lignes
if df_ciqual_original is not None:
    print(df_ciqual_original.info())

#------------------------------------------------
# Réduction du DataFrame pour ne garder quelques aliments pertinents

# On récupère la liste de toutes les colonnes réelles du fichier
all_columns = df_ciqual_original.columns.tolist()

# Dictionnaire pour mapper nos mots-clés aux vrais noms de colonnes contenant des retours à la ligne
mapped_columns = {}

# Mots-clés simples à chercher dans les en-têtes
keywords = {
    'alim_nom_fr': 'alim_nom_fr',
    'Energie': 'Energie',
    'Eau': 'Eau',
    'Protéines': 'Protéines',
    'Glucides': 'Glucides',
    'Lipides': 'Lipides'
}

# On balaie les colonnes réelles pour trouver celles qui contiennent nos mots-clés
for key, keyword in keywords.items():
    found = [col for col in all_columns if keyword in str(col)]
    if found:
        mapped_columns[key] = found[0] # On prend la première correspondance trouvée
    else:
        print(f"⚠️ Attention : Impossible de trouver une colonne contenant '{keyword}'")

# On vérifie si on a bien trouvé nos 6 colonnes
if len(mapped_columns) == 6:
    print("✅ Toutes les colonnes ont été associées avec succès !")
    
    # On filtre en utilisant les vrais noms trouvés dynamiquement
    columns_to_keep = list(mapped_columns.values())
    df_filtered = df_ciqual_original[columns_to_keep].copy()
    
    # Pour que ce soit plus simple pour toi, on renomme proprement ces colonnes complexes
    df_filtered.columns = list(mapped_columns.keys())
    
    # ---- Insertion du filtre des lignes ----
    aliments_vises = [
        'Carotte, crue', 'Laitue, crue', 'Poivron rouge, cru', 
        "Brocoli, bouilli/cuit à l'eau, croquant", 
        'Pomme de terre sautée/poêlée/rissolée, préfrite, surgelée, cuite', 
        'Banane, chair sans peau, crue', 'Orange, chair sans peau, sans pépins, crue', 
        'Raisin cru (aliment moyen)', 'Riz basmati, cuit, sans sel ajouté', 
        'Pâtes sèches, standard, cuites, sans sel ajouté', 'Boeuf, steak ou bifteck grillé/poêlé', 
        'Poulet, filet sans peau grillé/poêlé', 'Boeuf, steak haché 15% MG cru', 
        'Oeuf dur', 'Oeuf au plat, sans matière grasse'
    ]
    
    # Application du filtre sur la colonne désormais appelée 'alim_nom_fr'
    df_final = df_filtered[df_filtered['alim_nom_fr'].isin(aliments_vises)].reset_index(drop=True)
    
    print(df_final.head())
    
else:
    print("❌ Erreur : Il manque des colonnes, le filtrage a échoué.")