import pandas as pd
import numpy as np

def obtener_tipo_dato(columna):
    tipo_dato = str(columna.dtype)
    return tipo_dato

def obtener_porcentaje_faltante(columna):
    porcentaje_faltante = columna.isnull().sum() / len(columna) * 100
    return porcentaje_faltante

def obtener_frecuencia(columna):
    frecuencia = columna.value_counts()
    return frecuencia

def detectar_outliers(columna, umbral=3):
    z_scores = (columna - columna.mean()) / columna.std()
    outliers = np.abs(z_scores) > umbral
    porcentaje_outliers = outliers.sum() / len(columna)
    return outliers.sum(), porcentaje_outliers* 100

def recomendar_imputacion_categorica(columna, causa_faltante):
    porcentaje_faltante = obtener_porcentaje_faltante(columna)
    frecuencia = obtener_frecuencia(columna)

    print("Información de la columna:")
    print("Tipo de dato: Categórica")
    print("Porcentaje de datos faltantes:", porcentaje_faltante)
    print("Frecuencia de valores:")
    print(frecuencia)
    print("Causa de los datos faltantes:", causa_faltante)

    if causa_faltante == "MAR":
        return "Imputación múltiple"
    elif causa_faltante == "MCAR":
        if porcentaje_faltante < 5:
            valor_mas_frecuente = frecuencia.index[0]
            return f"Imputación con valor más frecuente ({valor_mas_frecuente})"
        else:
            return "Eliminación de filas con datos faltantes"
    elif causa_faltante == "MNAR":
        return "Modelo de imputación avanzado"

def recomendar_imputacion_numerica(columna, causa_faltante):
    porcentaje_faltante = obtener_porcentaje_faltante(columna)
    media = columna.mean()
    mediana = columna.median()
    outliers, porcentaje_outliers = detectar_outliers(columna)

    print("Información de la columna:")
    print("Tipo de dato: Numérica")
    print("Porcentaje de datos faltantes:", porcentaje_faltante)
    print("Media:", media)
    print("Mediana:", mediana)
    print("Maximo:", columna.max())
    print("Minimo:", columna.min())
    print("¿Cantidad outliers?:", outliers)
    print("¿Porcentaje outliers?:", porcentaje_outliers)
    print("Causa de los datos faltantes:", causa_faltante)

    if causa_faltante == "MAR":
        return "Imputación múltiple"
    elif causa_faltante == "MCAR":
        if porcentaje_faltante < 5:
            if outliers:
                return "Imputación con mediana"
            else:
                return "Imputación con media"
        else:
            return "Eliminación de filas con datos faltantes"
    elif causa_faltante == "MNAR":
        return "Modelo de imputación avanzado"

def recomendar_imputacion(columna, causa_faltante):
    tipo_dato = obtener_tipo_dato(columna)
    porcentaje_faltante = obtener_porcentaje_faltante(columna)

    if porcentaje_faltante == 0:
        return "No se requiere imputación, no hay datos faltantes"
    if tipo_dato == "object":
        return recomendar_imputacion_categorica(columna, causa_faltante)
    else:
        return recomendar_imputacion_numerica(columna, causa_faltante)
