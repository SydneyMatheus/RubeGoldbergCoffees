#Disciplina:  12333 TÓP. ESPECIAIS EM INTEGRAÇÃO SOFTWARE HARDWARE
#Atividade: Trabalho M2 – Café de Rube Goldberg
#Versão 1
#Acadêmico(s): Sydney Matheus de Souza
#              Carlos Daniel Batista
#              Gabriel Farias Goi

import cv2
import math
import urllib.request
import numpy as np
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyDCNjoSmXJasSthJPlIiHoQ9dQjA8fJAck",
  "authDomain": "rubegoldberginths.firebaseapp.com",
  "databaseURL": "https://rubegoldberginths-default-rtdb.firebaseio.com",
  "projectId": "rubegoldberginths",
  "storageBucket": "rubegoldberginths.appspot.com",
  "messagingSenderId": "896241581822",
  "appId": "1:896241581822:web:5bb3659d75acb3b85cafaf",
  "measurementId": "G-XK9H6Z4XVN"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

cafePronto = 0
length = 300

while True:
    url = db.child("/serverUrl").get().val()                                #recebe a URL a qual a ESPCAN está enviando as imagens
    print(url)                                                              #'http://XXX.XXX.XXX.XXX/cam-lo.jpg'

    try:                                                                    #Arrumar o try para não englobar o código inteiro
        img_resp = urllib.request.urlopen(url)
        img = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img, -1)
        frameCut = frame[:,60:61]

        #print(frame.shape)                                                 # tamanho da IMG: 240x320

        gray = cv2.cvtColor(frameCut, cv2.COLOR_BGR2GRAY)                   #imagem cinza
        blackWhite = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)[1]    #imagem preto e branco
                                                                            #mais e menos detalhes podem ser definidos pelo threshold, 127 é o padrão

        length = np.sum(blackWhite == 255)         #Conta o total de pixels brancos
        print(length)

        if (length - 10) < 0:                      # A cada 200 amostras é verificado se o valor da linha ficou em torno de 125
            cafePronto += 1
            print("O café esta pronto! (" + str(cafePronto) + ") length: " + str(length))
            if cafePronto == 50:                    # Se for definido que esse tamanho é próximo a 125 ele verifica mais 2 vezes
                print("O café esta pronto!")        # Se em alguma dessas 3 vezes der que o café não ficou pronto ele refaz
                                                    # Para garantir que so seja computado quando o café realmente estiver pronto

                db.child("status").update({"coffe": True})
                break
        else:
            cafePronto = 0
            print("O café está em preparo!!! length:" + str(length))

        cv2.imshow("output", frame)
        cv2.imshow("Edges", blackWhite)

    except:
        print("A imagem não pode ser lida")

    key = cv2.waitKey(5)                                            #Parametro "0" espera infinitamente pressionar uma tecla, outro valor (>0) a espera é em ms
    if key == ord('q'):
        break

cv2.destroyAllWindows()