import numpy as np
from datetime import datetime, timedelta
import pandas as pd

data = pd.read_csv('tarefasDetalhe.csv')

"""**Converte as data para o formato datetime usado na biblioteca pandas**"""

data['Start'] = pd.to_datetime(data['Start'], format='%Y-%m-%d %H:%M:%S')
data['Finish'] = pd.to_datetime(data['Finish'], format='%Y-%m-%d %H:%M:%S')

"""**Funcao usada para informar qual sprint uma data pertence**
  + A funcao possui três parametros:
    + value: data que deseja obter a sprint 
    + init_date: data na qual inicia a primeira sprint
    + sprint_size: numero de dias ate a proxima sprint
"""

def sprint_date(value,sprint=1,init_date='2021/06/07', sprint_size=14):
    init_date = datetime.strptime(init_date, '%Y/%m/%d')
    value = datetime.strptime(value, '%Y-%m-%d') if type(value) != pd.Timestamp and pd.notnull(value) else value

    while init_date <= value:
        init_date = init_date + timedelta(sprint_size)
        sprint = sprint+1

    return sprint-1

data['Sprint_calc'] = data['Finish'].apply(sprint_date)

"""**Funcao usada retornar somente o numro de dias da coluna 'Duration'**
  + '10 days' ------> 10
  + '5 days'  ------> 5
"""

def correct_duration(x):
  x = str(x)
  size_x = len(x)
  if size_x >6 and size_x<8:
    return x[:2]
  elif size_x >5 and size_x < 7:
    return x[0]

data['Duration'] = data['Duration'].apply(correct_duration)

""" + *Se a Data final < data de hoje, a coluna target terá o valor 1*
 + *Se a Data final >= data de hoje, a coluna target terá o valor representado pela seguinte formula:*
  + ( [data de hoje] - [data de inicio] ) / [numero de dias da semana]
"""

data['target'] = -99

for linha in range(len(data)):
    dias_da_semana = 7
    data_hoje = datetime.now()
    if data.loc[linha, 'Finish']<data_hoje:
        data.loc[linha, 'target'] = 1
    else:
        data.loc[linha, 'target'] = (data_hoje - data.loc[linha, 'Start'])/dias_da_semana

"""*A coluna target_semanal e a coluna Duration dividido por 5*"""

data['target_semanal'] = data['Duration'].apply(lambda x: int(x)/5 if x != None else x)

"""**Filtro das tarefas**"""

tarefas_concluidas = data[(data['target']==1)&(data['% complete']==1)]

tarefas_atrasadas = data[(data['target']==1)&(data['% complete']!=1)]

tarefas_adiantadas = data[(data['target']!=1)&(data['% complete']!=0)]

"""*Balanceamento das Tarefas*"""

tarefas_balaceadas = int(tarefas_adiantadas_percentual + tarefas_atrasadas_percentual)

numero_tarefas_concluidas + tarefas_balaceadas

"""**New Table**"""

sprints = data['Sprint_calc'].value_counts().to_frame()
sprints.columns = ['count_task']

count_task_concluded = tarefas_concluidas.groupby(by='Sprint_calc').sum()['% complete'].to_frame()
count_task_concluded.columns = ['task_concluded']

count_task_late = tarefas_atrasadas.groupby(by='Sprint_calc').sum()['% complete'].to_frame()
count_task_late.columns = ['task_late']

count_task_advanced = tarefas_adiantadas.groupby(by='Sprint_calc').sum()['% complete'].to_frame()
count_task_advanced.columns = ['task_advanced']

table_summary = sprints.join(column_task_concluded)\
.join(count_task_late)\
.join(count_task_advanced)\
.sort_index()

table_summary.fillna(0, inplace=True)
table_summary.drop(0, inplace=True)
table_summary.index.name = 'sprint'

for i in table_summary.index:
  if table_summary.loc[i,'task_late'] != 0:
    table_summary.loc[i,'diference'] = table_summary.loc[i,'count_task'] - (table_summary.loc[i,'task_concluded'] + table_summary.loc[i,'task_advanced'] + (1 - table_summary.loc[i,'task_late']))
    #table_summary.loc[i,'yield'] = table_summary.loc[i,'task_concluded'] + table_summary.loc[i,'task_advanced'] + (1 - table_summary.loc[i,'task_late'])

  else:
    table_summary.loc[i,'diference'] = table_summary.loc[i,'count_task'] - (table_summary.loc[i,'task_concluded'] + table_summary.loc[i,'task_advanced'])
    #table_summary.loc[i,'yield'] = table_summary.loc[i,'task_concluded'] + table_summary.loc[i,'task_advanced']

sum_task_concluded = table_summary['task_concluded'].sum()
sum_task_advanced = table_summary['task_advanced'].sum()
sum_task_late = table_summary['task_late'].sum()

count_task_late = len(table_summary[table_summary['task_late']!=0])
dif_task_late = count_task_late - sum_task_late

Task_balance = int( sum_task_concluded + sum_task_advanced + dif_task_late )

print(f"Temos {Task_balance} tarefas concluídas")

table_summary['debtor'] = table_summary['diference'].cumsum()

table_summary

"""**Charts**"""

table_summary[['debtor','yield', 'count_task']].plot(kind='line')





'''def sprint_date(value,sprint=1,init_date='2021/01/04', sprint_size=14):
  init_date = datetime.strptime(init_date, '%Y/%m/%d')
  value = datetime.strptime(value, '%Y/%m/%d') if type(value) != pd.Timestamp and pd.notnull(value) else value
  while init_date <= value:
    init_date = init_date + timedelta(sprint_size)
    sprint = sprint+1
  
  return sprint-1
'''
