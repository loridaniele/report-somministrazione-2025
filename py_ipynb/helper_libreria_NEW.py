

import pandas as pd
import numpy as np
from typing import List

# Funzioni di pivoting personalizzate
#===============================
#pivot_somma
#pivot_somma_totale
#pivot_percentuali_100
#===============================

def pivot_somma(df: pd.DataFrame,
                colonna_indice: str,
                colonne_colonne: List[str],
                colonna_valore: str) -> pd.DataFrame:
    """
    Produce una pivot table con:
    - indice = colonna_indice
    - colonne = vettore di colonne specificate
    - valori = somma della colonna_valore

    Parametri:
        df               : DataFrame di partenza
        colonna_indice   : colonna da usare come indice
        colonne_colonne  : lista di colonne che formano le colonne della pivot
        colonna_valore   : colonna numerica da sommare nelle celle

    Ritorna:
        pivot_table : DataFrame pivotato
    """

    pivot = pd.pivot_table(
        df,
        index=colonna_indice,
        columns=colonne_colonne,
        values=colonna_valore,
        aggfunc="sum",
        fill_value=0
    )

    return pivot

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pivot_somma_totale(df: pd.DataFrame,
                       colonna_indice: str,
                       colonne_colonne: List[str],
                       colonna_valore: str,
                       sort_rows: bool = False) -> pd.DataFrame:
    """
    Produce una pivot table con:
    - indice = colonna_indice
    - colonne = vettore di colonne-colonne
    - valori = somma della colonna_valore
    - colonna 'TOT' con la somma per riga
    - ordinamento opzionale delle righe (decrescente per TOT)

    Parametri
    ---------
    df : DataFrame
        Dataset di partenza

    colonna_indice : str
        Nome colonna da usare come indice

    colonne_colonne : lista di str
        Nomi delle colonne che formano l'asse colonne della pivot

    colonna_valore : str
        Nome colonna con i valori da sommare

    sort_rows : bool
        True  -> ordina le righe in modo decrescente sulla colonna TOT
        False -> mantiene l'ordine originale

    Ritorna
    -------
    DataFrame pivotato con colonna TOT
    """

    # Pivot principale
    pivot = pd.pivot_table(
        df,
        index=colonna_indice,
        columns=colonne_colonne,
        values=colonna_valore,
        aggfunc="sum",
        fill_value=0
    )

    # Aggiunta colonna totale
    pivot["TOT"] = pivot.sum(axis=1)

    # Ordinamento righe su TOT (decrescente)
    if sort_rows:
        pivot = pivot.sort_values("TOT", ascending=False)

    return pivot


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#funzione - trasformazione percentuale
def pivot_percentuali_100(
    pivot: pd.DataFrame,
    mode: str = "riga",
    decimali: int = 2,
    base_cento: bool = True
    ) -> pd.DataFrame:
    """
    Trasforma un pivot numerico in un pivot di percentuali, con opzione
    su tipo di normalizzazione, numero di decimali e base 100.

    Parametri
    ---------
    pivot : DataFrame
        Matrice pivot (numerica), risultato di pivot_somma.

    mode : {"riga", "colonna", "totale"}
        - "riga"     → ogni riga somma 1 (o 100 se base_cento=True)
        - "colonna"  → ogni colonna somma 1 (o 100)
        - "totale"   → l'intera matrice somma 1 (o 100)

    decimali : int
        Numero di decimali da mantenere nel risultato finale.

    base_cento : bool
        - True  → percentuali *in base 100* (0–100)
        - False → frazioni (0–1)

    Ritorna
    -------
    pivot_pct : DataFrame
        Pivot con percentuali formattate.
    """

    if mode not in ["riga", "colonna", "totale"]:
        raise ValueError("mode deve essere 'riga', 'colonna', 'totale'")

    pivot_num = pivot.astype(float)

    # --- NORMALIZZAZIONE ---
    if mode == "riga":
        tot = pivot_num.sum(axis=1)
        pivot_pct = pivot_num.div(tot, axis=0)

    elif mode == "colonna":
        tot = pivot_num.sum(axis=0)
        pivot_pct = pivot_num.div(tot, axis=1)

    elif mode == "totale":
        tot = pivot_num.values.sum()
        pivot_pct = pivot_num / tot

    # --- BASE 100 ---
    if base_cento:
        pivot_pct = pivot_pct * 100

    # --- DECIMALI ---
    pivot_pct = pivot_pct.round(decimali)

    # eventuali NaN a zero
    pivot_pct = pivot_pct.fillna(0)

    return pivot_pct

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def pivot_diff_percentuali_mean(
    pivot_riga_pct: pd.DataFrame,
    decimali: int = 2,
    base_cento: bool = True
    ) -> pd.DataFrame:
    """
    Calcola la differenza percentuale tra ogni riga del pivot (percentuali di riga)
    e la distribuzione percentuale totale (media delle righe), con gestione decimali.

    Parametri
    ---------
    pivot_riga_pct : DataFrame
        Pivot contenente percentuali di riga (0–1 oppure 0–100).

    decimali : int
        Numero di decimali da mantenere nel risultato.

    base_cento : bool
        - True  → l’output è in base 100 (0–100)
        - False → output come frazione (0–1)

    Ritorna
    -------
    pivot_diff : DataFrame
        Pivot con differenze percentuali riga - percentuale totale.
    """

    # 1. Copia di sicurezza
    pivot_num = pivot_riga_pct.astype(float)

    # 2. Distribuzione totale = media delle percentuali riga
    dist_tot = pivot_num.mean(axis=0)   # Series

    # 3. Differenze tramite broadcasting
    pivot_diff = pivot_num - dist_tot

    # 4. Conversione in base cento se richiesto
    if base_cento:
        pivot_diff = pivot_diff * 100

    # 5. Arrotondamento
    pivot_diff = pivot_diff.round(decimali)

    return pivot_diff
