from src.rsa import RSA
from src.aes import AES
import hashlib
import base64
from pickle import dumps, loads

def rsa(message):
    rsa = RSA()
     
    # Parte II - Geração de chaves e cifra RSA ----------------------------------- #
    # a) Geração de chaves (p e q primos com no mínimo de 1024 bits) testando primalidade com Miller-Rabin
    print("\n>>>> Gerando as chaves publica e privada...")
    public_key, private_key = rsa.generate_keys()
    
    print("\n>>>> Chave pública: ", public_key)
    print("\n>>>> Chave privada: ", private_key)
    
    # b e c) Cifração/decifração assimétrica RSA usando OAEP
    encrypted_message = rsa.OAEPencrypt(message, public_key)
    
    # print("\n>>>> Mensagem cifrada: ", encrypted_message, "\n")
    
    decrypted_message = rsa.OAEPdecrypt(encrypted_message, private_key)
    
    print("\n>>>> Mensagem decifrada: ", decrypted_message.decode())
    
    # Parte III - Assinatura RSA ------------------------------------------------- #
    # a) Cálculo de hashes da mensagem em claro (função de hash SHA-3)
    # TODO: esse item realmente é necessário? 
    hash_sha3 = hashlib.sha3_256(message).digest() 
    print("\n>>>> Gerando o Hash sha3 da menssagem...")
    print("\n>>>> Hash sha3: ", hash_sha3)

    # b) Assinatura da mensagem (cifração do hash da mensagem)
    signature_message = rsa.OAEPencrypt(hash_sha3, public_key)  
    print("\n>>>> Cifrando o hash com RSA-OAEP...")
    
    # print("\n>>>> Assinatura da mensagem: ", signature_message)

    # c) Formatação do resultado (caracteres especiais e informações para verificação em BASE64)
    b64_message_encoded = base64.b64encode(dumps(signature_message))
    print("\n>>>> Codificando em BASE64...")
    print("\n>>>> Mensagem codificada em BASE64: ", b64_message_encoded)

    # Parte IV - Verificação ----------------------------------------------------- #
    # a) Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64)
    b64_message_decoded = base64.b64decode(b64_message_encoded) 
    signature_message = loads(b64_message_decoded)
    print("\n>>>> Decodificando base64...")

    # b) Decifração da assinatura (decifração do hash)
    decrypted_hash = rsa.OAEPdecrypt(signature_message, private_key) 
    print("\n>>>> Decodificando o hash da mensagem com RSA-OEAP...")

    # c) Verificação (cálculo e comparação do hash do arquivo) 
    # Mensagem modificada
    #message = "Outra mensagem".encode()
    hash_sha3_file = hashlib.sha3_256(message).digest()
    
    if hash_sha3_file == decrypted_hash:
        print("\n>>>> Verificação realizada com sucesso!\n")
    else:
        print("\n>>>> Falha na verificação!\n")

def aes(message):
    aes = AES()

    chave = "5468617473206D79204B756E67204675" # isso aqui eh uma chave de 128 bits em haxadecimal- traducao "thats my kung fu"
    cifraOuDecifra = int(input("Voce deseja cifrar ou decrifrar uma mensagem?\n0 - Cifrar\n1 - Decifrar\n"))

    if cifraOuDecifra == 1:
        chave = input("Insira a chave de decifracao:\n")

    # chave = base64.b64encode(chave.encode())

    message = message.decode('ascii')
    # chave = chave.decode('ascii')

    

    cipher = aes.CifraDecifra(message, chave, cifraOuDecifra) # em tese, o 'estado' eh a mensagem cifrada

    for e in cipher:
        print(e)

def main():
    message = input("Insira uma mensagem para ser cifrada: ").encode()

    message = base64.b64encode(message)

    # rsa = RSA()
    # aes = AES()

    escolha = -1

    while escolha!=1 or escolha!=2:
        escolha = int(input("Como voce deseja cifrar sua mensagem?\n1 - RSA\n2 - AES\n3 - Sair\n"))

        if escolha == 1: # funciona
            rsa(message)
        elif escolha == 2: # testar depois
            aes(message)
        elif escolha == 3:
            exit()
        else:
            print("Opcao Invalida.\n")

if __name__ == "__main__":
    main()
