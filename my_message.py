import reti as r
from utils import format_bits, is_power_of_two


# Funzione per stampare le possibili tracce da computare
def print_trace_questions():
    print("\n\n1. Determinare il codice di Hamming del seguente byte 'm'. Quindi, illustrare cosa succede se a destinazione varia il valore di 'un bit'.")
    print("2. Determinare l'Internet Checksum del seguente messaggio formato da 32 bit: 'm'. Inoltre, determinare cosa succede a destinazione se dovesse cambiare 'un bit'")
    print("3. Determinare il bit di parità di un messaggio 'm' di 8 bit.")
    print("4. Torna al menu principale.")
    
    # Richiedere all'utente di scegliere una traccia
    return int(input("Inserisci il numero della traccia da computare: "))

''' Funzioni per i messaggi: Codice di Hamming, Bit di parità e Internet Checksum '''

# Funzione per calcolare inserire da tastiera il messaggio e effettua dei controlli sull'input
def check_message(len_max):
    check = False
    while not check:
        m = input("Inserire il messaggio formato da " + str(len_max) + " bit: ").replace(" ", "")
    
        if len(m) != len_max:
            print("Il messaggio inserito non ha la lunghezza corretta. Riprovare.")
        elif not all(char in ['0', '1'] for char in m):
            print("Errore: il codice deve contenere solo 0 e 1.")
        else:
            return m

# Funzione per cambiare un bit del messaggio
def change_message(m, bit_err):
    if not int(bit_err) == 0:
        # Converti la stringa in una lista per poter modificare i singoli caratteri
        m = list(m)
        m[int(bit_err) - 1] = '1' if m[int(bit_err) - 1] == '0' else '0'
        
        # Riconverti la lista in una stringa
        m = ''.join(m)
        
        return m

# Funzione per calcolare la somma binaria tra due messaggi
def binary_sum(A, B):
    # Calcola la somma binaria tra A e B
    sum = bin(int(A, 2) + int(B, 2))[2:].zfill(16)
    
    # Se si ottiene un riporto (len == 17), sommarlo al risultato
    if len(sum) == 17:  # Se la lunghezza è 17, c'è un riporto
        carry = int(sum[0], 2)  # Il primo bit è il riporto
        sum_without_carry = sum[1:]  # La parte senza il riporto
        sum_carry = bin(int(sum_without_carry, 2) + carry)[2:].zfill(16)  # Somma il riporto
        
        # Stampa il risultato con il riporto
        print(f"\t{format_bits(A)} + {format_bits(B)} = {format_bits(sum_without_carry)} + {carry} = {format_bits(sum_carry)}")
        return sum_carry
    else:
        # Stampa il risultato senza riporto
        print(f"\t{format_bits(A)} + {format_bits(B)} = {format_bits(sum)}")
        return sum

# Funzione per negare tutti i bit di un messaggio
def not_bits(bits):
    return ''.join(['1' if bit == '0' else '0' for bit in bits])

# Funzione per calcolare l'xor tra tutti i bit di un messaggio
def xor_all_bits(bit_sequence: str) -> int:
    # Converti il primo bit in intero
    result = int(bit_sequence[0])
    output = f"\t{bit_sequence[0]}"  # Inizia con il primo bit
    
    # Esegui l'operazione XOR con ciascun bit successivo
    for bit in bit_sequence[1:]:
        output += f" XOR {bit}"
        result ^= int(bit)
    
    # Aggiungi il risultato finale all'output
    output += f" = {result}"
    
    # Stampa l'output su una sola riga
    print(output)
    
    return result

# Printa la lista di bit con il messaggio specificato in input
def print_list_bits(hamming_code, msg):
    result = msg
    for bit in hamming_code:
        result += str(bit) + " "
    print(result)

''' Funzioni per computare le tracce '''

# Funzione per dividere il messaggio in 2 messaggi da 16 bit e calcolare la somma binaria tra i due
def split_sum(m):
    # Dividere il messaggio in due messaggi da 16 bit
    A = m[:16]
    B = m[16:]
    
    # Calcolare la somma dei due messaggi
    return binary_sum(A, B)

