"""
Pipeline de Generación de Mapa 2D mediante Stitching de Imágenes

Este script implementa un flujo completo que incluye:
1. Calibración de cámara (método de Zhang)
2. Generación de panorama utilizando OpenCV Stitcher (modo SCANS)
3. Recorte automático de regiones inválidas

Autor: Diego Hilario López Rodríguez
Curso: TE3003.B
"""

import cv2
import numpy as np
import glob

# =========================
# CONFIGURACIÓN
# =========================
CHECKERBOARD = (7,5)
CALIB_PATH = "calib/*.jpeg"
IMG_PATH = "images/*.jpeg"


# =========================
# 1. CALIBRACIÓN DE CÁMARA
# =========================
def calibrate_camera():
    """
    Realiza la calibración de la cámara utilizando imágenes de un patrón tipo checkerboard.
    
    Retorna:
        K: matriz intrínseca de la cámara
        dist: coeficientes de distorsión
    """
    
    objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    objpoints = []  # puntos en el mundo real
    imgpoints = []  # puntos en la imagen

    images = glob.glob(CALIB_PATH)

    if len(images) == 0:
        raise Exception("No se encontraron imágenes en la carpeta /calib")

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

    ret, K, dist, _, _ = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    print(" Calibración completada correctamente")
    return K, dist


# =========================
# 2. CORRECCIÓN DE DISTORSIÓN
# =========================
def undistort_images(images, K, dist):
    """
    Aplica corrección de distorsión a un conjunto de imágenes.
    
    Parámetros:
        images: lista de imágenes
        K: matriz intrínseca
        dist: coeficientes de distorsión
    
    Retorna:
        Lista de imágenes corregidas
    """
    undistorted = []
    for img in images:
        corrected = cv2.undistort(img, K, dist)
        undistorted.append(corrected)
    return undistorted


# =========================
# 3. STITCHING AUTOMÁTICO
# =========================
def stitch_opencv(images):
    """
    Genera un panorama utilizando el módulo Stitcher de OpenCV en modo SCANS,
    adecuado para superficies planas (vista cenital).
    
    Parámetros:
        images: lista de imágenes
    
    Retorna:
        Imagen panorama o None si falla
    """
    print(" Ejecutando OpenCV Stitcher (modo SCANS)...")

    stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)

    # Ajuste del umbral de confianza para mejorar robustez
    stitcher.setPanoConfidenceThresh(0.2)

    status, pano = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        print(f" Error en stitching: {status}")
        return None

    print(" Stitching completado exitosamente")
    return pano


# =========================
# 4. RECORTE AUTOMÁTICO
# =========================
def crop_black(image):
    """
    Elimina bordes negros generados durante el proceso de stitching.
    
    Parámetros:
        image: imagen panorama
    
    Retorna:
        Imagen recortada
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)

    return image[y:y+h, x:x+w]


# =========================
# 5. FUNCIÓN PRINCIPAL
# =========================
def main():
    """
    Ejecuta el pipeline completo:
    calibración → carga de imágenes → stitching → recorte → guardado
    """

    # Calibración de cámara
    K, dist = calibrate_camera()

    # Carga de imágenes
    image_paths = sorted(glob.glob(IMG_PATH))

    if len(image_paths) == 0:
        raise Exception("No se encontraron imágenes en la carpeta /images")

    images = [cv2.imread(p) for p in image_paths]

    print(f" {len(images)} imágenes cargadas correctamente")

    # Nota: se puede activar si se desea corrección de distorsión
    # images = undistort_images(images, K, dist)

    # Generación del panorama
    panorama = stitch_opencv(images)

    if panorama is None:
        print(" No fue posible generar el mapa 2D")
        return

    # Recorte de bordes negros
    panorama = crop_black(panorama)

    # Guardado del resultado
    cv2.imwrite("mapa_2D_FINAL_STITCHER.jpg", panorama)

    print(" Mapa generado exitosamente: mapa_2D_FINAL_STITCHER.jpg")


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    main()