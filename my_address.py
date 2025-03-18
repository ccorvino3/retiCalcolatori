import ipaddress
import random
from utils import power_of_two, is_power_of_two
import re
import reti as r


# Funzione che stampa le possibili tracce da computare
def print_trace_questions():
    print("\n1. Nell'indirizzamento senza classi, dato l'indirizzo IP 'IP' si determini: \n\tIl numero di indirizzi IP del blocco e quanti indirizzi IP possono essere associati agli host, \n\tIl network address, \n\tIl broadcast address, \n\tLa subnet mask.")
    print("2. Ad un'organizzazione viene assegnato il seguente blocco di indirizzi 'IP'. \n\tL'organizzazione ha bisogno di creare le seguenti 'n' sottoreti. \n\tSi progettino le sottoreti utilizzando il subnetting.")
    print("3. Dati le seguenti 'n' reti, verificare se sono aggregabili con la tecnica del supernetting. \n\tNel caso lo siano determinare Network Address e Broadcast Address della SuperRete ottenuta. \n\tNel caso non lo siano esplicitare il motivo per cui non sono aggregabili.")
    print("4. Dato l'indirizzo IP 'IP' e supposto che si adotti l'indirizzamento classful si vuol conoscere: \n\tLa classe dell'indirizzo, \n\tSe l'indirizzo è di rete oppure di un host, \n\tInfine, si vuol conoscere il numero di hosts della rete a cui apparterrebbe lo stesso indirizzo IP se si adottasse l'indirizzamento classless con prefisso pari a 'n' bit.")
    print("5. Si consideri la seguente configurazione Ipv4: \n\tIP Address: 'IP' \n\tSubnet Mask: 'SM' (Opzionale). \n   Si determini: \n\tIl numero di indirizzi IP del blocco, \n\tIl network address, \n\tIl broadcast address.")
    print("6. Torna al menu principale.")
        
    # Richiedere all'utente di scegliere una traccia
    return int(input("Inserisci il numero della traccia da computare: "))


''' Funzioni per gli indirizzi IP '''

# Funzione che converte un numero decimale in binario, adattato per gli indirizzi IP
def dec2bin(value):
    # Verifica se l'IP ha un prefisso
    if '/' in str(value):
        ip, prefix = str(value).split('/')
    else:
        ip = str(value)
        prefix = None  # Nessun prefisso presente

    # Converti l'indirizzo IP in binario, suddividendolo in blocchi da 8 bit
    if '.' in ip:  # Se è un indirizzo IPv4
        binary_ip = '.'.join([bin(int(octet))[2:].zfill(8) for octet in ip.split('.')])
    else:  # Se è un singolo numero (questo caso è meno comune, ma lo gestiamo comunque)
        binary_ip = bin(int(ip))[2:].zfill(8)

    # Riaggiungi il prefisso se era presente
    if prefix:
        return f"{binary_ip}/{prefix}"
    else:
        return binary_ip

# Funzione che converte un numero binario in decimale, adattato per gli indirizzi IP
def bin2dec(value):
    # Controlla se l'input contiene un prefisso
    if '/' in str(value):
        value, prefix = str(value).split('/')
    else:
        prefix = None  # Nessun prefisso presente

    # Verifica se l'input è un indirizzo IP binario (controlla se c'è un punto)
    if '.' in str(value):
        # Se è un indirizzo IP binario, suddividilo in blocchi da 8 bit e converti ciascun blocco
        decimal_ip = '.'.join([str(int(octet, 2)) for octet in value.split('.')])
    else:
        # Se è un singolo numero binario, convertilo in decimale
        decimal_ip = str(int(value, 2))

    # Riaggiungi il prefisso se era presente
    if prefix:
        decimal_ip += f"/{prefix}"
    
    return decimal_ip

# Funzione che prende in input un IP e restituisce un indirizzo IP valido
def take_ip(msg, req_prefix=True):
    correct = False
    while not correct:
        ip = input(msg).replace(" ", "")  # Rimuovere eventuali spazi
        
        if not has_IP_prefix(ip):
            prefix = None
        else:
            prefix = True

        try:
            if (prefix is not None):
                ip_obj = ipaddress.ip_network(ip, strict=False)
            else:
                ip_obj = ip
            correct = check_prefixIP(ip, req_prefix) and check_pointIP(ip)
        except ValueError:
            print("Indirizzo IP non valido. Riprova.")

    # A questo punto, l'indirizzo IP è stato verificato e corretto.
    return ip_obj

