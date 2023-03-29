import cv2
import numpy as np
import serial

arduino = serial.Serial('COM4', 9600)

cap = cv2.VideoCapture(0)
x1, x2, y1, y2 = 214, 428, 160, 320
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read() 
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Conversion de datos de colores 

    ColorMin2 = np.array([136,87,111], dtype=np.uint8)
    ColorMax2 = np.array([255,255,180], dtype=np.uint8)
    mascara2 = cv2.inRange(frameHSV, ColorMin2, ColorMax2)

    contornos,_ = cv2.findContours(mascara2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.rectangle(frame,(x1, y1), (x2, y2), (255,255,255), 2)
    
    if len(contornos) > 0:
        c = max(contornos, key=cv2.contourArea) #si es mayor a 3000 el area del contorno se dibujara 
        M = cv2.moments(c)
        if (M["m00"] == 0): M["m00"] = 1
        #coordenadas del centroide
        x = int(M["m10"]/ M["m00"])
        y = int(M["m01"]/ M["m00"])
        
        Coord = (x, y)

        if cv2.contourArea(c) > 3000:
            #Dibuja un punto en el centro
            cv2.circle(frame, (Coord), 7, (255, 255, 255), -1)
            #escribe las coordenadas del centroide en pantalla
            cv2.putText(frame, '{}, {}'.format(x,y), (x+10, y),font, 1, (255, 255, 255), cv2.LINE_4) 
        
            if (x > 214 and x < 428) and (y > 160 and y < 320):
                arduino.write(b"centro\n")
            else: 
                if y > 240:
                    arduino.write(b"adelante\n")
                    if x < 214:
                        arduino.write(b"der\n")
                    if x > 214 and x < 428:
                        arduino.write(b"cenArr")
                    if x > 428:
                        arduino.write(b"izq\n")
                else:
                    arduino.write(b"atras\n")
                    if x < 214:
                        arduino.write(b"der\n")
                    if x > 214 and x < 428:
                        arduino.write(b"CenAba\n")
                    if x > 428:
                        arduino.write(b"izq\n")
        else: 
            cv2.putText(frame, 'Buscando...'.format(str), (250, 200),font, 1, (255, 255, 255), cv2.LINE_4)
            arduino.write(b"Buscar\n")

        
    cv2.imshow('frame2', mascara2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        arduino.close()
        break

cap.release()
cap.destroyAllWindows
