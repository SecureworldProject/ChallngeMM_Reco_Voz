# -*- coding: utf-8 -*-
import os
import wave
import time
import pickle
import pyaudio
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture 
from tkinter import messagebox, ttk
import tkinter as tk
import lock
from Funtions_Recovoz import calculate_delta, extract_features
from asyncio.windows_events import NULL
from functools import partial

warnings.filterwarnings("ignore")

props_dict = {}

def init(props):
    global props_dict
    print("CHALLENGE_RECO_VOZ --> Enter in init")

    # Props es un diccionario
    props_dict = props
    resultado = ('1', 1) #executeChallenge()
    if (resultado[1]>0):
        return 0
    else:
        return -1

def executeChallenge():
    print("CHALLENGE_RECO_VOZ --> Starting execute")
    #for key in os.environ: print(key, ':', os.environ[key])
    dataPath = os.environ['SECUREMIRROR_CAPTURES']

    print("CHALLENGE_RECO_VOZ --> Storage folder is:", dataPath)

    # Mecanismo de lock BEGIN
    # -----------------------
    lock.lockIN("Reco_Voz")

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 10
    device_index = 2
    audio = pyaudio.PyAudio()
    
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    if (numdevices>0):
        messagebox.showinfo(message="El challenge de Reconocimiento de Voz iniciara grabación de audio", title="Inicio de grabación audio")
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = 0,
                    frames_per_buffer=CHUNK)
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        messagebox.showinfo(message="El challenge de Reconocimiento de Voz ha finalizado la grabación de audio", title="Fin de grabación de audio")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
    else:
        messagebox.showinfo(message="Este challenge no se puede ejecutar porque no se encuentra micrófono en tu PC", title="No existe dispositivo de grabación de audio")
        lock.lockOUT("Reco_Voz")
        key_size = 0
        result = (NULL, key_size)
        print("CHALLENGE_RECO_VOZ --> result:", result)
        return result

    
    #cerramos el lock
    lock.lockOUT("Reco_Voz")

    #Se crea el archivo de audio
    OUTPUT_FILENAME="sample.wav"
    WAVE_OUTPUT_FILENAME=os.path.join(dataPath+"\\testing_set\\",OUTPUT_FILENAME)
    #trainedfilelist = open(dataPath+"\\testing_set_addition.txt", 'a')
    #trainedfilelist.write(OUTPUT_FILENAME+"\n")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

    source   = dataPath+"\\testing_set\\"
    modelpath = dataPath+"\\trained_models\\"
    test_file = dataPath+"\\testing_set_addition.txt"
    file_paths = open(test_file,'r')

    gmm_files = [os.path.join(modelpath,fname) for fname in
                  os.listdir(modelpath) if fname.endswith('.gmm')]

    models=[pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
         
    # Read the test directory and get the list of test audio files 

    sr,audio = read(source + OUTPUT_FILENAME)
    
    vector   = extract_features(audio,sr)
     
    log_likelihood = np.zeros(len(models)) 
    
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
     
    winner = np.argmax(log_likelihood)
    print("\tdetected as - ", int(speakers[winner]))

    #cad es el resultado que vamos a devolver si es modo parental entrara dentro del if y si no devolvera directamente cad la "categoria"
    cad=int(speakers[winner])
    time.sleep(1.0)  

    if props_dict['mode']=='parental':

        #si la categoria es 8 o 9 es el padre o madre por lo tanto devolvera un 1
        if cad>7:
            cad=1
        else:
            cad=0
            
    #y generamos el resultado
    cad="%d"%(cad)
    key = bytes(cad,'utf-8')
    key_size = len(key)
    result = (key, key_size)
    print("result:", result)
    return result



# esta parte del codigo no se ejecuta a no ser que sea llamada desde linea de comandos
if __name__ == "__main__":
    midict = {"mode":"noparental"}
    props_dict = midict
    executeChallenge()