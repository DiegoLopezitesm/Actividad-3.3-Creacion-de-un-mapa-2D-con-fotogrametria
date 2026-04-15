# 🧠 Pipeline de Fotogrametría 2D con OpenCV

## 📌 Descripción
Este proyecto implementa un pipeline completo de visión computacional para generar un **mapa 2D (panorama)** a partir de múltiples imágenes, simulando la captura aérea de un dron.

El enfoque se basa en **fotogrametría planar**, donde imágenes de una superficie plana se combinan mediante detección de características y transformaciones geométricas.

---

## 🎯 Objetivos
- Realizar **calibración de cámara** usando un patrón checkerboard  
- Capturar imágenes con traslape de una superficie plana  
- Aplicar técnicas de **stitching (unión de imágenes)**  
- Generar un **mapa 2D reconstruido**  

---

## ⚙️ Descripción del Pipeline

El sistema sigue las siguientes etapas:

1. **Calibración de Cámara**
   - Método de Zhang  
   - Obtención de matriz intrínseca y coeficientes de distorsión  

2. **Adquisición de Imágenes**
   - Imágenes con 60–70% de traslape  
   - Perspectiva cenital (tipo dron)  

3. **(Opcional) Corrección de Distorsión**
   - Uso de parámetros de calibración  

4. **Stitching de Imágenes**
   - Uso de OpenCV Stitcher (modo SCANS)  
   - Optimización global de homografías  

5. **Post-procesamiento**
   - Recorte automático de regiones negras  

---

## 🗂️ Estructura del Proyecto

Activity3.3/
│
├── calib/              # Imágenes de calibración (checkerboard)
├── images/             # Imágenes para generar el mapa
├── main.py             # Script principal
└── README.md           # Documentación

---

## 🚀 Instalación

pip install opencv-python numpy

---

## ▶️ Uso

python main.py

Salida generada:
mapa_2D_FINAL_STITCHER.jpg

---

## 📸 Recomendaciones para Captura de Imágenes

- Mantener **60–70% de traslape** entre imágenes  
- Mantener la cámara **paralela al plano**  
- Usar superficies con **textura (no lisas)**  
- Mantener **altura e iluminación constantes**  

---

## ⚠️ Problemas Comunes

- Error en stitching → aumentar traslape  
- Imagen recortada → ajustar parámetros  
- Distorsión → desactivar undistort  

---

## 🧠 Fundamento Teórico

El proyecto se basa en fotogrametría 2D, donde una escena plana se reconstruye utilizando homografías.

---

## 📄 Reflexión

Durante esta actividad se identificaron diversos retos, principalmente relacionados con la calidad de las imágenes y el traslape entre ellas. La detección de características depende en gran medida de la textura de la superficie, por lo que escenas uniformes dificultan el proceso. Además, se observó que el uso del Stitcher de OpenCV mejora significativamente la consistencia geométrica frente a métodos manuales. Finalmente, se concluye que la calidad de los datos de entrada es determinante en el desempeño del pipeline.

---

## 👨‍💻 Autor
Diego López  
ITESM – Ingeniería en Robótica y Sistemas Digitales
