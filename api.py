#libraries
import requests
import pprint
import pandas as pd
import json

#API link IBGE QUERY BUILDER
link = "https://servicodados.ibge.gov.br/api/v3/agregados/1209/periodos/2022/variaveis/606?localidades=N2[3]|N3[31]&classificacao=58[3299,3300,3301,3520,3244,3245]"

#request
request_link = requests.get(link)
informations = request_link.json() 
data = informations

# Função para transformar o dicionário em DataFrame
def process_data(data):
    processed_data = []
    for record in data:
        id_ = record["id"]
        variavel = record["variavel"]
        unidade = record["unidade"]
        for resultado in record["resultados"]:
            classificacoes = resultado["classificacoes"]
            for cl in classificacoes:
                categoria = cl["categoria"]
            series = resultado["series"]
            for serie in series:
                localidade = serie["localidade"]["nome"]
                valor_2022 = serie["serie"]["2022"]
                processed_data.append({
                    "id": id_
                    ,"variavel": variavel
                    ,"unidade": unidade
                    ,"localidade": localidade
                    ,"valor_2022": valor_2022
                    ,'categoria':categoria
                })
    return pd.DataFrame(processed_data)

# Processando os dados
df = process_data(data)
df = pd.DataFrame(df)

# Criando uma nova coluna 'grupo_idade' a partir das classificações
df['grupo_idade'] = df['categoria'].apply(lambda x: list(x.values())[0])

#print(df)
#------------
df = pd.DataFrame(df)
print(df)

#---------------------------------
#Visualização - QUATIDADE DE POPULAÇÃO EM MG POR FAIXA ETÁRIA

# import matplotlib.pyplot as plt

# # Filtrando os dados por grupo de idade
# grupo_df = df[df['localidade'] == 'Minas Gerais']

# # Gerando o gráfico de barras
# # Gerando o gráfico de barras
# plt.figure(figsize=(10, 6))
# plt.bar(grupo_df['grupo_idade'], grupo_df['valor_2022'].sort_values(ascending=True), color='skyblue')

# # Adicionando título e rótulos
# plt.title('População por Grupo de Idade - Localidade: Minas Gerais')
# plt.xlabel('Localidade: Minas Gerais')
# plt.ylabel('População')

# # Exibindo o gráfico
# plt.show()


