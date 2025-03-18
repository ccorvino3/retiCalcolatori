import reti as r
from utils import format_bits
import os
import sys


# Funzione che stampa le possibili tracce da computare
def print_trace_questions():
    print("\n\n1. Convertire da decimale a binario.")
    print("2. Convertire da binario a decimale.")
    print("3. Torna al menu principale.")
    
    # Richiedere all'utente di scegliere una traccia
    return int(input("Inserisci il numero dell'esercizio da computare: "))

# Funzione che controlla se il numero inserito è positivo
def check_message():
    check = False
    while not check:
        n = int(input("Inserire un numero decimale positivo: "))
        
        if n < 0:
            print("Errore: il numero deve essere positivo.")
        else:
            return n

# Funzione che controlla se il numero binario inserito è corretto
def check_binary():
    check = False
    while not check:
        b = input("Inserire un numero binario: ")
        
        if not all(char in ['0', '1'] for char in b):
            print("Errore: il numero deve contenere solo 0 e 1.")
        else:
            return b

# Funzione che converte un numero decimale in binario su 8 bit
def dec2bin():
    repeat = True
    while repeat:    
        # Richiedere all'utente di inserire un numero decimale
        n = check_message()
        
        # Convertire il numero decimale in binario
        print(f"Il numero decimale {n} convertito in binario è: {bin(n)[2:]}")
        
        # Chiedere all'utente se vuole continuare
        repeat = input("Vuoi continuare ad eseguire altre conversioni? (si/no) ") == "si"

# Funzione che converte un numero binario in decimale
def bin2dec():
    repeat = True
    while repeat:    
        # Richiedere all'utente di inserire un numero binario
        b = check_binary()
        
        # Convertire il numero da binario a decimale
        print(f"Il numero binario {b} convertito in decimale è: {int(b, 2)}")
        
        # Chiedere all'utente se vuole continuare
        repeat = input("Vuoi continuare ad eseguire altre conversioni? (si/no) ") == "si"

# Codice Main per l'esecuzione del programma
def main():
    # Breve intro
    print("Benvenuto nel programma di calcolo per gli esercizi delle tracce riguardo la conversione di numeri da decimale a binario e viceversa all'esame di Reti di calcolatori a.a. 2023-2024!")
    
    repeat = True
    
    while repeat:
        # Stampare le possibili tracce da computare
        trace_number = print_trace_questions()
        
        if trace_number < 0 or trace_number > 3:
            print("Errore: il numero inserito non è valido.")
            continue
        
        # Eseguire la traccia scelta
        if trace_number == 1:
            dec2bin()
            pass
        elif trace_number == 2:
            bin2dec()
            pass
        elif trace_number == 3:
            repeat = False
            r.main()
            break
        
        # Chiedere all'utente se vuole continuare
        print("\n\n") # Aggiungere spazi per una migliore leggibilità tra le diverse tracce
        repeat = input("Vuoi continuare ad eseguire altre conversioni? (si/no) ") == "si"

# Eseguire il programma
if __name__ == "__main__":
        main()