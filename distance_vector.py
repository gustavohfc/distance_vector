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

    neighboor_list = [] 
    # loop que vai ler as informacoes dos nos vizinhos e adicionar um dicionario de cada no vizinho em uma lista
    for line in f:
        neigh_name, neigh_link_cost, neigh_ip = line.split()
        neigh_dict = {'neighboor_name': neigh_name, 'link_cost': int(neigh_link_cost), 'neighboor_ip': neigh_ip}
        neighboor_list.append(neigh_dict)


    f.closed

    return node_name, node_port_number, neighboor_list

# Funcao que le o arquivo de distance vector que um no recebe de outros
# O arquivo vai conter o nome do no que enviou, numero de destinos e outras informacoes
# A funcao vai receber o nome do arquivo e vai retornar os parametros lidos
def read_dist_vect_file(file_name):
    f = open(file_name, 'r')

    sender_name = f.readline() # le a primeira linha do arquivo que eh o nome do vizinho que enviou
    number_of_dest = int(f.readline()) # le a segunda linha do arquivo, que eh o numero de destinos

    dist_vec_list = []
    # loop que vai ler o distance vector do no que enviou e vai colocar em um dicionario
    for line in f:
        dest_name, dist = line.split()
        dist_vec_dict = {'dest_name': dest_name, 'distance': int(dist)}
        dist_vec_list.append(dist_vec_dict)

    f.closed

    return sender_name, number_of_dest, dist_vec_list


# Funcao que monta a tabela de roteamento, que contem: destino, custo e next hop
#TODO

# Funcao que vai criar o arquivo de distance vector de cada no
# O arquivo vai conter o nome do no que esta enviando, numero de destinos e outras informacoes
# A Funcao vai escrever em um arquivo texto
# NUMBER OF DEST EH O NUMERO DE VIZINHOS QUE DADO NO TEM
def write_dist_vect_file(node_name, number_of_dest, dist_vec_list):
    file_name = node_name + '-distance_vector.txt' # cria o nome do arquivo
    f = open(file_name, 'w')
    
    # Parametros de cabecalho do arquivo de distance vector
    f.write(node_name)
    f.write(str(number_of_dest) + '\n')
    
    # Vai escrever no arquivo os custos atualizados e os destinos do no atual
    for x in dist_vec_list:
        str_file = x['dest_name'] + '\t' + str(x['distance']) + '\n'# constroi a string que vai ser escrita no arquivo
        f.write(str_file)

    f.closed


a,b,c = read_conf_file('no1-conf.txt')
d, e, f = read_dist_vect_file('no1-distance_vector.txt')
write_dist_vect_file(a, 3, f)
write_conf_file(a, b, c)
