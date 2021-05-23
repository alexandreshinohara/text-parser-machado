import pandas as pd
import numpy as np

#open files and populate dataframes
df_pt = pd.read_csv('Dom-Casmurro_ptb.txt', delimiter="\t")
df_gledson = pd.read_csv('Dom Casmurro_Gledson_eng.txt', delimiter="\t")
df_scott = pd.read_csv('Dom Casmurro_Scott-Buccleuch_eng.txt', delimiter="\t")
df_caldwell = pd.read_csv('Dom Casmurro_Caldwell_eng.txt', delimiter="\t")
df_alg_roman = pd.read_csv('alg_roman.csv', delimiter=';',dtype={'num':'int'})

#VLOOKUP the rows with roman numbers and add column chapter with chapter number
df_pt = df_pt.merge(df_alg_roman, how='left', left_on='Dom Casmurro', right_on='alg_r').drop(columns='alg_r').rename({'num':'chap_pt'}, axis=1)
df_gledson = df_gledson.merge(df_alg_roman, how='left', left_on='DOM CASMURRO', right_on='alg_r').drop(columns='alg_r').rename({'num':'chap_gled'}, axis=1)


#Fill in NaN values on the chapter column based on current chapter number

#for df_pt:
for c in range(len(df_pt.index)):
    if np.isnan(df_pt.at[c, 'chap_pt']):
        df_pt.at[c, 'chap_pt'] = df_pt.at[(c - 1), 'chap_pt']

c = 0
#df_gledson:
for c in range(len(df_gledson.index)):
    if np.isnan(df_gledson.at[c, 'chap_gled']):
        df_gledson.at[c, 'chap_gled'] = df_gledson.at[(c - 1), 'chap_gled']

#merge df_gledson to df_pt dataframe
df_pt['en_gledson'], df_pt['chap_gled'] = df_gledson['DOM CASMURRO'], df_gledson['chap_gled']


#---- SCOTT txt ---

#adding a new column filled with None
df_scott['chap_scott'] = None

#flexing a new loop style. Check if string is a number in the cell. If so, fill in chap_scott column
for r, c in df_scott.iterrows():
    if df_scott.at[r,'DOM CASMURRO'].isnumeric():
        df_scott.at[r, 'chap_scott'] = df_scott.at[r,'DOM CASMURRO']

#now replace None with current chapter
for c in range(df_scott.shape[0]):
    if df_scott.at[c, 'chap_scott'] == None:
        df_scott.at[c, 'chap_scott'] = df_scott.at[(c - 1), 'chap_scott']

#merge df_scott to df_pt
df_pt['en_scott'], df_pt['chap_scott'] = df_scott['DOM CASMURRO'], df_scott['chap_scott']


#--CALDWELL txt------------
#this one is tougher. I need to split the row with chapter number and title, replace current row with chapter number and
#add a new row below with the title, to conform with the format of the other files

#adding a new column 
df_caldwell['chap_cald'] = None
#chapter counter
x = 0

#check character if ∙ in row, split it and populate list of lists spl
spl = []
total_l = len(df_caldwell.index)
for r in range(total_l):
    if '∙' in df_caldwell.at[r, 'Dom Casmurro']:
        x = x + 1
        #split row and populate list of lists
        spl_temp = df_caldwell.at[r, 'Dom Casmurro'].split('∙')
        #add current row to list
        spl_temp.append(r)
        spl.append(spl_temp)
    df_caldwell.at[r, 'chap_cald'] = x


#spl list of lists consists of [[chapter number string, chapter title string, row number in the caldwell txt] ]

for r in range(len(spl)):
    #replace full string with chapter number in spl
    df_caldwell.at[spl[r][2], 'Dom Casmurro'] = spl[r][0]
    #add new row in the text between current row (chapter number) and next row and fill in the chapter title
    df_caldwell.at[spl[r][2] + 0.5, 'Dom Casmurro'] = spl[r][1]
    df_caldwell.at[spl[r][2] + 0.5, 'chap_cald'] = spl[r][0]
#sort and refresh index
df_caldwell = df_caldwell.sort_index().reset_index(drop=True)


df_pt['en_caldwell'], df_pt['chap_caldwell'] = df_caldwell['Dom Casmurro'], df_caldwell['chap_cald']



#convert chapter columns to int
df_pt['chap_pt'] = df_pt['chap_pt'].astype('Int64')
df_pt['chap_gled'] = df_pt['chap_gled'].astype('Int64')


#export to csv
df_pt.to_csv('domcasmurroalltext.csv',index=False)




