"""
Función reutilizable para descargar datos de la API de Eurostat.
Proyecto: ¿Cuánto vale tu trabajo?
Autor: Andoni Olaso
"""

import requests
import pandas as pd


def descargar_eurostat(indicador, desde='1999-S1'):
    """
    Descarga un indicador de la API de Eurostat y lo devuelve como DataFrame.
    
    Parámetros:
    - indicador: código del dataset en Eurostat (ej: 'ilc_iw01')
    - desde: periodo inicial (por defecto '1999-S1')
    
    Devuelve: DataFrame con columnas por cada dimensión + columna 'valor'
    """
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{indicador}"
    params = {'sinceTimePeriod': desde, 'lang': 'en'}
    
    print(f"Descargando {indicador}...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"  ERROR: código {response.status_code}")
        return None
    
    data = response.json()
    dimensions = data['id']
    
    dim_categories = {}
    dim_sizes = []
    for dim_name in dimensions:
        dim = data['dimension'][dim_name]
        cat_index = dim['category']['index']
        ordered_cats = sorted(cat_index.keys(), key=lambda x: cat_index[x])
        dim_categories[dim_name] = ordered_cats
        dim_sizes.append(len(ordered_cats))
    
    multipliers = []
    for i in range(len(dim_sizes)):
        mult = 1
        for j in range(i + 1, len(dim_sizes)):
            mult *= dim_sizes[j]
        multipliers.append(mult)
    
    values = data['value']
    rows = []
    for str_idx, val in values.items():
        idx = int(str_idx)
        row = {}
        for i, dim_name in enumerate(dimensions):
            cat_position = (idx // multipliers[i]) % dim_sizes[i]
            row[dim_name] = dim_categories[dim_name][cat_position]
        row['valor'] = val
        rows.append(row)
    
    df = pd.DataFrame(rows)
    print(f"  OK: {len(df)} filas x {len(df.columns)} columnas")
    return df
