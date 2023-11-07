# ChallngeMM_Reco_Voz
ChallengeMM recognized by a regular user

# DESCRIPCION y FIABILIDAD:
Reco_Voz es un challenge multimedia que cuenta con dos modos de funcionamiento: 
1. Modo Parental, comprueba que el usuario es una persona adulta con la que se ha entrenado el modelo previamente.
2. Modo no parental, comprueba si el usuario es un usuario habitual (empleado de la empresa), lo hace mediante
reconocimiento de voz, dando como resultado la categoría correspondiente al modelo que presente más similitud
con la voz del usuario que desea acceder a la información.

# FUNCIONAMIENTO:
Este challenge requiere un proceso inicial de creación de base de datos y entrenamiento de modelos, esto se hace con el 
archivo crearBD_RV.py, donde se realizan capturas de 5 audios de cada usuario con los que se entrenarán los modelos y se
almacenan en la carpeta training_set con el nombre de la categoría correspondiente a cada usuario, para con estos entrenar
los modelos de mezcla gaussiana (gmm).

El challenge se encuentra en el fichero Reco_Voz.py donde se toma una captura de audio en el momento de la ejecución se pasa
a los modelo almacenados en la carpeta trained_models, devolviendo estos un score de similitud con cada uno de ellos. El challenge 
en modo empresarial devolverá la categoría correspondiente al modelo del usuario entrenado anteriormente con más similitud al
audio capturado. La clave resultante para el modo parental será 0 ó 1, siendo 1 el valor correcto si se trata de una adulto conocido. 

#Modelo de IA de gmm para reconocimiento de voz:
[https://docs.opencv.org/4.2.0/da/d60/tutorial_face_main.html#tutorial_face_eigenfaces](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html )

Para la extracción de características se ha utilizado Mel Frequency Cepstral Coefficient (MFCC) 
http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/ para extraer
las características de la muestra de audio. Para aprender sobre esta librería: https://python-speech-features.readthedocs.io/en/latest/ 

Las principales librerías usadas son las siguientes:

os para crear directorios y listar archivos. https://docs.python.org/es/3.10/library/os.html

wave para leer y escribir audios .wav en python. https://docs.python.org/3/library/wave.html 

pyaudio para el trabajo con audios en python. https://pypi.org/project/PyAudio/ 

python_speech_features para la extracción de características para el reconocimiento automático de voz, específicamente se ha utilizado Mel Frequency Cepstral Coefficient (MFCC) para extraer las características de la muestra de audio. Para aprender sobre esta librería: https://python-speech-features.readthedocs.io/en/latest/ 

sklearn.mixture para importar GaussianMixture,  librería que contiene el modelo de inteligencia artificial utilizado para el reconocimiento de voz, modelos de mezcla gaussiana (GMM). Para aprender sobre ello, ver: https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html 

Tkinter para las GUI de interacción con el usuario. Para instalar el módulo tkinter simplemente: pip install tkinter. Para aprender tkinter: https://www.pythontutorial.net/tkinter/ . Para instalar el módulo tkinter simplemente: pip install tkinter 

# REQUISITOS:
La variable de entorno SECUREMIRROR_CAPTURES que apunta al directorio donde se guardan las capturas de los challenges debe existir. Y en ella se deben crear los siguientes directorios:
testing_set: En este directorio se guardará el audio grabado durante la ejecución del challenge para reconocer la voz del usuario que desea acceder a la información.

trained_models: En este directorio se guardarán los modelos entrenados.

training_set: En este directorio se guardará la data de audios durante la ejecución del fichero crearBD_RV.py para entrenar los modelos.

Además, en la dirección de la variable de entorno también debe existir el fichero training_set_addition.txt, en este fichero se generará una lista de los nombres de los audios de la data de entrenamiento durante la ejecución del fichero crearBD_RV.py. Esto permitirá controlar la cantidad de audios generados por cada usuario y si no alcanza una cantidad igual a 5 audios no se genera un modelo correspondiente al usuario en cuestión.

Funtions_Recovoz.py: Este fichero contiene las funciones de extracción de características necesarias para el entrenamiento y prueba del modelo. 

Reco_Voz.py: Este fichero contiene el challenge de reconocimiento de voz

crearBD_RV.py: Este fichero permite la creación la base de datos de audios y el entrenamiento de los modelos.

El_Quijote.txt: Este fichero contiene el primer capítulo de la obra “El Quijote”, se utiliza para mostrar al usuario un fragmento de 512 caracteres, diferentes cada vez, para que los lea mientras se graban los audios. 

# Configuración para validar el challenge:

El valor del campo "FileName" debe ser "challenge_loader_python.dll". Dentro del campo "Props" debe haber varios pares clave-valor:

"module_python": Debe contener el nombre del archivo del módulo de python  (sin incluir ".py"). En este caso: "Reco_Voz".

"validity_time": el tiempo de validez del challenge en segundos (entero).

"refresh_time": el tiempo en segundos (entero) entre ejecuciones automáticas del challenge.

"modo": determina el modo de ejecución. El modo parental se selecciona si su valor es "parental". De lo contrario, se utiliza el modo no parental.

Otros campos como "Description" y "Requirements" son opcionales e informativos.

# EJEMPLO:
Ejemplo de configuración del challenge para el modo no parental:

{
	"FileName": "challenge_loader_python.dll",
	"Description": "Reco_Voz",
	"Props": {
		"module_python": "Reco_Voz",
		"validity_time": 3600,
    "metodo":"empresarial",

	},
	"Requirements": "microfono en PC"
}


A continuación se presenta una configuración en modo parental, para el caso de uso en empresas. 

{
	"FileName": "challenge_loader_python.dll",
	"Description": "Reco_Voz",
	"Props": {
		"module_python": "Reco_Voz",
		"validity_time": 3600,
    "metodo":"parental",

	},
	"Requirements": "microfono en PC"
}

