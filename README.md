# Proyecto individual MLOps
### Esta es mi solución a la propuesta de trabajo dictada por Henry

![api](https://drive.google.com/file/d/18-STyrV8-wvr53NC-eEevXrVZdM1kBIH/view?usp=sharing)

Para ver la consigna del proyecto visitar el [repositorio](https://github.com/soyHenry/PI_ML_OPS/tree/ft).

### Deploy hecho en render
### https://pi-mlops-6ztl.onrender.com/docs

    ⚠️Demora hasta 3 minutos en levantar⚠️
#### Distribución del proyecto:
    ├─── dataset
    |   └─── steam_games.json
    ├─── scripts
    |   └─── data_prepocesada.py
    |   └─── eda.ipynb
    |   └─── funciones_auxiliares.py
    |   └─── modelo_precio_videojuego.pkl
    └─── .gitignore
    └─── main.py
    └─── readme.md
    └─── requirements.txt

#### Detalles de los archivos:

- **steam_games.json**: Dataset original.
- **data_prepocesada.py**: Script de transformaciones del dataset para los endpoints de la api.
- **eda.ipynb**: EDA (Exploratory Data Analysis) y entrenamiento del modelo de predicción.
- **modelo_precio_videojuego.pkl**: Modelo de machine learning entrenado.
- **main.py**: La API.
- **readme.md**: Readme del proyecto.
- **requirements.txt**: Dependencias para que la api funcione correctamente.

#### Como levantar el proyecto en local

1. Instalar las dependencias del proyecto que se encuentran en **requirements.py** usando pip

    🚧 *Advertencia: se recomienda crear previamente un entorno virtual usando [conda](https://docs.conda.io/en/latest/) o [pyenv](https://github.com/pyenv/pyenv)*.

    En este caso usaremos conda
    
        conda create -n nombreEjemplo python3

    Activamos el entorno virtual

        conda activate nombreEjemplo
    
    Ahora si, instalamos las dependencias del proyecto con pip

        pip install -r requirements.py

2. Ya estamos listos para levantar el proyecto, abrimos nuestra terminal de preferencia, nos movemos a la carpeta del proyecto y escribimos el siguiente comando

        uvicorn main:app

    Esperamos que se complete el startup y listo, para probar la api dirigirse al localhost.

        http://127.0.0.1:8000/docs
    
    
### Contacto
🔗 LinkedIn: [Lucas Ramos](https://www.linkedin.com/in/luc-ramos/) |
📧 Correo: lu.ramos.2k@gmail.com

