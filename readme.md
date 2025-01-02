# Análisis de Lluvia y Escurrimiento

Este script realiza cálculos de escurrimientos y diseño hidráulico usando los métodos de Horton, Método Racional y Método de HUT. Los resultados se exportan a un archivo Excel.

## Requisitos
- Python 3.x
- pandas
- numpy
- openpyxl

## Instalación
Ejecuta el siguiente comando para instalar las dependencias:



## Uso
Coloca un archivo `lluvia.xlsx` con las columnas:
- Periodo de retorno
- Precipitación (Hp)

Ejecuta el script:


## Salida
El script genera un archivo `Analisis_LluviaEscurrimiento.xlsx` con las siguientes hojas:
1. Tabla de lluvia
2. Tabla de Hpd y He
3. Intensidad de diseño
4. Gasto de diseño (Método Racional)
5. Gasto de diseño (Método de HUT)