# Funzione per calcolare l'Internet Checksum = NOT(Somma(A, B))
def compute_IC(m):
    # Calcolare la somma dei bit del messaggio
    sum = split_sum(m)
    
    # Calcolare Internet Checksum = NOT(Somma)
    return sum, not_bits(sum)

# Funzione per calcolare i bit di parità del codice di Hamming
def get_parity_bits(m):
    n = len(m)
    # Calcola il numero di bit di parità necessari
    r = 0
    while (2 ** r) < (n + r + 1):
        r += 1

    # Creazione del messaggio finale con spazi per i bit di parità
    hamming_code = []
    j = 0
    for i in range(1, n + r + 1):
        if i == (2 ** j):
            hamming_code.append(0)  # Posizione per bit di parità
            j += 1
        else:
            hamming_code.append(m[i - 1 - j])  # Bit di dati

    # Calcola i bit di parità
    for i in range(r):
        parity_index = 2 ** i
        parity_value = 0
        controlled_bits = []
        
        # Calcola l'XOR dei bit controllati dal bit di parità
        for k in range(parity_index, len(hamming_code) + 1):
            if k & parity_index == parity_index:  # Controlla se il bit corrente è controllato da h_i
                controlled_bits.append(hamming_code[k - 1])
                parity_value ^= hamming_code[k - 1]
        hamming_code[parity_index - 1] = parity_value
        
        # Stampa il valore di h_i
        print(f"\th{parity_index} = {' xor '.join(map(str, controlled_bits[1:]))} = {parity_value}")
    return hamming_code

# Funzione per rilevare l'errore nel codice di Hamming
def detect_error(hamming_code):
    r = 0
    while (2 ** r) <= len(hamming_code):
        r += 1

    error_position = 0
    error_bits = []

    for i in range(r):
        parity_index = 2 ** i
        parity_value = 0
        controlled_bits = []
        
        for k in range(1, len(hamming_code) + 1):
            if k & parity_index == parity_index:  # Controlla se il bit corrente è controllato da h_i
                controlled_bits.append(hamming_code[k - 1])
                parity_value ^= hamming_code[k - 1]

        # Stampa l'output dettagliato
        print(f"\th{parity_index} = {' xor '.join(map(str, controlled_bits))} = {parity_value} ")

        if parity_value != 0:
            error_position += parity_index
            error_bits.append('1')  # Bit errato
        else:
            error_bits.append('0')  # Nessun errore
    
    # Stampa la rappresentazione binaria degli errori
    error_bits.reverse()  # Inverti per mostrare dall'ultimo al primo
    error_bits_str = ''.join(error_bits)
    print(f"\t{error_bits_str} (in binario) = {error_position} (posizione del bit errato nel codice di hamming)")

    return error_position

# Funzione per il punto 1
def hamming():
    # Input del messaggio
    message = input("Inserisci il messaggio binario (es. 1011): ")
    message_bits = [int(bit) for bit in message]

    # Calcola i bit di parità e crea il codice di Hamming
    print("Sorgente: ")
    hamming_code = get_parity_bits(message_bits)
    print(f"\tCodice di Hamming: {''.join(map(str, hamming_code))}")

    # Chiede all'utente se cambiare un bit
    print("Destinazione: ")
    change = input("\tVuoi cambiare un bit nel codice di Hamming? (s/n): ")
    if change.lower() == 's':
        bit_position = int(input(f"\tInserisci la posizione del bit da cambiare (1-{len(hamming_code)}): ")) - 1
        # Cambia il bit (not)
        hamming_code[bit_position] ^= 1
        print(f"\tCodice di Hamming dopo la modifica: {''.join(map(str, hamming_code))}")

    # Rileva l'errore
    error_position = detect_error(hamming_code)
    if (error_position > 0):
        if not is_power_of_two(int(error_position)):
            print(f"\tErrore trovato nella posizione: {error_position}. Essendo un bit controllato => NOT(m{error_position})")
        else:
            print(f"\tErrore trovato nella posizione: {error_position}. Essendo un bit controllore => viene ignorato in quanto il messaggio è arrivato correttamente a destinazione.")
    else:
        print("\tNessun errore a destinazione.")

