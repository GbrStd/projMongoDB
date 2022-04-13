import re

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dados_abertos"]
mycol = mydb["gastos_por_unidade"]

"""
2 - Criar 4 consultas referentes a estes dados, e utilizar o foreach para retornar estas informações filtradas. 
3 - Com as informações filtradas, gerar arquivos de saída para cada consulta realizada. 
4 - Criar um "menu" para que os itens 1, 2 e 3 possam ser executados.
"""

consult_cache = []

arquivo = open('gastos-por-unidade-03-2022.csv', mode='r', encoding="utf8")
headers = arquivo.readline().replace('\n', '').split(',')

while True:

    print("Escolha uma opção: ")

    print("[1] Salvar arquivo CSV no MongoDB")
    print("[2] Consultar MongoDB")
    print("[3] Baixar Arquivo .TXT com os resultados das consultas")
    print("[4] Sair")

    opcao = input("---> ")

    if opcao == '1':
        lines = arquivo.readlines()
        blocks = []
        for line in lines:
            current_line = line.replace('\n', '').strip()
            # Regex para encontrar a vírgula do valor em R$
            pattern = r"\,+([0-9][0-9])\""
            current_line = re.subn(pattern, '', current_line)[0]
            current_line = current_line.replace('"', '').split(',')
            current_index = len(blocks)
            blocks.append({})
            for index, header in enumerate(headers):
                # Remove 2 ou mais espaços
                blocks[current_index][header] = re.sub('  +', ' ', current_line[index])
        mycol.insert_many(blocks)
        print("Dados Inseridos!")

    elif opcao == '2':
        filter_query1 = {"natureza_despesa": "SERV. PESSOA JURÍDICA"}
        filter_query2 = {"natureza_despesa": "PASSAGENS"}
        filter_query3 = {"_id": "6256fa90c31c37f740409f69"}
        filter_query4 = {"unidade": "CENTRO DE APOIO AO DESENV TECNOLOGICO"}

        results_db = [mycol.find(filter_query1).sort("unidade", 1),
                      mycol.find(filter_query2),
                      mycol.find(filter_query3),
                      mycol.find(filter_query4)]
        for result in results_db:
            for entry in result:
                current_element = []
                for keys in entry:
                    current_element.append(str(entry[keys]))
                consult_cache.append([','.join(current_element)])

    elif opcao == '3':
        if len(consult_cache) <= 0:
            print("Faça uma consulta antes de baixar os resultados!")
        else:
            consults_txt = open('resultados.txt', mode='w+', encoding="utf8")
            consults_txt.write(','.join(headers) + '\n')
            for consult in consult_cache:
                consults_txt.write(consult[0] + '\n')
            consults_txt.close()

    elif opcao == '4':
        arquivo.close()
        break

    else:
        print("Opção inválida!")
