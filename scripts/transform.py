import pandas as pd

def transform_data(df):
    # Gestion des valeurs manquantes
    df['reason_start'].fillna('unknown', inplace=True)
    df['reason_end'].fillna('unknown', inplace=True)

    # Conversion des types
    df['ts'] = pd.to_datetime(df['ts'])
    df['ms_played'] = df['ms_played'].astype(int)

    # Création de nouvelles colonnes
    df['minutes_played'] = df['ms_played'] / 60000
    df['day_of_week'] = df['ts'].dt.day_name()
    df['hour_of_day'] = df['ts'].dt.hour

    # Nettoyage des chaînes de caractères
    df['track_name'] = df['track_name'].str.title().str.strip()
    df['artist_name'] = df['artist_name'].str.title().str.strip()
    df['album_name'] = df['album_name'].str.title().str.strip()

    # Suppression des doublons
    df.drop_duplicates(subset=['ts', 'artist_name', 'track_name'], inplace=True)

    # Filtrage des écoutes de moins de 5 secondes
    df = df[df['ms_played'] >= 5000]
    
    print("Transformation réussie, voici un aperçu des données transformées :")
    print(df.head())
    
    return df