# Funzione che verifica se un indirizzo IP contiene i 3 "." separatori
def check_pointIP(ip):
    # Separa l'indirizzo IP dal prefisso, se presente
    ip_part = ip.split('/')[0]

    # Dividi l'indirizzo IP usando il punto come delimitatore
    octets = ip_part.split('.')
    
    # Verifica se ci sono esattamente 4 ottetti (3 punti)
    if len(octets) == 4:
        # Controlla che ciascun ottetto sia composto solo da cifre e che sia un numero valido
        for octet in octets:
            if not octet.isdigit() or not (0 <= int(octet) <= 255):
                return False
        return True
    else:
        return False

# Funzione che verifica se un indirizzo IP ha un prefisso
def has_IP_prefix(ip):
    # Regex per verificare un IP con un prefisso che ha 1 o 2 cifre dopo il '/'
    # Usa il pattern regex per verificare l'IP con il prefisso
    return True if re.match(r"^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$", ip) else False

# Funzione che verifica se un indirizzo IP con prefisso è valido, dato un flag se il prefisso è richiesto
def check_prefixIP(ip, req_prefix):  
    try:
        if req_prefix:
            # Prima, controlla se l'input contiene il carattere '/'
            if '/' in ip:
                # Divide l'input prendendo solo il prefisso (parte dopo il carattere '/')
                prefix_part = ip.split('/')[1]

                # Controlla che il prefisso sia un numero intero valido
                if prefix_part.isdigit():
                    if 0 <= int(prefix_part) <= 32:
                        return True
                    else:
                        print("Prefisso non valido. Deve essere un numero tra 0 e 32.")
                        return False
                else:
                    print("Prefisso non valido. Deve essere un numero intero.")
                    return False
            else:
                print("Indirizzo IP senza prefisso o formato non corretto.")
                return False
        else:
            return True
    except ValueError:
        print("Indirizzo IP non valido.")
        return False

# Funzione che prende un IP random (se non dato in input) e lo restituisce
def take_ip_listRandom(networks_list, ip=None):
    # Restituisci un IP random se non è stato fornito in input else restituisci l'IP dato
    return random.choice(networks_list) if ip is None else ip

# Funzione per fare la negazione di un indirizzo IP di 4 ottetti e 3 "." separatori
def negate_ip(ip):
    # Controlla se l'IP contiene un prefisso
    if '/' in str(ip):
        ip, prefix = str(ip).split('/')
    else:
        prefix = None  # Nessun prefisso presente

    # Converti l'indirizzo IP in una stringa se non lo è già
    if isinstance(ip, ipaddress.IPv4Address):
        ip = str(ip)

    # Dividi l'indirizzo IP in ottetti
    octets = ip.split('.')
    
    # Verifica che l'indirizzo IP abbia 4 ottetti
    if len(octets) != 4:
        raise ValueError("Indirizzo IP non valido. Deve avere 4 ottetti separati da punti.")
    
    # Esegui la negazione di ciascun ottetto
    negated_octets = []
    for octet in octets:
        # Converti l'ottetto in intero
        octet_int = int(octet)
        # Esegui la negazione bit a bit (inverti i bit)
        negated_octet = 255 - octet_int
        # Aggiungi l'ottetto negato alla lista
        negated_octets.append(str(negated_octet))
    
    # Unisci gli ottetti negati in un indirizzo IP
    negated_ip = '.'.join(negated_octets)
    
    # Riaggiungi il prefisso se era presente
    if prefix:
        negated_ip += f"/{prefix}"
    
    return negated_ip

