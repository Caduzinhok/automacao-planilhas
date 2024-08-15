import pandas as pd
from io import BytesIO

def main(file_initial_obj, file_final_obj, name_file):
    # Validações para o nome do arquivo
    name_file = name_file.split('.')[0].replace(".csv", '')
    
    print("Lendo dados do Arquivo CSV...")

    try:
        # Ler arquivos como CSV
        base_inicial = pd.read_csv(file_initial_obj, sep=";", encoding='utf-8')
        base_final = pd.read_csv(file_final_obj, sep=";", encoding='utf-8')
        base_inicial['Status'] = ''
        base_final['Status'] = ''
    except Exception as e:
        print(f"Erro ao ler os arquivos CSV: {e}")
        return None

    print("Filtrando dados do arquivo CSV...")

    try:
        # Verificando items que estavam na base 1 (Ativos e Suspensos)
        for index, row in base_inicial.iterrows():
            user_mail = row['username']
            curso = row['course1']

            if user_mail == "#N/D":
                base_inicial.at[index, 'Status'] = 'suspended'
                continue

            base_filtrada = base_final[(base_final['username'] == user_mail) & (base_final['course1'] == curso)]

            if not base_filtrada.empty:
                base_inicial.at[index, 'Status'] = 'active'
            else:
                base_inicial.at[index, 'Status'] = 'suspended'
    except KeyError as e:
        print(f"Erro nas colunas: {e}")
        return None
    except Exception as e:
        print(f"Erro ao cruzar informações: {e}")
        return None

    print("Juntando bases e salvando no Downloads...")
    
    try:
        # Juntar as bases
        base_completa = pd.merge(base_inicial, base_final, on=["username", "course1"], how='outer', suffixes=('_inicial', '_final'))
        base_completa.drop(columns=['Status_final'], inplace=True)
        base_completa.rename(columns={"Status_inicial": "Status"}, inplace=True)
        base_completa['enrolstatus1'] = ''

        # Definir valores na coluna enrolstatus1
        base_completa.loc[base_completa['Status'] == 'suspended', 'enrolstatus1'] = '1'
        base_completa.loc[base_completa['Status'].isnull(), 'Status'] = 'new'
        base_completa.loc[base_completa['Status'].isin(['new', 'active']), 'enrolstatus1'] = '0'
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
