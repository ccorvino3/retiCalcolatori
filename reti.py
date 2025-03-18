import my_address as addr
import my_conversion as conv
import my_copy as copy
import my_message as msg


def print_trace():
    print("\n\nLe tracce disponibili riguardano tipologie come:")
    print("\t1. Codice di Hamming, Bit di parità e Internet Checksum")
    print("\t2. Supernetting, Subnetting, Classless (CIDR), Classful")
    print("\t3. Comando COPY")
    print("\t4. Conversioni di numeri da decimale a binario e viceversa")
    print("\t0. Chiude il programma.")
    
    return int(input("Quale tipologia di traccia vuoi eseguire? "))

# Codice Main per l'esecuzione del programma
def main():
    # Breve intro
    print("Benvenuto nel programma di calcolo che computa gli esercizi delle tracce per l'esame di Reti di calcolatori a.a. 2023-2024!")
    print("Premetto che alcuni controlli sugli input non sono stati effettuati per mancanza di tempo. Quindi, si prega di inserire"
          + " valori corretti per evitare errori e di non snervarsi se ciò accada. Grazie.")
    
    repeat = True
    
    while repeat:
        # Stampare le possibili tracce da computare
        trace_number = print_trace()
        
        if trace_number < 0 or trace_number > 4:
            print("Errore: il numero inserito non è valido.")
            continue
        
        # Eseguire la traccia scelta
        if trace_number == 1:
            msg.main()
            pass
        elif trace_number == 2:
            addr.main()
            pass
        elif trace_number == 3:
            print("Non ancora implementata. Ci scusiamo per il disagio.")
            #copy.main()
            pass
        elif trace_number == 4:
            conv.main()
            pass
        elif trace_number == 0:
            print("Grazie per aver utilizzato il programma!")
            repeat = False
            break
        
        # Chiedere all'utente se vuole continuare
        print("\n\n") # Aggiungere spazi per una migliore leggibilità tra le diverse tracce
        repeat = input("Vuoi continuare ad eseguire altre tracce? (si/no) ") == "si"

# Eseguire il programma
if __name__ == "__main__":
    main()