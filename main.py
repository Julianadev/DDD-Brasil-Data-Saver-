import requests
import logging
import traceback
import pandas as pd
import os
import openpyxl

def get_response(ddd):
    url = f'https://brasilapi.com.br/api/ddd/v1/{ddd}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Chave {ddd} não encontrada')
            return None
    except ConnectionError:
        logging.error(f'Erro na solicitação da API: {response.status_code}')
        logging.error(traceback.format_exc())

def salvar(response_content, ddd):
    nome_arquivo = input('Digite o nome do arquivo: ').strip()
    if nome_arquivo:
        # Verifica se o arquivo termina em .xlsx
        if not nome_arquivo.endswith('.xlsx'):
            # Se não terminar será atribuído o .xlsx
            nome_arquivo += '.xlsx'

        estado = response_content.get('state', 'Estado Desconhecido')
        cidade = response_content.get('cities', [])
        codigo = ddd

        # Verificar se o arquivo existe
        if os.path.exists(nome_arquivo):
            # Se existir, carregar a planilha existnte
            df_existente = pd.read_excel(nome_arquivo)

            # Adicionar os novos dados ao DataFrame existente
            df_novo = pd.DataFrame(cidade, columns=['Cidades'])
            df_novo['Estado'] = estado
            df_novo['Codigo'] = codigo
            df_existente = pd.concat([df_existente, df_novo], ignore_index=True)

            # Salvar o DataFrame atualizado de volta no arquivo
            df_existente.to_excel(nome_arquivo, index=False)
        else:
            # Se o arquivo não existir, criar uma nova planilha
            df = pd.DataFrame(cidade, columns=['Cidades'])
            df['Estado'] = estado
            df['Codigo'] = codigo

            df.to_excel(nome_arquivo, index=False)

        print('Dados adicionados com sucesso.')
        os.startfile(nome_arquivo)
    else:
        print('Operação de salvamento cancelada.')

def main():
    try:
        ddd = input('Digite o DDD: ')
        response_content = get_response(ddd)
        if isinstance(response_content, str):
            print(response_content)
        elif 'state' in response_content:
            estado = response_content.get('state', 'Estado Desconhecido')
            cidade = response_content.get('cities', [])
            print('\n', estado)
            for i in cidade:
                print(i)
        else:
            print(f'Chave não encontrada')

        salvar_resultados = input('Deseja salvar os resultados? S/N ')
        if salvar_resultados.upper() == 'S':
            salvar(response_content, ddd)
        else:
            print('Encerrando o programa...')
    except ConnectionError:
        logging.error(f'Erro de conexão')
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()







