import pandas as pd

def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Extraction réussie, voici un aperçu des données :")
        print(df.head())
        return df
    except Exception as e:
        print(f"Erreur lors de l'extraction des données : {e}")
        return None


