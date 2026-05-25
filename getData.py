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
df_ciqual = load_ciqual_to_dataframe(path)

# Visualisation des 5 premières lignes
if df_ciqual is not None:
    print(df_ciqual.info())