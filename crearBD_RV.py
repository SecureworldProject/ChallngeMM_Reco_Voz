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
from Funtions_Recovoz import calculate_delta, extract_features
from tkinter import messagebox, ttk
import tkinter as tk
import random
from tkinter import *

warnings.filterwarnings("ignore")

def record_audio_train():
    #for key in os.environ: print(key, ':', os.environ[key])
    dataPath = os.environ['SECUREMIRROR_CAPTURES']
    modelpath = dataPath+"\\trained_models\\"
    gmm_files = [os.path.join(modelpath,fname) for fname in
                  os.listdir(modelpath) if fname.endswith('.gmm')]
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    name =str(len(models))
    for count in range(5):
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
            url_text= dataPath+"\\El_Quijote.txt"
            text=open(url_text,'r', encoding="utf-8")

            #skip zero header
            text.seek(random.randint(0, 10000))

            #reading information header 
            text_view = text.read(512)
            
            totall_text = StringVar()
            totall_text.set(text_view)

            totall = Label(main_window, textvariable=totall_text)
            totall.place(width=700, height=200)            

            messagebox.showinfo(message="Se iniciará la grabación del audio "+ str(count+1)+ " de 5 para crear la data del usuario. Debe ACEPTAR este mensaje y LEER EN VOZ ALTA EL MENSAJE QUE APARECE EN PANTALLA", title="Inicio de grabación audio")
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index = 0,
                        frames_per_buffer=CHUNK)
            Recordframes = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                Recordframes.append(data)
            messagebox.showinfo(message="Se ha finalizado la grabación del audio " + str(count+1), title="Fin de grabación de audio")
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        
        else:
            messagebox.showinfo(message="Este challenge no se puede ejecutar porque no se encuentra micrófono en tu PC", title="No existe dispositivo de grabación de audio")
            exit()

        
        
        OUTPUT_FILENAME=name+"-sample"+str(count)+".wav"
        WAVE_OUTPUT_FILENAME=os.path.join(dataPath+"\\training_set\\",OUTPUT_FILENAME)
        trainedfilelist = open(dataPath+"\\training_set_addition.txt", 'a')
        
        trainedfilelist.write(OUTPUT_FILENAME+"\n")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()



def train_model():
    #for key in os.environ: print(key, ':', os.environ[key])
    dataPath = os.environ['SECUREMIRROR_CAPTURES']
    source   = dataPath+"\\training_set\\"   
    dest = dataPath+"\\trained_models\\"
    train_file = dataPath+"\\training_set_addition.txt"        
    file_paths = open(train_file,'r')
    
    count = 1
    c=0
    features = np.asarray(())
    for path in file_paths:    
        path = path.strip()   
        print(path)
        


        sr,audio = read(source + path)
        print(sr)
        vector   = extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        if count == 5:  
            c+=1  
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            
            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            pickle.dump(gmm,open(dest + picklefile,'wb'))
            print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
            features = np.asarray(())
            count = 0
        count = count + 1
    totall_text = StringVar()
    
    totall_text.set("Se han entrenado " + str(len(os.listdir(dest)))+" modelos satisfactoriamente")

    totall = Label(main_window, textvariable=totall_text)
    totall.place(width=700, height=200)

def accept_selection():
    # Obtener la opción seleccionada.
    selection = combo.get()
    if (selection=="Grabar audio para entrenamiento"):
        record_audio_train()
    elif(selection=="Entrenar modelos"):
        train_model()
    else:
        exit()

main_window = tk.Tk()
main_window.config(width=700, height=200)
main_window.title("Challenge de Reconocimiento de Voz")

label_text = StringVar()
label_text.set("Seleccione la accion que desea realizar:")
label=Label(main_window, textvariable=label_text)
label.place(width=500, height=70)  
combo = ttk.Combobox(
    state="readonly",
    values=["Grabar audio para entrenamiento", "Entrenar modelos"]
)


combo.config(width=50, height=50)
combo.place(x=150, y=50)
button = ttk.Button(text="Aceptar", command=accept_selection)
button.place(x=550, y=150)
main_window.mainloop(0)