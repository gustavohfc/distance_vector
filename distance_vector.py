# Projeto final de Internet do Futuro - 2/2017
# Implementacao do protocol distance vector
# Victor Vieira e Gustavo Carvalho

import socket


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

# Funcao que recebe uma string de algum outro no e retorna o dicionario do distance vector d
def read_dist_vect_file(dist_vector_str):
    splited_string = dist_vector_str.splitlines()
    
    sender_name = splited_string[0]
    number_of_dest = int(splited_string[1]) 

    dist_vec_list = []
    # loop que vai ler o distance vector do no que enviou e vai colocar em um dicionario
    for i in range(2, len(splited_string)):
        dest_name, dest_ip, dist = splited_string[i].split()
        dist_vec_dict = {'dest_name': dest_name, 'dest_ip': dest_ip, 'distance': int(dist)}
        dist_vec_list.append(dist_vec_dict)

    return sender_name, number_of_dest, dist_vec_list


# Funcao que monta a tabela de roteamento, que contem: destino, custo e next hop
#TODO

# Funcao que vai criar a string de distance vector de cada no
# A Funcao vai retornar uma string com o vetor distancia
# NUMBER OF DEST EH O NUMERO DE VIZINHOS QUE DADO NO TEM
def create_dist_vect(node_name, neighboor_list, routing_table):
    number_of_dest = len(neighboor_list)
    
    # Parametros de cabecalho da string do distance vector
    dist_vect_str = node_name + '\n'
    dist_vect_str = dist_vect_str + str(number_of_dest) + '\n'
    
    # Vai adicionar a string os custos atualizados e os destinos do no atual
    for x in routing_table:
        dist_vect_str = dist_vect_str + x['destination_name'] + ' ' + str(x['destination_addr']) + ' '
        dist_vect_str = dist_vect_str + x['distance'] + ' ' + x['next_hop'] + '\n'

    return dist_vect_str



# TODO: Funcao que recebe routing_table e retorna uma string para ser enviada para outro no


# TODO: Funcao que recebe uma string e retorna o dicionario do distance vector


# Funcao recebe a lista inicial de vizinhos e monta a tabela de roteamento inicial
def initialize_routing_table(neighboor_list):
    routing_table = []

    for neighboor in neighboor_list:
        routing_table.append({
            'destination_name': neighboor['neighboor_name'],
            'destination_addr': neighboor['neighboor_ip'],
            'distance': neighboor['link_cost'],
            'next_hop': neighboor['neighboor_name']
        })

    return routing_table

# TODO: update_routing_table(routing_table, data, addr)


# TODO: send_dist_vector(routing_table)


def write_routing_table(routing_table):
    with open("routing_table_log.txt", "a") as log:
        for entry in routing_table:
            log.write("Name: {}\t\tAddress: {}\t\tDistance: {}\t\tNext hop: {}\n".format(entry['destination_name'], entry['destination_addr'], entry['distance'], entry['next_hop']))
        log.write("\n\n\n----------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n")


# routing_table_entry = {'destination': , 'distance': , 'next_hop': }


if __name__ == "__main__":
    node_name, node_port_number, neighboor_list = read_conf_file('conf.txt')

    # Inicializa o distance vector apenas com os vizinhos
    routing_table =  initialize_routing_table(neighboor_list)

    # Inicializa o socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((socket.gethostname(), node_port_number))
    sock.settimeout(5)

    while True:
        data, addr = sock.recvfrom(1024)

        change = update_routing_table(routing_table, data, addr)

        if change == True:
            dist_vector = 
            send_dist_vector(dist_vector)
            write_routing_table(routing_table)


# a,b,c = read_conf_file('no1-conf.txt')
# d, e, f = read_dist_vect_file('no1-distance_vector.txt')
# write_dist_vect_file(a, 3, f)
# write_conf_file(a, b, c)