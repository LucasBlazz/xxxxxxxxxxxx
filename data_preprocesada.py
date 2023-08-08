from ast import literal_eval
import pandas as pd
import funciones_auxiliares as fa



rows = []
with open("dataset_raw/steam_games.json") as f:
    for line in f.readlines():
        rows.append(literal_eval(line))

df = pd.DataFrame(rows)


#Tranformamos el tipo de dato de la columna "release_date" a datetime con el formato"YEAR-MONTH-DAY", dejando como NaT a los que no de este tipo.
df["release_date"] = pd.to_datetime(df["release_date"],format="%Y-%m-%d", errors="coerce")


#Eliminamos los registros que no tengan fecha de salida ya que es la columna mas importante para las funciones

df.dropna(subset=["release_date"], inplace=True)


#Creamos una columna que sea solo el año ya que no nos aporta nada saber el dia o mes

df["year_release"] = df["release_date"].dt.year




# Dataset para la funcion GENERO
df_genero = df.copy()
df_genero = df_genero[["year_release","genres"]]
df_genero.dropna(subset=["genres"], inplace=True)



# Dataset para la funcion JUEGOS
df_juegos = df[["year_release","app_name","specs"]]
df_juegos.dropna(subset="app_name",inplace=True)
df_juegos["dlc"] = df["specs"].apply(fa.contiene_DLC)
filtro_tiene_dlc = df_juegos["dlc"] == False
df_juegos = df_juegos[filtro_tiene_dlc]



# Dataset para funcion SPECS
df_specs = df[["specs","year_release"]]
df_specs.dropna(subset=["specs"],inplace=True)



# Dataset para funcion EARLY ACCESS
df_early_access = df[["app_name","early_access","specs","year_release"]]
filtro_es_early_acc = df_early_access["early_access"] == True
df_early_access = df_early_access[filtro_es_early_acc]


# Dataset para funcion SENTIMENT
df_sentiment = df[["sentiment","year_release"]]
df_sentiment.dropna(subset=["sentiment"], inplace=True)
df_sentiment["sentiment"].unique()
posibles_valores = ["Mostly Positive","Very Positive","Positive","Mixed","Negative","Very Negative","Overwhelmingly Negative"]
filtro_op_posibles = df_sentiment["sentiment"].apply((lambda x: any(opcion in x for opcion in posibles_valores)))
df_sentiment = df_sentiment[filtro_op_posibles]



# Dataset para funcion METASCORE
df_metascore = df[["app_name","metascore","specs","year_release"]]
df_metascore.dropna(subset=["metascore"],inplace=True)
df_metascore["metascore"] = pd.to_numeric(df_metascore["metascore"],errors="coerce")
df_metascore["dlc"] = df_metascore["specs"].apply(fa.contiene_DLC)
filtro_tiene_dlc = df_metascore["dlc"] == False
df_metascore = df_metascore[filtro_tiene_dlc]

#print(df_juegos.head(5))
#print(df_genero.head(5))