# Funzione che calcola n Ip, NA e BA
def compute_ip_NA_BA(ip, SM=None, has_sm=True):
    NA = ipaddress.ip_network(ip, strict=False).network_address
    BA = ipaddress.ip_network(ip, strict=False).broadcast_address
    
    if has_sm:
        prefix = compute_ip_block(SM)
        print(f"network address = {dec2bin(ip)} AND {dec2bin(SM)} = {dec2bin(NA)} = {NA}/{prefix}")
        print(f"broadcast address = {dec2bin(ip)} OR {dec2bin(negate_ip(SM))} = {dec2bin(BA)} = {BA}/{prefix}")
        
    else:
        network = ipaddress.ip_network(ip, strict=False).prefixlen
        host = 32 - network
        
        # Determinare il numero di indirizzi IP del blocco
        print(f"\tnumero di indirizzi IP del blocco = 32 - {network} = {host} -> 2^{host} = {2**host}")
        print(f"\tnetwork address = {dec2bin(NA)} = {NA}/{network} \n\t\t(Imposto tutti i bit degli host ({host}) a 0)")
        print(f"\tbroadcast address = {dec2bin(BA)} = {BA}/{network} \n\t\t(Imposto tutti i bit degli host ({host}) a 1)")

# Calcola il numero di indirizzi IP data la SM (Subnet Mask)
def compute_ip_block(SM):
    # Nego la subnet mask e la converto in binario
    not_SM_bin = dec2bin(negate_ip(SM))

    # Somma 1 alla subnet mask negata binaria
    not_SM_bin_plus_1_bin = add_binary(not_SM_bin.replace('.', ''), '1')
    not_SM_bin_plus_1_int = bin2dec(not_SM_bin_plus_1_bin)
    
    print(f"numero IP del blocco = NOT(SM) + 1 = {not_SM_bin} + 1 = {not_SM_bin_plus_1_bin} = {not_SM_bin_plus_1_int}")
    
    return 32 - power_of_two(int(not_SM_bin_plus_1_int))

# Funzione che somma due numeri binari e restituisce il risultato in binario, per il punto 5
def add_binary(bin1, bin2):
    # Restituisci il risultato come stringa binaria senza il prefisso '0b'
    return bin(int(bin1, 2) + int(bin2, 2))[2:]


''' Funzioni per computare le tracce '''

# Funzione che verifica se una stringa inizia con "startwith" e, in caso affermativo, converte i primi tre caratteri in minuscolo, per il punto 3
def lowercase_non_prefix(startswith, s):
    # Verifica se la stringa inizia con "NON"
    if s.startswith(startswith):
        # Converte i primi tre caratteri in minuscolo e li concatena al resto della stringa
        return s[:3].lower() + " "
    return ""

# Funzione che verifica la contiguità delle reti nel supernetting, per il punto 3
def check_contiguity(networks_list):
    # Controlla se la lista è vuota o ha solo un elemento
    if len(networks_list) < 2:
        return False  # Non ci sono reti consecutive da confrontare

    for i in range(len(networks_list) - 1):
        current_network = networks_list[i]
        next_network = networks_list[i + 1]

        # Calcola il numero di host nella rete corrente
        num_hosts = 2 ** (32 - current_network.prefixlen)

        # Calcola l'indirizzo finale della rete corrente
        last_ip = current_network.network_address + num_hosts - 1

        # Verifica se l'indirizzo finale + 1 è uguale all'indirizzo di rete successivo
        if last_ip + 1 != next_network.network_address:
            return False  # Le reti non sono consecutive

    return True  # Tutte le reti sono consecutive

