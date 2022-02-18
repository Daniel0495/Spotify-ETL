## ETL Spotify básico


Este proyecto pretende ser un ejercicio de práctica en la construcción de pipelines de datos. Toma los datos de reproducción de spotify, "limpia" los campos necesirios y finalmente guarda la información en una base de datos MySQL.

Es importante aclarar que es una primera version, por lo cual no pretende ser una solución óptima al "problema".

Si desea ejecutar el archivo, es necesario que configure un archivo .env y complete de la siguiente manera:
~~~
SPOTIFY_CLIENT_ID = 'spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'https://google.com'

MYSQL_PASSWORD= password
MYSQL_USER= user
MYSQL_HOST= host
MYSQL_DATABASE='spotify'
~~~