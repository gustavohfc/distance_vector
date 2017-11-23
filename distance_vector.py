# Projeto final de Internet do Futuro - 2/2017
# Implementacao do protocol distance vector
# Victor Vieira e Gustavo Carvalho


# Funcao que le o arquivo de configuracao de cada no na topologia sendo simulada
# O arquivo vai conter informacoes gerais do no e quais sao seus vizinhos, bem como custo do link
# A funcao vai receber o nome do arquivo e vai retornar os parametros lidos
def read_conf_file(file_name):
    f = open(file_name, 'r')

    node_name = f.readline() # le a primeira linha do arquivo, que contem o nome do no
    node_port_number = f.readline() # le a segunda linha do arquivo, que contem a porta UDP que o no escuta

    neighboor_list = [] #
    # loop que vai ler as informacoes dos nos vizinhos e adicionar um dicionario de cada no vizinho em uma lista
    for line in f:
        neigh_name, neigh_link_cost, neigh_ip = line.split()
        neigh_dict = {'neighboor_name': neigh_name, 'link_cost': neigh_link_cost, 'neighboor_ip': neigh_ip}
        neighboor_list.append(neigh_dict)


    f.closed

    return node_name, node_port_number, neighboor_list



a,b,c = read_conf_file('teste.txt')
print a
print b
for neigh in c:
    print neigh