# Funzione che verifica se le reti sono aggregabili con il supernetting, per il punto 3
def check_supernetting():
    # Richiedere all'utente di inserire le reti da verificare
    n = int(input("Inserisci il numero di reti da verificare: "))
    networks_list = []
    for i in range(n):
        network = take_ip(f"Inserisci l'indirizzo IP della rete {i + 1}: ")
        networks_list.append(network)
    print("\n") # Aggiungere spazi per una migliore leggibilità
    
    # Determinare se si può fare il supernetting
    conditions = []
    
    ## Verificare se il numero di reti è una potenza di 2
    conditions.append(is_power_of_two(n))
    esito = "SODDISFATTA" if conditions[0] else "NON SODDISFATTA"
    print(f"1. Numero di reti potenza di 2 -> {esito}. \n\tPerché {n} {lowercase_non_prefix('NON', esito)}è una potenza di 2.")
    
    ## Verificare se le reti hanno la stessa dimensione
    if len(set([network.prefixlen for network in networks_list])) == 1:
        esito = True
        msg = f" ({networks_list[0].prefixlen})"
    else: 
        esito = False
        msg = ""
    conditions.append(esito)
    esito = "SODDISFATTA" if conditions[1] else "NON SODDISFATTA"
    print(f"2. Dimensione delle reti uguale -> {esito}. \n\tPerché le {n} reti {lowercase_non_prefix('NON', esito)}hanno la stessa dimensione{msg}.")
    
    ## Verificare se le reti sono contigue
    if (conditions[1]):
        conditions.append(check_contiguity(networks_list))
    esito = "SODDISFATTA" if conditions[2] else "NON SODDISFATTA"
    print(f"3. Contiguità delle reti -> {esito}. \n\tPerché ogni rete {lowercase_non_prefix('NON', esito)}ha una distanza di 2^(32 - {networks_list[0].prefixlen}) = {2 ** (32 - networks_list[0].prefixlen)} IP dall'altra.")
    
    ## Verificare la divisibilità
    print(f"4. Divisibilità:")
    ### Calcolare il numero di reti
    n_networks = power_of_two(n)
    print(f"\tNumero di reti = 2^{n_networks} = {2 ** n_networks}")
    ### Calcolare il numero di host delle reti
    if (conditions[1]):
        n_host = 32 - networks_list[0].prefixlen
        print(f"\tNumero di host delle reti = 2^(32 - {networks_list[0].prefixlen}) = 2^{n_host} = {2 ** n_host}")
    else:
        conditions.append(False)
    ### Prodotto tra il numero di reti e il numero di host delle reti
    print(f"\t2^{n_networks} * 2^{n_host} = 2^({n_networks + n_host}) = {2 ** (n_networks + n_host)}")
    ### Verificare se il primo IP in binario partendo da destra ha n_host + n_networks bit a 0
    host = n_host + n_networks
    conditions.append(dec2bin(networks_list[0].network_address).replace('.', '').endswith('0' * (host)))
    esito = "SODDISFATTA" if conditions[3] else "NON SODDISFATTA"
    print(f"   Divisibilità -> {esito}. \n\tPerché il primo IP {networks_list[0]} in binario {dec2bin(networks_list[0].network_address)} {lowercase_non_prefix('NON', esito)}ha {host} bit a 0. (partendo da destra)")
    
    if all(conditions):
        print(f"\nLe reti sono aggregabili con il supernetting.\n\tPertanto la super-rete da creare avrà parte host = {host} e parte network = 32 - {host} = {32 - host} -> /{32 - host}")
        return True, host, 32 - host, networks_list
    else:
        print("\nLe reti non sono aggregabili con il supernetting.")
        return False, None, None, None

# Funzione che determina la classificazione di un indirizzo IP classful, per il punto 4
def class_ip_classful(ip, classification):
    # Dividi l'indirizzo IP in ottetti
    octets = ip.split('.')

    # Verifica che ci siano esattamente 4 ottetti
    if len(octets) != 4:
        print("Indirizzo IP non valido. Deve avere 4 ottetti separati da punti.")
        return

    # Converti il primo ottetto in intero
    first_octet = int(octets[0])
    
    # Converti il primo ottetto in binario
    first_octet_bin = dec2bin(first_octet)

    # Trova la classificazione corrispondente
    for r, class_number, _, class_letter in classification:
        if first_octet in r:
            # Prendi i primi n bit del primo ottetto
            print_bits = first_octet_bin[:class_number]
            print(f"È di classe {class_letter}, perché inizia per {print_bits} ({first_octet} = {first_octet_bin})")
            return class_letter

# Funzione per determinare se un indirizzo IP è di rete o di host, per il punto 4
def is_host_network(ip, classification, class_letter):
    # Prendo il numero di blocchi di network e di host dato class_number
    for _, second_elem, third_elem, cls in classification:
        if cls == class_letter:
            n_block_net = second_elem
            n_block_host = third_elem
    
    # Divido l'IP nei blocchi della parte host (dopo la parte network)
    block_host = ip.split('.')[n_block_net:]
    
    # Verifico se tutti i blocchi della parte host sono uguali a 0, 1 o mix di 0 e 1
    all_zero = True
    all_one = True
    mixed = False
    for i in range(n_block_host):
        i_block_host = dec2bin(int(block_host[i]))

        if i_block_host.count('0') == 8:
            all_one = False
        elif i_block_host.count('1') == 8:
            all_zero = False
        else:
            all_zero = False
            all_one = False
            mixed = True

    # Verifica le condizioni finali
    if all_zero:
        print(f"L'indirizzo IP {ip} è di rete, perché gli ultimi {n_block_host} blocchi sono uguali a 0.")
    elif all_one:
        print(f"L'indirizzo IP {ip} è di broadcast, perché gli ultimi {n_block_host} blocchi sono tutti uguali a 1.")
    elif mixed:
        print(f"L'indirizzo IP {ip} è di host, perché gli ultimi {n_block_host} blocchi contengono sia 0 sia 1.")
    return

