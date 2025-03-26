import cv2
import numpy as np
from tkinter import messagebox, Tk
import time
from datetime import datetime

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

    # Contador para controlar o tempo de 15 segundos antes de disparar o alerta
    start_time = time.time()

    # Variável para controlar o intervalo de captura de fotos
    last_photo_time = time.time()

    # Contador de capturas de foto
    photo_counter = 0
    max_photos = 5  # Definir o máximo de fotos a serem capturadas
    captured_photos = []  # Lista para armazenar as fotos capturadas

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
            if cv2.contourArea(contour) > 500:  # Ignora movimentos muito pequenos
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Caixa vermelha

                # Detecta rostos na imagem
                faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (fx, fy, fw, fh) in faces:
                    # Aumentando o tamanho do contorno do rosto
                    padding = 30  # Adiciona 30 pixels de padding ao redor do rosto detectado
                    fx, fy = max(0, fx - padding), max(0, fy - padding)
                    fw, fh = fw + 2 * padding, fh + 2 * padding

                    # Desenhando o contorno maior
                    cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)  # Caixa verde para rosto

                    # Verifica se já passaram 2 segundos desde a última captura de foto
                    if photo_counter < max_photos and (time.time() - last_photo_time) >= 2:
                        # Captura a foto do rosto detectado
                        face_image = frame[fy:fy + fh, fx:fx + fw]

                        # Gera um nome único para a foto com base na data e hora atual
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"face_detected_{timestamp}.jpg"

                        # Salva a foto com o nome único
                        cv2.imwrite(filename, face_image)
                        print(f"Foto salva como {filename}")

                        # Adiciona a foto à lista
                        captured_photos.append(face_image)

                        # Incrementa o contador de fotos
                        photo_counter += 1

                        # Atualiza o tempo da última captura
                        last_photo_time = time.time()

                        # Verifica se atingiu o limite de 5 fotos
                        if photo_counter >= max_photos:
                            print("Limite de fotos atingido. Não será tirada mais nenhuma foto.")

        # Exibe o frame atual
        cv2.imshow("Detecção de Invasão - Webcam", frame)

        # Controla o tempo de 15 segundos antes de exibir o alerta
        elapsed_time = time.time() - start_time
        if elapsed_time >= 15 and not alert_triggered:
            show_alert()
            alert_triggered = True

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

# Inicia a detecção de movimento
detect_motion()
