import numpy as np

import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
alt.renderers.set_embed_options(actions=False)

import re
import json
import pandas as pd

import re
import json
import pandas as pd

#!pip install tabulate

#----------------------------------------------estrai_tabella_da_html 

def estrai_tabella_da_html(percorso_file_html):
    """
    Legge un file HTML di Plotly di serie storiche, estrae la serie di dati e 
    restituisce un DataFrame Pandas strutturato a Crosstab con TOTALI.
    Affina l'estetica rimuovendo i '.0' e i 'NaN'.
    Adattata per gestire dinamicamente qualsiasi Categoria (CPI, Età, Genere, ecc.).
    """
    with open(percorso_file_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 1. Troviamo la matrice di dati
    pattern = r'Plotly\.newPlot\(\s*"[^"]+",\s*(\[.*?\])\s*,\s*\{"template"'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        raise ValueError("Non sono riuscito a trovare la matrice dati nell'HTML.")

    json_data = match.group(1)
    traces = json.loads(json_data)

    # 2. Spacchettiamo i dati usando nomenclature universali
    records = []
    for trace in traces:
        # Usiamo 'nome_categoria' al posto di 'nome_cpi'
        nome_categoria = trace.get('name', 'Sconosciuto')
        anni = trace.get('x', [])
        valori = trace.get('y', [])
        
        for anno, valore in zip(anni, valori):
            records.append({
                'Anno': anno,
                'Categoria': nome_categoria, # Nome colonna generico e flessibile
                'COB': valore
            })

    df_grezzo = pd.DataFrame(records)

    # 3. Forgiamo la Tabella Pivot (Gestendo il caso in cui il dataframe sia vuoto)
    if not df_grezzo.empty:
        df_pivot = pd.pivot_table(
            df_grezzo, 
            index='Anno', 
            columns='Categoria', # Puntiamo alla nuova colonna universale
            values='COB', 
            aggfunc='sum',     
            margins=True,      
            margins_name='TOTALE' 
        ).reset_index()
        
        # Pulizia estetica (rimuove il nome tecnico dell'asse colonne)
        df_pivot.columns.name = None 
    else:
        # Fallback di sicurezza in caso di grafico vuoto
        df_pivot = pd.DataFrame(columns=['Anno', 'Categoria', 'COB'])
    
    # --- 4. LA LUCIDATURA ESTETICA (Rimozione .0 e NaN) ---
    def pulisci_celle(val):
        if pd.isna(val):                  # Se la cella è vuota (NaN)
            return ''                     # Sostituisci con stringa vuota
        if isinstance(val, (int, float)): # Se è un numero (es. 234.0)
            return str(int(val))          # Rimuovi il decimale e rendilo testo ('234')
        return str(val)                   # Lascia intatte le stringhe ('TOTALE')

    # Passiamo il panno lucidante su tutte le colonne
    for col in df_pivot.columns:
        df_pivot[col] = df_pivot[col].apply(pulisci_celle)

    return df_pivot

# --- ESEMPIO DI UTILIZZO ---
# Salva il tuo codice html in un file in percorso_file_html e lancia lo script:

#percorso_file_html=  "C:\\Users\\lorid\\quarto_report_somministrazione_OML34-#2025\\esportazioni_quarto\\grafico_10_COB_CPI_top25Qualif_1525.html"
#df_risultato = estrai_tabella_da_html(percorso_file_html)
#print(df_risultato)

#-----------------------------------------------------fine funzione----------


import re
import json
import pandas as pd

def estrai_tabella_da_html_con_titolo(percorso_file_html, trasponi=False):
    """
    Legge un file HTML di Plotly di serie storiche, estrae la serie di dati e il TITOLO reale,
    restituendo un DataFrame Pandas (Crosstab) pulito (senza .0 o NaN) e una stringa.
    Supporta la trasposizione assi tramite il parametro 'trasponi'.
    """
    with open(percorso_file_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 1. Regex Robusta: Catturiamo tutto ciò che sta dentro Plotly.newPlot( ... )
    pattern = r'Plotly\.newPlot\(\s*"[^"]+",\s*(\[.*?\])\s*,\s*(\{.*?\})\s*,\s*\{"responsive"'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        raise ValueError("Impossibile trovare il blocco dati Plotly nell'HTML.")

    json_data_str = match.group(1)
    json_layout_str = match.group(2)

    # 2. Convertiamo da Testo a Dizionari/Liste Python
    traces = json.loads(json_data_str)
    layout = json.loads(json_layout_str)

    # 3. ESTRAZIONE DEL TITOLO REALE
    titolo_estratto = "Tabella Dati" # Default
    if 'title' in layout and 'text' in layout['title']:
        titolo_estratto = layout['title']['text']
    elif 'text' in layout.get('title', {}):
        titolo_estratto = layout['title']['text']

    # 4. ESTRAZIONE DATI
    records = []
    for trace in traces:
        nome_categoria = trace.get('name', 'Sconosciuto')
        anni = trace.get('x', [])
        valori = trace.get('y', [])
        
        for anno, valore in zip(anni, valori):
            records.append({
                'Anno': anno,
                'Categoria': nome_categoria,
                'COB': valore
            })

    df_grezzo = pd.DataFrame(records)

    # 5. Creazione Tabella Pivot Dinamica (con opzione TRASPONI)
    if not df_grezzo.empty:
        # --- LA MAGIA DELLA TRASPOSIZIONE ---
        # Se trasponi=True, le categorie diventano le righe e gli anni le colonne.
        riga_index = 'Categoria' if trasponi else 'Anno'
        colonna_index = 'Anno' if trasponi else 'Categoria'

        df_pivot = pd.pivot_table(
            df_grezzo, 
            index=riga_index, 
            columns=colonna_index, 
            values='COB', 
            aggfunc='sum',     
            margins=True,      
            margins_name='TOTALE' 
        ).reset_index()
        
        # Pulizia intestazioni
        df_pivot.columns.name = None 
    else:
        # Fallback se non ci sono dati
        colonne_vuote = ['Categoria', 'Anno', 'COB'] if trasponi else ['Anno', 'Categoria', 'COB']
        df_pivot = pd.DataFrame(columns=colonne_vuote)

    # --- 6. LA LUCIDATURA ESTETICA (Rimozione .0 e NaN) ---
    def pulisci_celle(val):
        if pd.isna(val):                  # Se la cella è vuota (NaN)
            return ''                     # Sostituisci con stringa vuota
        if isinstance(val, (int, float)): # Se è un numero (es. 234.0)
            return str(int(val))          # Rimuovi il decimale e rendilo testo ('234')
        return str(val)                   # Lascia intatte le stringhe ('TOTALE')

    # Passiamo il panno lucidante su tutte le colonne della tabella
    for col in df_pivot.columns:
        df_pivot[col] = df_pivot[col].apply(pulisci_celle)

    # Restituiamo ENTRAMBI gli elementi finali
    return df_pivot, titolo_estratto

#--------------esempio

#percorso_file_html="esportazioni_quarto\\grafico_7_COB_NAZ_tutti_contratti_1525_tutte_le_naz.html"
#df_tabella, titolo_dinamico = estrai_tabella_da_html_con_titolo(percorso_file_html, trasponi=False)
#print(titolo_dinamico)
#print(df_tabella)

#------------------------------------fine funzione------------------


import re
import json
import pandas as pd

def estrai_tabella_barre_da_html_con_titolo(percorso_file_html):
    """
    Legge un file HTML di Plotly (grafico a barre), estrae le categorie, 
    i valori e (se presenti) le percentuali, aggiunge una riga di TOTALE,
    e restituisce un DataFrame Pandas pulito.
    """
    with open(percorso_file_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 1. Regex per catturare il blocco dati Plotly
    pattern = r'Plotly\.newPlot\(\s*"[^"]+",\s*(\[.*?\])\s*,\s*(\{.*?\})\s*,\s*\{"responsive"'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        raise ValueError("Impossibile trovare il blocco dati Plotly nell'HTML.")

    json_data_str = match.group(1)
    json_layout_str = match.group(2)

    traces = json.loads(json_data_str)
    layout = json.loads(json_layout_str)

    # 2. Estrazione Titolo (con fallback se non presente)
    titolo_estratto = "Tabella Distribuzione"
    if 'title' in layout and 'text' in layout['title']:
        titolo_estratto = layout['title']['text']
    elif 'text' in layout.get('title', {}):
        titolo_estratto = layout['title']['text']

    # 3. Estrazione Dati
    records = []
    
    # Nei grafici a barre di solito c'è una sola traccia principale
    for trace in traces:
        if trace.get('type') == 'bar':
            
            # Capiamo l'orientamento: se è orizzontale ('h'), le categorie sono la Y.
            if trace.get('orientation') == 'h':
                categorie = trace.get('y', [])
                valori = trace.get('x', [])
            else:
                categorie = trace.get('x', [])
                valori = trace.get('y', [])
                
            testi = trace.get('text', []) # Contiene es: "553006 (53.1%)"
            usa_testi = len(testi) == len(valori)

            for i in range(len(valori)):
                record = {
                    'Categoria': categorie[i],
                    'COB': valori[i]
                }
                
                # Bonus: Estraiamo la percentuale pulita dalle parentesi
                if usa_testi:
                    match_perc = re.search(r'\((.*?%)\)', str(testi[i]))
                    if match_perc:
                        record['Incidenza'] = match_perc.group(1)
                        
                records.append(record)

    df_risultato = pd.DataFrame(records)

    # --- 4. AGGIUNTA DELLA RIGA TOTALE ---
    if not df_risultato.empty:
        totale_cob = df_risultato['COB'].sum()
        
        riga_totale = {
            'Categoria': 'TOTALE',
            'COB': totale_cob
        }
        
        # Se c'è la colonna percentuale, impostiamo il totale al 100%
        if 'Incidenza' in df_risultato.columns:
            riga_totale['Incidenza'] = '100.0%'
            
        # Aggiungiamo la nuova riga alla fine del DataFrame
        df_risultato.loc[len(df_risultato)] = riga_totale

    # 5. LA LUCIDATURA ESTETICA (Rimozione .0 e NaN)
    def pulisci_celle(val):
        if pd.isna(val):                  
            return ''                     
        if isinstance(val, (int, float)): 
            return str(int(val))          
        return str(val)                   

    if not df_risultato.empty:
        for col in df_risultato.columns:
            df_risultato[col] = df_risultato[col].apply(pulisci_celle)

    return df_risultato, titolo_estratto

# -------------- Esempio di utilizzo --------------
# percorso_file = "output_esportazioni_quarto/grafico_barre.html"
# df_tabella, titolo = estrai_tabella_barre_da_html_con_titolo(percorso_file)
# print(titolo)
# print(df_tabella.to_markdown(index=False))

#------------------------------------fine funzione------------------

def applica_correzione_titolo(titolo_estratto):
    """
    Riceve il titolo estratto dal grafico HTML e verifica se esiste
    una corrispondenza ESATTA nel dizionario di sostituzione.
    Se la trova, restituisce il titolo nuovo. Se non la trova,
    restituisce il titolo intatto.
    """
    
    # "Console di Regia" dei titoli
    mappa_sostituzioni = {
        # "Titolo Originale Esatto" : "Il tuo Nuovo Titolo Definitivo"
        "Top 25 Tipologie Contrattuali": "Distribuzione delle Prime 25 Tipologie Contrattuali (2015-2025 anni)",
        "Top 25 Qualifiche (Tutti i contratti)": "Distribuzione delle Prime 25 Qualifiche Professionali più richieste (2015-2025)",
        "Trend Genere: Tutti i contratti": "Andamento Storico Generale suddiviso per Genere",
        # Aggiungi
    }
    
    # Il metodo .get() fa la ricerca ESATTA. 
    # Se 'titolo_estratto' è tra le chiavi, restituisce il valore nuovo.
    # Altrimenti, come fallback (secondo parametro), restituisce 'titolo_estratto' intatto.
    return mappa_sostituzioni.get(titolo_estratto, titolo_estratto)

# -------------- Esempio di utilizzo --------------
# 2. --- IL TUO FILTRO DI SOSTITUZIONE ESATTA ---
#    titolo_finale = applica_correzione_titolo(titolo_dinamico)
#------------------------------------fine funzione------------------

