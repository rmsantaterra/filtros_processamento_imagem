from imagens_transformacoes import imagem_to_cinza
from imagens_files import file_to_matriz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as im
import os
import sys
sys.path.insert(0, os.path.join('..'))

def getMatrizBlur(matriz_cinza):
    matriz_imagem_blur = matriz_cinza.copy()

    lins = matriz_cinza.shape[0]
    cols = matriz_cinza.shape[1]

    m = matriz_cinza
    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_imagem_blur[i][j] = (
                1*m[i-1][j-1] + 1*m[i-1][j] + 1*m[i-1][j+1] +
                1*m[i][j-1] + 1*m[i][j] + 1*m[i][j+1] +
                1*m[i+1][j-1] + 1*m[i+1][j] + 1*m[i+1][j+1]
            )/9
    return matriz_imagem_blur


def filterBlur(matriz_cinza):
    matriz_imagem_blur = getMatrizBlur(matriz_cinza)
    plt.imshow(matriz_imagem_blur, cmap='gray')
    plt.show()


def filterSobel(matriz_cinza):

    lins = matriz_cinza.shape[0]
    cols = matriz_cinza.shape[1]

    matriz_imagem_sobel_vertical = matriz_cinza.copy()
    matriz_imagem_sobel_horizontal = matriz_cinza.copy()

    m = matriz_cinza
    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_imagem_sobel_vertical[i][j] = (
                1*m[i-1][j-1] + 0*m[i-1][j] + -1*m[i-1][j+1] +
                2*m[i][j-1] + 0*m[i][j] + -2*m[i][j+1] +
                1*m[i+1][j-1] + 0*m[i+1][j] + -1*m[i+1][j+1]
            )
            matriz_imagem_sobel_vertical[i][j] = max(
                0, matriz_imagem_sobel_vertical[i][j])
            matriz_imagem_sobel_vertical[i][j] = min(
                255, matriz_imagem_sobel_vertical[i][j])

    m = matriz_cinza
    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_imagem_sobel_horizontal[i][j] = (
                1*m[i-1][j-1] + 2*m[i-1][j] + 1*m[i-1][j+1] +
                0*m[i][j-1] + 0*m[i][j] + 0*m[i][j+1] +
                -1*m[i+1][j-1] + -2*m[i+1][j] + -1*m[i+1][j+1]
            )
            matriz_imagem_sobel_horizontal[i][j] = max(
                0, matriz_imagem_sobel_horizontal[i][j])
            matriz_imagem_sobel_horizontal[i][j] = min(
                255, matriz_imagem_sobel_horizontal[i][j])
    
    matriz_imagem_sobel = matriz_imagem_sobel_horizontal + matriz_imagem_sobel_vertical
    
    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_imagem_sobel[i][j] = max(0, matriz_imagem_sobel[i][j])
            matriz_imagem_sobel[i][j] = min(255, matriz_imagem_sobel[i][j])

    
    plt.imshow(matriz_imagem_sobel, cmap='gray')
    plt.show()


def filterSharpening(matriz_cinza):
    matriz_blur = getMatrizBlur(matriz_cinza)

    lins = matriz_cinza.shape[0]
    cols = matriz_cinza.shape[1]

    mc = matriz_cinza
    mb = matriz_blur
    matriz_original_subtraido_blur = matriz_cinza.copy()

    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_original_subtraido_blur[i][j] = mc[i][j] - mb[i][j]

            matriz_original_subtraido_blur[i][j] = min(
                255, matriz_original_subtraido_blur[i][j])

    matriz_sharpening = matriz_cinza.copy()

    for i in range(1, lins-1):
        for j in range(1, cols-1):
            matriz_sharpening[i][j] = mc[i][j] + matriz_original_subtraido_blur[i][j]

            matriz_sharpening[i][j] = max(
                0, matriz_sharpening[i][j])
            matriz_sharpening[i][j] = min(
                255, matriz_sharpening[i][j])

    plt.imshow(matriz_sharpening, cmap='gray')
    plt.show()

if __name__ == "__main__":
    nome_file = os.path.join('.', 'imagens', 'flor.jpg')
    matriz = file_to_matriz(nome_file)
    matriz_cinza = imagem_to_cinza(matriz)

    print(
        """Digite o filtro desejado:
        
        [1] - Blur
        [2] - Sobel (Clareamento das bordas)
        [3] - Sharpening"""
    )

    optionSelected = int(input())

    if optionSelected == 1:
        filterBlur(matriz_cinza)
    elif optionSelected == 2:
        filterSobel(matriz_cinza)
    elif optionSelected == 3:
        filterSharpening(matriz_cinza)
    else:
        print('Opção inexistente')