# Funzione per il punto 2
def internet_checksum():
    # Chiedere all'utente di inserire il messaggio
    m = check_message(32)
    
    # Sorgente:
    ## Calcolare IC = NOT(Somma)
    print("Sorgente:")
    sum, IC = compute_IC(m)
    print(f"\tIC = NOT({format_bits(sum)}) = {format_bits(IC)}")
    
    # Destinazione:
    print("Destinazione:")
    bit_err = input(f"\tInserire 0 se non cambia nessun bit oppure un bit compreso tra 1 e {len(m)} per verificare cosa succede a destinazione: ")
    ## Cambiare il bit errato
    change_message(m, bit_err)
    ## Stampa il messaggio
    print(f"\tm = {format_bits(m)}")
    ## Calcolare la somma tra i due messaggi da 16 bit
    sum = split_sum(m)
    ## Calcolare la somma tra sum+riporto e IC
    sum = binary_sum(sum, IC)
    sum_format = format_bits(sum)
    ## NOT(m + IC) == 0 => messaggio corretto, else messaggio errato
    sum_not = not_bits(sum)
    sum_not_format = format_bits(sum_not)
    print(f"\t=> NOT({sum_format}) = {sum_not_format}")
    if all(bit == '0' for bit in sum_not):
        print("\tIl messaggio è arrivato correttamente a destinazione.")
        print(f"\tMessaggio corretto (perché {sum_not_format} = 0)")
    else:
        print(f"\tMessaggio non corretto (perché {sum_not_format} != 0)")

# Funzione per il punto 3
def parity_bit():
    # Richiedere all'utente di inserire il messaggio
    m = check_message(8)
    print(f"m = {format_bits(m)}")
    
    # Sorgente:
    print("Sorgente:")
    ## Calcolare il bit di parità
    parity = xor_all_bits(m)
    m = m + str(parity)
    print(f"\t=> m = {format_bits(m)}")
    
    # Destinazione:
    print("Destinazione:")
    bit_err = input(f"\tInserire 0 se non cambia nessun bit oppure i bit errati (compreso tra 1 e {len(m)}) per verificare cosa succede a destinazione: ").replace(" ", "")
    ## Cambiare i bit errati
    if (bit_err != "0"):
        for i in range(len(bit_err)):
            m = change_message(m, int(bit_err[i]))
    print(f"\t=> m = {format_bits(m)}")
    ## Xor con il bit errato
    if (xor_all_bits(m) == 0):
        if (len(bit_err) %2 == 1):
            print(f"\tIl messaggio è arrivato correttamente a destinazione.")
        else:
            print(f"\tA destinazione l'xor in {format_bits(m)} è 0, ma il metodo fallisce perché sono cambiati nel messaggio i bit '{' '.join(bit_err)}', infatti questo metodo funziona quando il numero di bit errati è dispari o è 0.")
    else:
        print(f"\tIl messaggio non è arrivato correttamente a destinazione.")

# Codice Main per l'esecuzione del programma
def main():
    # Breve intro
    print("Benvenuto nel programma di calcolo per gli esercizi delle tracce riguardo il codice di Hamming, il bit di parità e l'internet checksum all'esame di Reti di calcolatori a.a. 2023-2024!")
    
    repeat = True
    
    while repeat:
        # Stampare le possibili tracce da computare
        trace_number = print_trace_questions()
        
        if trace_number < 1 or trace_number > 4:
            print("Errore: il numero inserito non è valido.")
            continue
        
        # Eseguire la traccia scelta
        if trace_number == 1:
            hamming()
            pass
        elif trace_number == 2:
            internet_checksum()
            pass
        elif trace_number == 3:
            parity_bit()
            pass
        elif trace_number == 4:
            repeat = False
            r.main()
            break
        
        # Chiedere all'utente se vuole continuare
        print("\n\n") # Aggiungere spazi per una migliore leggibilità tra le diverse tracce
        repeat = input("Vuoi continuare ad eseguire altre tracce? (si/no) ") == "si"

# Eseguire il programma
if __name__ == "__main__":
    main()