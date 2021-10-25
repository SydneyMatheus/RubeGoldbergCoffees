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

};

url = 'http://192.168.137.123/cam-lo.jpg'   #substituir por uma requisição ao firebase
                                            #toda vez que inicia a camêra o URL pode mudar
cafePronto = 0
length = 300

while True:
    lastLine = np.zeros((1,1,2))
    lastLine[0][0][0] = 0
    lastLine[0][0][1] = 0
    lastLength = 0
    laps = 0
    while laps < 200:                                                   #executa 200 amostras para verificar se ficou pronto
        try:                                                            #Arrumar o try para não englobar o código inteiro
            img_resp = urllib.request.urlopen(url)
            img = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img, -1)
            frameCut = frame[:,60:160]

            #print(frame.shape) # tamanho da IMG: 240x320

            gray = cv2.cvtColor(frameCut, cv2.COLOR_BGR2GRAY)           #imagem cinza
            gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]  #imagem preto e branco
                                                                        #mais e menos detalhes podem ser definidos pelo threshold, 127 é o padrão

            edges = cv2.Canny(gray, 100, 120)                           #determina todos os contornos na img
            lines = cv2.HoughLinesP(edges, 1, math.pi / 1, 20, None, 2, 480)    #determina as linhas a partir dos contornos

            if lastLength == 0:                                         #Sistema para remover desvio padrão
                lastLine[0][0][0] = lines[0][0][1]
                lastLine[0][0][1] = lines[0][0][3]
                lastLength = lastLine[0][0][0] - lastLine[0][0][1]
            else:
                length = lines[0][0][1] - lines[0][0][3]
                lastLength = lastLine[0][0][0] - lastLine[0][0][1]

                if abs(lastLength - length)>20:                         #Se o tamanho da linha atual tiver uma diferença
                    lines[0][0][1] = lastLine[0][0][0]                  #de 20 da última linha ela é descartada
                    lines[0][0][3] = lastLine[0][0][1]
                else:
                    lastLine[0][0][0] = lines[0][0][1]
                    lastLine[0][0][1] = lines[0][0][3]

            if lines is None:                                          #remover depois
                print('O café ta pronto!')
            else:
                dot1 = (lines[0][0][0], lines[0][0][1])
                dot2 = (lines[0][0][2], lines[0][0][3])
                cv2.line(frame, dot1, dot2, (255, 0, 0), 3)
                cv2.imshow("output", frame)
                cv2.imshow("Edges", edges)
                length = lines[0][0][1] - lines[0][0][3]
                #print(length)

        except:
            print("A imagem não pode ser lida")
        #cap.release()

        key = cv2.waitKey(5)                                            #Parametro "0" espera infinitamente pressionar uma tecla, outro valor (>0) a espera é em ms
        if key == ord('q'):
            break
        laps += 1;
        #print(laps)

    if (length - 125) < 10:                                             #A cada 200 amostras é verificado se o valor da linha ficou em torno de 125
        cafePronto += 1
        print("O café esta pronto! (" + str(cafePronto) + ") length: " + str(length))
        if cafePronto == 3:                                             #Se for definido que esse tamanho é próximo a 125 ele verifica mais 2 vezes
            print("O café esta pronto!")                                #Se em alguma dessas 3 vezes der que o café não ficou pronto ele refaz
                                                                        #Para garantir que so seja computado quando o café realmente estiver pronto
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            db = firebase.database()

            db.child("status").update({"coffe": True})

            break
    else:
        cafePronto = 0
        print("O café está em preparo!!! length:" + str(length))

cv2.destroyAllWindows()