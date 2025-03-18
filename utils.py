
# Funzione che ritorna una stringa con uno spazio ogni 4 bit per una migliore leggibilità
def format_bits(bits):
    # Aggiunge uno spazio ogni 4 bit
    return ' '.join([bits[i:i+4] for i in range(0, len(bits), 4)])

# Funzione che calcola la potenza di 2 più vicina al numero dato o converte il numero in una potenza di 2
def power_of_two(n):
    # Trova la potenza di 2 più vicina o comunque converte il numero in una potenza di 2
    index = 1
    power = 1
    while power < n:
        power = 2 ** index
        if power < n:
            index += 1
    
    return index

# Funzione che determina se un numero è una potenza di 2
def is_power_of_two(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0
