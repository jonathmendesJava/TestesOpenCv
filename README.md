📷 Sistema de Detecção de Invasão com OpenCV 📷

Este projeto utiliza a webcam para monitoramento e detecção de invasão em um ambiente. Ele analisa movimentos, detecta rostos e captura imagens quando uma possível invasão é identificada.

🚀 Funcionalidades

Monitoramento em tempo real utilizando a webcam.

Detecção de movimento para identificar possíveis invasores.

Reconhecimento facial para capturar imagens dos intrusos.

Captura automática de imagens (limite de 5 capturas por evento).

Aviso de invasão após o processamento das capturas.

🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes bibliotecas:

1️⃣ OpenCV (cv2)

Biblioteca principal para processamento de imagens e detecção de movimento.

Principais funções utilizadas:

cv2.VideoCapture(0): Captura o vídeo da webcam.

cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY): Converte o quadro para escala de cinza.

cv2.absdiff(frame_anterior, frame_atual): Calcula a diferença entre quadros para detectar movimento.

cv2.findContours(): Identifica contornos dos objetos em movimento.

cv2.CascadeClassifier('haarcascade_frontalface_default.xml'): Detecta rostos no vídeo.

cv2.rectangle(): Desenha retângulos ao redor dos rostos.

cv2.imshow(): Exibe a câmera ao vivo.

cv2.imwrite(): Salva imagens capturadas.

2️⃣ NumPy (numpy)

Usado para operações matemáticas e manipulação de arrays.

Principais usos:

np.array(): Cria arrays para armazenar frames.

np.mean(): Cálculo de médias para processamento de imagem.

3️⃣ PIL (Pillow)

Biblioteca para manipulação de imagens.

Principal uso no projeto:

Image.open(): Abre e processa imagens capturadas.

4️⃣ Tkinter (tkinter)

Usado para exibir mensagens e interfaces simples.

Exemplo:

tkinter.messagebox.showwarning("Alerta", "Invasão Detectada!")

🔧 Como Executar o Projeto

1️⃣ Instalar as dependências:

pip install opencv-python numpy pillow

2️⃣ Executar o código principal:

python detect_invasao.py

📸 Exemplo de Funcionamento

O sistema inicia a webcam e monitora o ambiente.

Caso um movimento significativo seja detectado, a captura é ativada.

O sistema identifica rostos e salva até 5 imagens.

Após capturar as imagens, é exibido um aviso de invasão.

O monitoramento continua até que o usuário finalize o programa.

📌 Melhorias Futuras 📌

📌 Envio de alertas via e-mail ou Telegram.

📌 Implementação de um banco de dados para armazenar capturas.

📌 Integração com sistemas de segurança externos.

👨‍💻 Autor: Jonath Mendes
📌 GitHub: jonathmendesJava

Se gostou do projeto, deixe uma ⭐ no repositório!
