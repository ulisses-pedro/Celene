import math;

primeira = input("Insira a primeira palavra: ")
segunda = input("Insira a segunda palavra: ")

def anagrama (primeira, segunda):
    listap = list(primeira)
    listas = list(segunda)
    
    for anag in primeira:
        if anag in listas:
            listap.remove(anag)
            listas.remove(anag)
            
    return len(listap) + len(listas)

print (anagrama (primeira, segunda))