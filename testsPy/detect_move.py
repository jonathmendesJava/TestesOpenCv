import cv2
import numpy as np
from tkinter import messagebox, Tk
import time

# Função para exibir o alerta em uma janela Tkinter
def show_alert():
    root = Tk()
    root.withdraw()  # Não queremos a janela principal
    messagebox.showwarning("Alerta", "Invasão detectada!")
    root.destroy()

# Função para detectar movimento
def detect_motion():
    # Inicializa a captura da webcam
    cap = cv2.VideoCapture(0)

    # Inicializa o fundo (imagem de referência para comparação)
    background_subtractor = cv2.createBackgroundSubtractorMOG2()

    # Carregar o classificador Haar Cascade para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Flag para garantir que o alerta seja exibido apenas uma vez
    alert_triggered = False

    # Contador para controlar o tempo de 15 segundos
    start_time = time.time()

    while True:
        # Captura o frame da câmera
        ret, frame = cap.read()

        if not ret:
            break

        # Converte o frame para escala de cinza (para reduzir complexidade)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplica o subtrator de fundo para detectar mudanças
        fg_mask = background_subtractor.apply(gray_frame)

        # Aplica dilatação para melhorar a visibilidade das mudanças
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)

        # Encontra os contornos do movimento detectado
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Se houver movimento (contornos encontrados), destacamos na imagem
        for contour in contours:
            if cv2.contourArea(contour) > 700:  # Ignora movimentos muito pequenos
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Caixa vermelha

                # Detecta rostos na imagem
                faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (fx, fy, fw, fh) in faces:
                    cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)  # Caixa verde para rosto

                    # Captura a foto do rosto detectado
                    face_image = frame[fy:fy + fh, fx:fx + fw]
                    cv2.imwrite("face_detected.jpg", face_image)  # Salva a foto

                # Controla o tempo de 15 segundos antes de exibir o alerta
                elapsed_time = time.time() - start_time
                if elapsed_time >= 15 and not alert_triggered:
                    show_alert()
                    alert_triggered = True

        # Exibe o frame atual
        cv2.imshow("Detecção de Invasão - Webcam", frame)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

# Inicia a detecção de movimento
detect_motion()
