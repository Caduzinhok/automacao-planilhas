import pandas as pd
import os

def main(file_initial_path, file_final_path, name_file):
    ### Validações para evitar erros de formato.
    if('.' in name_file):
        name_file = str(name_file).replace(".", '')
        
    if('csv' in name_file):
        name_file = str(name_file).replace(".csv", '')
        
    print("Lendo dados do Arquivo CSV...")

    try:
        ### Ler arquivos como CSV
        base_inicial = pd.read_csv(file_initial_path, sep=";", encoding='utf-8')
        base_final =  pd.read_csv(file_final_path, sep=";", encoding='utf-8') 
        base_final['Status'] = ''
        base_inicial['Status'] = ''
    except:
        print("Não foi possível ler os arquivos do formato CSV, por favor verifique o formato ou o caminho...")
    print("Filtrando dados do arquivo CSV...")

    try:
        ### Verificando items que estavam na base 1 (Ativos e Suspensos)
        for index, item in base_inicial.iterrows():
            user_mail = str(base_inicial.iloc[index]['username']) ### Obter valor da base na coluna 1 = username
            curso = str(base_inicial.iloc[index]['course1']) ### Obter valor da base na coluna 1 = username

            base_filtrada = base_final[base_final['username'] == user_mail]
            base_filtrada = base_filtrada[base_filtrada['course1'] == curso]

            if(len(base_filtrada) >= 1 and (user_mail != "#N/D")): ### Se encontrou o usuário e o usuário não é nulo ou undefined
                base_inicial.at[index, 'Status'] = 'active'
            else:
                base_inicial.at[index, 'Status'] = 'suspended'
    except:
        print("Não foi possível cruzar as informações dos arquivos, verifique se os nomes das colunas estão como 'username' e 'course1'")


    print('Juntando bases e salvando no Downloads...')
    try:
        base_completa = base_inicial.merge(base_final, on=["username", 'course1'], how='outer')
    except:
        print("Não foi possível juntar ambas as bases, verifique os nomes das colunas ou quantidade de colunas.")
    ### Organizar colunas duplicadas
    base_completa = base_completa.drop(columns=['Status_y'])
    base_completa = base_completa.rename(columns={"Status_x": "Status"})
    
    base_completa.loc[base_completa['Status'].isnull(),'Status'] = 'new' # Aqueles que não foram encontrados, setar como new
    
    ## Salvar Arquivo na pasta de downloads
    try:
        base_completa.to_csv("downloads\\"+name_file+".csv", sep=";", encoding='utf-8', index=False)
    except:
        print("Não foi possível salvar base Planilhas de Ofertas no caminho")
    print("Dados salvos com sucesso na pasta!!!")
    
    return name_file+".csv"