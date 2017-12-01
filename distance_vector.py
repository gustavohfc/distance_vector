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
    node_port_number = int(f.readline()) # le a segunda linha do arquivo, que contem a porta UDP que o no escuta

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


# Funcao que vai criar a string de distance vector de cada no
# A Funcao vai retornar uma string com o vetor distancia
# NUMBER OF DEST EH O NUMERO DE VIZINHOS QUE DADO NO TEM
def create_dist_vect(node_name, neighboor_list, routing_table):
    number_of_dest = len(neighboor_list)
    
    # Parametros de cabecalho da string do distance vector
    dist_vect_str = node_name
    dist_vect_str += str(number_of_dest) + '\n'
    
    # Vai adicionar a string os custos atualizados e os destinos do no atual
    for x in routing_table:
        dist_vect_str += x['destination_name'] + ' ' + x['destination_addr'] + ' '
        dist_vect_str += str(x['distance']) + '\n'

    return dist_vect_str


# Funcao recebe a lista inicial de vizinhos e monta a tabela de roteamento inicial
def initialize_routing_table(node_name, neighboor_list):
    routing_table = []

    routing_table.append({
        'destination_name': node_name.rstrip(),
        'destination_addr': '127.0.0.1',
        'distance': 0,
        'next_hop': ''
    })

    for neighboor in neighboor_list:
        routing_table.append({
            'destination_name': neighboor['neighboor_name'],
            'destination_addr': neighboor['neighboor_ip'],
            'distance': neighboor['link_cost'],
            'next_hop': neighboor['neighboor_name']
        })

    return routing_table


def write_routing_table(routing_table):
    with open("routing_table_log.txt", "a") as log:
        for entry in routing_table:
            log.write("Name: {}\t\tAddress: {}\t\tDistance: {}\t\tNext hop: {}\n".format(entry['destination_name'], entry['destination_addr'], entry['distance'], entry['next_hop']))
        log.write("\n\n\n----------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n")



def update_routing_table(routing_table, data):
    sender_name, number_of_dest, dist_vec_list = read_dist_vect_file(data)
    change = False

    for dist_vector in dist_vec_list:
        node_found = False

        # Encontra o no final na tabela de roteamento
        for entry_destination in routing_table:
            if entry_destination['destination_name'] == dist_vector['dest_name']:
                node_found = True

                # Encontra a entrada na tabela de roteamento correspondente ao vizinho que enviou o dist_vector
                for entry_neighboor in routing_table:
                    if sender_name == entry_neighboor['destination_name'] and entry_neighboor['distance'] + dist_vector['distance'] < entry_destination['distance']:
                        entry_destination['distance'] = dist_vector['distance'] + entry_neighboor['distance']
                        entry_destination['next_hop'] = entry_neighboor['destination_name']

                        change = True

        # Se o no de destino ainda nao esta na tabela de roteamento adiciona uma nova
        # linha na tabela de roteamento
        if not node_found:
            for entry in routing_table:
                if sender_name == entry['destination_name']:
                    routing_table.append({
                        'destination_name': dist_vector['dest_name'],
                        'destination_addr': dist_vector['dest_ip'],
                        'distance': dist_vector['distance'] + entry['distance'],
                        'next_hop': entry['destination_name']
                    })

                    change = True

    return change


if __name__ == "__main__":
    node_name, node_port_number, neighboor_list = read_conf_file('conf.txt')

    # Inicializa o distance vector apenas com os vizinhos
    routing_table =  initialize_routing_table(node_name, neighboor_list)

    # Inicializa o socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((socket.gethostname(), node_port_number))
    sock.settimeout(5)

    while True:
        try:
            data, addr = sock.recvfrom(2048)
        except socket.timeout:
            dist_vector = create_dist_vect(node_name, neighboor_list, routing_table)

            for neighboor in neighboor_list:
                sock.sendto(dist_vector, (neighboor['neighboor_ip'], node_port_number))

            continue

        change = update_routing_table(routing_table, data)

        if change == True:
            dist_vector = create_dist_vect(node_name, neighboor_list, routing_table)

            # Envia o distance para todos os vizinho
            for neighboor in neighboor_list:
                sock.sendto(dist_vector, (neighboor['neighboor_ip'], node_port_number))

            write_routing_table(routing_table)
