import pandas as pd
from io import BytesIO

def main(file_initial_obj, file_final_obj, name_file):
    # Validações para o nome do arquivo
    name_file = name_file.split('.')[0].replace(".csv", '')

    print("Lendo dados do Arquivo CSV...")

    try:
        # Ler arquivos como CSV
        base_inicial = pd.read_csv(file_initial_obj, sep=";", encoding='utf-8-sig')
        base_final = pd.read_csv(file_final_obj, sep=";", encoding='utf-8-sig')
        base_inicial['Status'] = ''
        base_final['Status'] = ''
    except Exception as e:
        print(f"Erro ao ler os arquivos CSV: {e}")
        return None

    print("Filtrando dados do arquivo CSV...")

    try:
        # Merge para identificar correspondências entre base_inicial e base_final
        merged = pd.merge(base_inicial[['username', 'course1']], base_final[['username', 'course1']], 
                          on=['username', 'course1'], how='outer', indicator=True)
        
        # Definir status com base no resultado do merge
        merged['Status'] = merged['_merge'].map({'both': 'active', 'left_only': 'suspended', 'right_only':'active'})
        ## Substituir valores inválidos por 'suspended'
        merged.loc[merged['username'] == "#N/D", 'Status'] = 'suspended'
        merged = merged.drop(columns=['_merge'])
    except KeyError as e:
        print(f"Erro nas colunas: {e}")
        return None
    
    print("Juntando bases e salvando no Downloads...")
    
    try:
        # Juntar as bases com um novo merge
        base_completa = pd.merge(merged, base_final, on=["username", "course1"], how='outer', suffixes=('_inicial', '_final'))
        base_completa.drop(columns=['Status_final'], inplace=True)
        base_completa.rename(columns={"Status_inicial": "Status"}, inplace=True)
        base_completa['enrolstatus1'] = ''

        # Definir valores na coluna enrolstatus1
        base_completa.loc[base_completa['Status'] == 'suspended', 'enrolstatus1'] = '1'
        base_completa.loc[base_completa['Status'].isnull(), 'Status'] = 'new'
        base_completa.loc[base_completa['Status'].isin(['new', 'active']), 'enrolstatus1'] = '0'
        base_completa = base_completa.drop(columns=['Status'])
    except Exception as e:
        print(f"Erro ao juntar as bases: {e}")
        return None

    # Salvar o resultado em um objeto BytesIO
    try:
        output = BytesIO()
        base_completa.to_csv(output, sep=";", encoding='utf-8-sig', index=False)
        output.seek(0)
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return None

    print("Dados salvos com sucesso na pasta!!!")
    return output