# Realizza il punto 1
def classless():
    # Richiedere all'utente di inserire l'indirizzo IP + calcolo di network e host
    ip = take_ip("Inserisci l'indirizzo IP: ")
    
    # Determinare il numero di indirizzi IP del blocco, il network address e il broadcast address
    compute_ip_NA_BA(str(ip), None, False)

# Realizza il punto 2
def subnetting():
    # Variabili locali utili per l'esercizio
    subnets_list = [] # Lista di dizionari per memorizzare le informazioni delle sottoreti
    
    # Richiedere all'utente di inserire l'indirizzo IP e il numero di sottoreti
    ip = take_ip("Inserisci l'indirizzo IP: ")
    n = int(input("Inserisci il numero di sottoreti: "))
    for i in range(n):
        subnet = {
            'n_ip': int(input(f"\tSottorete {i + 1} con indirizzi IP: ")),
            'network': None,
            'host': None,
            'NA': None,
            'BA': None
        }
        subnets_list.append(subnet)

    # Determinare i prefissi per ogni sottorete
    for i in range(n):
        subnets_list[i]['host'] = power_of_two(subnets_list[i]['n_ip'])
        n_ip = 2 ** subnets_list[i]['host']
        subnets_list[i]['network'] = 32 - subnets_list[i]['host']
        print(f"\nAlla sottorete {i + 1} saranno assegnati {n_ip} indirizzi IP -> 2**{subnets_list[i]['host']} = {n_ip}")
        print(f"\t-> 32 - {subnets_list[i]['host']} = {subnets_list[i]['network']} -> /{subnets_list[i]['network']}")
    print("\n") # Aggiungere spazi per una migliore leggibilità

    # Ordinare la lista in base al valore della chiave "network"
    subnets_list = sorted(subnets_list, key=lambda x: x['network'])
    subnets_list[0]['NA'] = ipaddress.ip_network(f"{ip.network_address}/{subnets_list[0]['network']}", strict=False)

    # Determinare il network address e il broadcast address per ogni sottorete
    for i in range(n):
        if i == 0: # Prima sottorete
            subnets_list[i]['BA'] = subnets_list[i]['NA'].broadcast_address
        else:  # Sottorete successiva
            subnets_list[i]['NA'] = ipaddress.ip_network(f"{subnets_list[i - 1]['BA'] + 1}/{subnets_list[i]['network']}", strict=False)
            subnets_list[i]['BA'] = subnets_list[i]['NA'].broadcast_address
        print(f"Sottorete {i + 1}: da {dec2bin(str(subnets_list[i]['NA'].network_address))}/{subnets_list[i]['network']} a {dec2bin(str(subnets_list[i]['BA']))}/{subnets_list[i]['network']} (cambio quindi gli host bit ({subnets_list[i]['host']}) a 1)")
        print(f"cioè da {subnets_list[i]['NA']} a {subnets_list[i]['BA']}/{subnets_list[i]['network']}")

# Realizza il punto 3
def supernetting():
    check, host, network, network_list = check_supernetting()
    if (check):
        # Calcolo la subnet mask
        SM = ipaddress.ip_network(f"{network_list[0].network_address}/{network}", strict=False).netmask
        print(f"\tsubnet mask = {dec2bin(SM)} = {SM}/{network} \n\t\t(Imposto network = {network} bit a 1 e host = {host} bit a 0)")
        
        # Calcolo il network address
        NA = ipaddress.ip_network(f"{network_list[0].network_address}/{network}", strict=False).network_address
        ip_random_list = take_ip_listRandom(network_list)
        print(f"\tnetwork address = un IP della rete AND SM = (prendo per semplicità uno della lista: {ip_random_list.network_address}) \n\t\t{dec2bin(ip_random_list.network_address)} AND \n\t\t{dec2bin(SM)} = \n\t\t{dec2bin(NA)} = {NA}/{network}")
        
        # Calcolo il broadcast address
        BA = ipaddress.ip_network(f"{network_list[-1].broadcast_address}/{network}", strict=False).broadcast_address
        print(f"\tbroadcast address = un IP della rete OR NOT(SM) = (prendo per semplicità uno della lista: {ip_random_list.network_address}) \n\t\t{dec2bin(ip_random_list.broadcast_address)} OR \n\t\t{dec2bin(negate_ip(SM))} = \n\t\t{dec2bin(BA)} = {BA}/{network}")
        
        print(f"Le {len(network_list)} reti sono state aggregate in una super-rete: {NA}/{network}")
    else:
        print("Non è possibile creare una super-rete.")

