from decouple import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import timedelta, datetime
import pandas as pd
from database_functions import *


scope = "user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config('SPOTIFY_CLIENT_ID'), 
                                               client_secret=config('SPOTIFY_CLIENT_SECRET'), 
                                               redirect_uri=config('SPOTIFY_REDIRECT_URI'), 
                                               scope=scope))


def extract(date, limit=50):
    """Obtiene las últimas canciones escuchadas.

    Args:
        date (datetime): fecha de consulta
        limit (int, optional): Límite de elementos a obtener
    """

    ds = int(date.timestamp()) * 1000
    return sp.current_user_recently_played(limit=limit) #, after=ds)


def transform(raw_data, date):
    data = []
    for r in raw_data["items"]:
        data.append(
            {
                "played_at": r["played_at"],
                "artist": r["track"]["artists"][0]["name"],
                "track": r["track"]["name"]
            }
        )
    df = pd.DataFrame(data)

    clean_df = df[pd.to_datetime(df["played_at"]).dt.date == date.date()]

    if not df["played_at"].is_unique:
        raise Exception("Un valor de 'played_at' no es único")

    if df.isnull().values.any():
        raise Exception("Hay un valor nulo en el DF")

    return clean_df


def load(data_clean):
    # Crear database 
    create_tables_database()


    for i,row in data_clean.iterrows():
        date = datetime.strptime(row['played_at'][:10] + ' ' + row['played_at'][11:19], '%Y-%m-%d %H:%M:%S')
        insert_database(date, row['artist'], row['track'])
        logger.info(f'{i} registros fueron almacenados en DB.')
    return


if __name__ == "__main__":
    date = datetime.today()  # - timedelta(days=1)
    print(date)

    # Extract
    data_raw = extract(date)
    print(f"Extraídos {len(data_raw['items'])} registros \n")

    # Transform
    clean_df = transform(data_raw, date)
    print(f"{clean_df.shape[0]} registros fueron transformados")
    print(clean_df)

    # Load
    load(clean_df)