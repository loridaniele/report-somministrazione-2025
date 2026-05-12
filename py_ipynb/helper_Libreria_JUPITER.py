import pandas as pd
import numpy as np



#esempio freq(D5,'CONTRATTO', 'Contratto')
def freq(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True)
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"%":per100})
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df
##################################################################################################
def freq_normalize(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True) 
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"norm":percent,"%":per100})
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df
##################################################################################################
# tabella frequenze con index ascendente
def freq_a(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True) 
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"%":per100})
    cx_df = cx_df.sort_index(ascending=True)  #ascendente - nota prima di aggiungere in fondo l'index 'Total' che non verrà ordinato
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df
##################################################################################################
# tabella frequenze con index discendente
def freq_d(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True) 
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"%":per100})
    cx_df = cx_df.sort_index(ascending=False)  #ascendente - nota prima di aggiungere in fondo l'index 'Total' che non verrà ordinato
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df

##################################################################################################
##################################################################################################
# tabella frequenze con index ascendente
def freq_a_normalize(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True) 
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"norm":percent,"%":per100})
    cx_df = cx_df.sort_index(ascending=True)  #ascendente - nota prima di aggiungere in fondo l'index 'Total' che non verrà ordinato
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df
##################################################################################################
# tabella frequenze con index discendente
def freq_d_normalize(df,col,nome_col):
    cx = df[col]
    counts = cx.value_counts()
    percent = cx.value_counts(normalize=True) 
    per100 = percent.mul(100).round(1)
    cx_df = pd.DataFrame({"freq":counts,"norm":percent,"%":per100})
    cx_df = cx_df.sort_index(ascending=False)  #ascendente - nota prima di aggiungere in fondo l'index 'Total' che non verrà ordinato
    cx_df = pd.concat([cx_df, pd.DataFrame([cx_df.sum().rename('Total')])])
    cx_df.columns.name= nome_col
    #-----------tolgo lo zero da freq !
    cx_df['freq'] = cx_df['freq'].astype(str).replace('\.0', '', regex=True)
    cx_df['freq'] = cx_df['freq'].astype(int)
    return cx_df

##################################################################################################
#tabelle di frequenza di tutte le colonne contenute in un vettore
def freqAll(df,v):
    
    for i in v:
        print("           "); print("           ");print("           ");
        print(fr'{i}')
        print('-----------------------------------------------------------')
        aa=freq(df,fr'{i}',fr'{i}').reset_index()
        print(aa)
        
    
    return 


def pt_freq(df,index1,colonne,livello):
    pt = df.pivot_table(index=index1, columns=colonne,values=livello,
                        aggfunc='count', fill_value='', margins =True)
    #rinomino la colonna e la riga 'All' (i totali) con 'Total'
    pt = pt.rename(columns={'All': 'Total'})
    pt = pt.rename(index={'All': 'Total'})
    return pt
#--------------------------------------------------------------------------
def pt_freq_order(df,index1,colonne,livello,order_cols):
    pt = df.pivot_table(index=index1, columns=colonne,values=livello,
                        aggfunc='count', fill_value='', margins =True)
    #rinomino la colonna e la riga 'All' (i totali) con 'Total'
    pt = pt.rename(columns={'All': 'Total'})
    pt = pt.rename(index={'All': 'Total'})
    #riordino secondo il vettore order_cols
    pt = pt.reindex(order_cols, axis=1)
    
    return pt
#--------------------------------------------------------------------------
# pitvot table - somma livello 
def pt_sum(df,index1,colonne,livello):
    pt = df.pivot_table(index=index1, columns=colonne,values=livello,
                        aggfunc='sum',fill_value=0, # fill_value='', 
                        margins =True)
    #rinomino la colonna e la riga 'All' (i totali) con 'Total'
    pt = pt.rename(columns={'All': 'Total'})
    pt = pt.rename(index={'All': 'Total'})
    return pt
#--------------------------------------------------------------------------
# pitvot table - somma livello - % di riga 
def pt_sum_percent(df,index1,colonne,livello):
    #print(df.columns)
    pt = (
            df.pivot_table(index=index1, columns=colonne,values=livello,
            aggfunc='sum', margins =True,
            margins_name='Total', fill_value=0 #, fill_value=''
            )
    .pipe(lambda d: d.div(d[livello[0]]['Total'], axis='index'))
    .applymap('{:.0%}'.format)
    )

    return pt
#--------------------------------------------------------------------------
def pt_sum_order(df,index1,colonne,livello,order_cols):
    pt = df.pivot_table(index=index1, columns=colonne,values=livello,
                        aggfunc='sum', fill_value=0, #fill_value='', 
                        margins =True)
    #rinomino la colonna e la riga 'All' (i totali) con 'Total'
    pt = pt.rename(columns={'All': 'Total'})
    pt = pt.rename(index={'All': 'Total'})
    #riordino secondo il vettore order_cols
    pt = pt.reindex(order_cols, axis=1)
    
    return pt