# Realizza il punto 4
def classful():
    # Richiedere all'utente di inserire l'indirizzo IP
    ip = take_ip("Inserisci l'indirizzo IP: ", False)
    
    # Dizionario di classificazione
    classification = [
        (range(0, 128), 1, 0, 'A'),   # Classe A
        (range(128, 192), 2, 0, 'B'), # Classe B
        (range(192, 224), 3, 0, 'C'), # Classe C
        (range(224, 240), 4, 0, 'D'), # Classe D
        (range(240, 256), 5, 0, 'E')  # Classe E
    ]
    classification = [(rng, num, 4 - num, label) for rng, num, _, label in classification]
    
    # Determinare la classe dell'indirizzo IP
    class_letter = class_ip_classful(ip, classification)
    
    # Determinare se l'indirizzo IP è di rete o di host
    ## Se è di classe A avrà il primo blocco parte rete e 3 parte host, se è di classe B avrà 2 parte rete e 2 parte host, ecc.
    is_host_network(ip, classification, class_letter)
    
    # Determinare il numero di hosts della rete
    n = int(input("Inserisci il prefisso dato dalla traccia: "))
    print(f"Per il prefisso {n}, il numero di hosts della rete è 2^(32 - {n}) = 2^{32 - n} = {2 ** (32 - n)}")

# Realizza il punto 5
def configuration_ipv4():
    # Richiedere all'utente di inserire l'indirizzo IP e la subnet mask
    has_sm = False
    ip = take_ip("Inserisci l'indirizzo IP: ", False)
    if not has_IP_prefix(str(ip)):
        SM = take_ip("Inserisci la subnet mask: ", False)
        ip += f"/{dec2bin(SM).count('1')}"
        #SM = ipaddress.ip_interface(SM)
        ip = ipaddress.ip_interface(ip)
        has_sm = True
    else:
        SM = ipaddress.ip_network(ip, strict=False).netmask
        print(f"subnet mask = {dec2bin(SM)} = {SM}/{ip.prefixlen} \n\t\t(Imposto network = {ip.prefixlen} bit a 1 e host = {32 - ip.prefixlen} bit a 0)")

    # Determinare il numero di indirizzi IP del blocco, NA e BA, e la subnet mask (se non fornita)
    compute_ip_NA_BA(ip, SM, has_sm)

# Codice Main per l'esecuzione del programma
def main():
    # Breve intro
    print("Benvenuto nel programma di calcolo per gli esercizi delle tracce riguardo gli indirizzi IP all'esame di Reti di calcolatori a.a. 2023-2024!")
    
    # Per permettere all'utente di fare altre scelte dopo aver completato una traccia
    repeat = True
    
    while repeat:
        # Stampare le possibili tracce da computare
        trace_number = print_trace_questions()
        
        if trace_number < 0 or trace_number > 6:
            print("Errore: il numero inserito non è valido.")
            continue
        
        # Eseguire la traccia scelta
        if trace_number == 1:
            classless()
            pass
        elif trace_number == 2:
            subnetting()
            pass
        elif trace_number == 3:
            supernetting()
            pass
        elif trace_number == 4:
            classful()
            pass
        elif trace_number == 5:
            configuration_ipv4()
            pass
        elif trace_number == 6:
            repeat = False
            r.main()
            break
        
        # Chiedere all'utente se vuole continuare
        print("\n\n") # Aggiungere spazi per una migliore leggibilità tra le diverse tracce
        repeat = input("Vuoi continuare ad eseguire altre tracce? (si/no) ") == "si"

if __name__ == "__main__":
    main()