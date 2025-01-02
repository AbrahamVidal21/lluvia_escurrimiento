import pandas as pd
import numpy as np

# Definir la función para calcular He (Método de Horton)
def calcular_he_horton(p, k, t):
    # Fórmula de Horton para el cálculo de He
    he = p * (1 - np.exp(-k * t))
    return he

# Método de HUT para cálculo de Gasto de Diseño
def calcular_gasto_hut(hpe, area, tiempo_base):
    # Fórmula de HUT para calcular el Gasto
    Q = 0.566 * ((hpe * area) / tiempo_base)
    return Q

# Supongamos que tienes un archivo Excel con las siguientes columnas: Periodo de retorno, Precipitación (Hp), Número de curva (N)
archivo_excel = "lluvia.xlsx"

# Leer los datos desde el archivo Excel
try:
    datos_lluvia = pd.read_excel(archivo_excel)
    print("Datos de lluvia por periodo de retorno:")
    print(datos_lluvia)
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_excel}' no se encontró en la raíz del proyecto.")
except Exception as e:
    print(f"Se produjo un error al leer el archivo: {e}")

# Definir los valores constantes
numero_curva = 91.9276  # Número de curva constante para todas las filas
Tc = 1.10  # Tiempo de concentración en horas (asumido, ajusta si es necesario)
e = 0.53  # Parámetro 'e' proporcionado
area_cuenca = 76100  # Área de la cuenca en m² (7.61 km²)
area_cuenca_hut = 7.61

# Definir una lista vacía para los resultados de la tabla original
resultados = []
# Definir una lista vacía para los resultados con Hpd, Numero de Curva y He
resultados_he = []
# Definir una lista vacía para los resultados con Intensidad de Diseño
resultados_tercera_tabla = []
# Definir una lista vacía para los resultados con Gasto de Diseño
resultados_gasto_MetodoRacional = []
# Definir una lista vacía para los resultados con el Método de HUT
resultados_hut = []

# Definir el valor de 'n' para el tiempo base (Método de HUT)
n = 2

# Definir el valor de 'k' para el coeficiente de retardado (esto debe ser determinado según las características del terreno)
k = 0.1  # Valor de 'k' en horas^-1, ajusta según el tipo de suelo

# Iterar sobre los datos cargados desde el Excel
for _, fila in datos_lluvia.iterrows():
    periodo_retorno = fila['Periodo de retorno']  # Asegúrate de que el encabezado esté correcto en el archivo Excel
    precipitacion = fila['Precipitacion']  # Asegúrate de que el encabezado esté correcto en el archivo Excel
    
    # Calcular el coeficiente K usando la fórmula de CN
    coef_k = (precipitacion * (1 - e)) / (24 ** (1 - e))

    # Calcular Hpd usando la fórmula proporcionada
    hpd = (coef_k * Tc ** (1 - e)) / (1 - e)

    # Calcular He utilizando el método de Horton
    he = calcular_he_horton(precipitacion, k, Tc)

    # Calcular C
    c = ((numero_curva - 85 )) / 100

    # Calcular la intensidad de diseño usando la fórmula
    intensidad_diseno = coef_k / ((1 - e) * Tc ** e)

    # Calcular el Gasto de Diseño (Método Racional)
    gasto_diseno_MetodoRacional = c * area_cuenca * intensidad_diseno / 3600  # Convertir a m³/s

    # Calcular el Tiempo Pico
    tiempo_pico = (Tc / 2) + (0.6 * Tc)

    # Calcular el Tiempo Base
    tiempo_base = n * tiempo_pico

    # Calcular el Gasto de Diseño usando la fórmula del método de HUT
    gasto_diseno_hut = calcular_gasto_hut(he, area_cuenca_hut, tiempo_base)

    # Agregar los resultados a la tabla original
    resultados.append({
        'Periodo de retorno (años)': periodo_retorno,
        'Precipitacion (mm)': precipitacion,
        'Coeficiente K': coef_k,
        'Hpd (mm)': hpd
    })

    # Agregar los resultados para la nueva tabla con Hpd, Número de Curva y He
    resultados_he.append({
        'Periodo de retorno (años)': periodo_retorno,
        'Hpd (mm)': hpd,
        'Numero de Curva': numero_curva,
        'He (mm)': he
    })

    # Agregar los resultados para la tercera tabla con Periodo de Retorno, Precipitacion, Pendiente, Longitud, Tc e Intensidad de diseño
    resultados_tercera_tabla.append({
        'Periodo de retorno (años)': periodo_retorno,
        'Precipitacion (mm)': precipitacion,
        'Pendiente Cauce (m/m)': 0.030,
        'Longitud del Cauce (m)': 8050,
        'Tiempo de Concentracion (h)': Tc,
        'Intensidad de diseño (mm/h)': intensidad_diseno
    })

    # Agregar los resultados a la tabla con Gasto de Diseño Método Racional
    resultados_gasto_MetodoRacional.append({
        'Periodo de Retorno (años)': periodo_retorno,
        'Precipitacion (mm)': precipitacion,
        'Intensidad de diseño (mm/h)': intensidad_diseno,
        'C (He / Hpd)': c,
        'Área de la Cuenca (m²)': area_cuenca,
        'Gasto de Diseño (m³/s)': gasto_diseno_MetodoRacional
    })

    # Agregar los resultados al Método de HUT
    resultados_hut.append({
        'Periodo de retorno (años)': periodo_retorno,
        'Lluvia en exceso (mm)': he,
        'Área (km²)': area_cuenca_hut,  # Convertir a km²
        'Tiempo Pico (h)': tiempo_pico,
        'Factor de corrección (n)': n,
        'Tiempo Base (h)': tiempo_base,
        'Gasto (m³/s)': gasto_diseno_hut
    })

# Convertir los resultados a DataFrames
df_resultados = pd.DataFrame(resultados)
df_resultados_he = pd.DataFrame(resultados_he)
df_resultados_tercera_tabla = pd.DataFrame(resultados_tercera_tabla)
df_resultados_gasto = pd.DataFrame(resultados_gasto_MetodoRacional)
df_resultados_hut = pd.DataFrame(resultados_hut)

# Mostrar las tablas
print("\nTabla de resultados con Precipitacion, Coeficiente K y Hpd:")
print(df_resultados)

print("\nTabla de resultados con Hpd, Numero de Curva y He:")
print(df_resultados_he)

print("\nTabla de resultados con Intensidad de diseño:")
print(df_resultados_tercera_tabla)

print("\nTabla de resultados con Gasto de Diseño Metodo Racional:")
print(df_resultados_gasto)

print("\nTabla de resultados con Método de HUT:")
print(df_resultados_hut)

# Guardar todas las tablas en un archivo Excel
with pd.ExcelWriter("Analisis_LluviaEscurrimiento.xlsx", engine="openpyxl") as writer:
    df_resultados.to_excel(writer, sheet_name="Tabla de lluvia", index=False)
    df_resultados_he.to_excel(writer, sheet_name="Tabla de Hpd y He", index=False)
    df_resultados_tercera_tabla.to_excel(writer, sheet_name="Tabla de Intensidad de diseño", index=False)
    df_resultados_gasto.to_excel(writer, sheet_name="Tabla de Gasto de Diseño Metodo Racional", index=False)
    df_resultados_hut.to_excel(writer, sheet_name="Tabla de Método de HUT", index=False)
