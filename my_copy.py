import cv2
import pytesseract
from graphviz import Digraph
import os


def process_image(image_path):
    # Carica l'immagine
    image = cv2.imread(image_path)
    if image is None:
        print("Impossibile caricare l'immagine.")
        return

    # Pre-processamento dell'immagine per OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Riconoscimento del testo (nomi delle cartelle)
    text = pytesseract.image_to_string(thresh)
    print("Text detected:", text)

    # Identificazione dei contorni (potenziali nodi)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Creazione di un grafo
    dot = Digraph(comment='Generated Graph', format='png')

    # Parsing e creazione del grafo dai nodi
    node_names = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        node_name = f"Node{i}"
        dot.node(node_name, text)  # Aggiungi il testo estratto come etichetta del nodo
        node_names.append(node_name)

        # Logica per connettere i nodi secondo la struttura osservata
        # Qui puoi implementare logiche più complesse per determinare le connessioni

    # Creare collegamenti tra i nodi se necessario
    for i in range(1, len(node_names)):
        dot.edge(node_names[i - 1], node_names[i])  # Collega i nodi in ordine

    # Salva il grafo generato
    file_name = os.path.splitext(os.path.basename(image_path))[0]  # Ottieni il nome del file senza l'estensione
    output_path = os.path.join(f'image_path\graph', f'graph_{file_name}')  # Nome del file con "graph_" come prefisso
    dot.render(output_path, view=True)

def main():
    # Path dell'immagine, dall'utente
    image_path = input("Inserisci il path assoluto dell'immagine: ")
    
    # Processa l'immagine
    process_image(image_path)

if __name__ == "__main__":
    main()