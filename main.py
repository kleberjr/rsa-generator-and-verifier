from src.rsa import RSA
from src.aes import AES
import hashlib
import base64
from pickle import dumps, loads

def rsa(message):

    rsa = RSA()
     
    print("\nGerando as chaves publica e privada...") # 1.a) geração de chaves (p e q primos com no mínimo de 1024 bits)
    public_key, private_key = rsa.generate_keys()
    
    #print("Public key: ", public_key)
    #print("Private key: ", private_key)
    
    encrypted_message = rsa.OAEPencrypt(message, public_key) # 1.b) cifração/decifração assimétrica RSA usando OAEP
    
    #print("Encrypted message: ", encrypted_message, "\n")
    
    decrypted_message = rsa.OAEPdecrypt(encrypted_message, private_key)
    
    #print("Decrypted message: ", decrypted_message)
    
    hash_sha3 = hashlib.sha3_256(message).digest() # 2.a) calculo de hashes da mensagem em claro (função de hash SHA-3) 
    print("Gerando o hash sha3 da menssagem...")
    #print("Hash sha3: ", hash_sha3)

    signature_message = rsa.OAEPencrypt(hash_sha3, public_key) # 2.b) assinatura da mensagem (cifração do hash da mensagem) 
    print("Cifrando o hash com RSA-OAEP...")
    
    #print("Signature message: ", signature_message)

    b64_message_encoded = base64.b64encode(dumps(signature_message)) # 2.c) formatação do resultado (caracteres especiais e informações para verificação em BASE64)
    print("Codificando em base64...")
    #print("BASE64 encoded message: ", b64_message_encoded)

    b64_message_decoded = base64.b64decode(b64_message_encoded) # 3.a) Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64) 
    signature_message = loads(b64_message_decoded)
    print("---------------\nDecodificando base64...")

    decrypted_hash = rsa.OAEPdecrypt(signature_message, private_key) # 3.b) Decifração da assinatura (decifração do hash) 
    print("Decodificando o hash da mensagem com RSA-OEAP...")

    # 3.c) Verificação (cálculo e comparação do hash do arquivo) 
    
    # Mensagem modificada
    #message = "Outra mensagem".encode()
    hash_sha3_file = hashlib.sha3_256(message).digest()
    
    if hash_sha3_file == decrypted_hash:
        print("Verificação realizada com sucesso")
    else:
        print("Falha na verificação")

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
