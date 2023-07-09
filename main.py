from src.rsa import RSA
from src.aes import AES
from src.utils import Utils
from src.miller_rabin import MillerRabin
import hashlib
import base64
from pickle import dumps, loads


def rsa(mensagem):

    rsa = RSA()
     
    print("\n>>> Gerando as chaves publica e privada") 
    pubk, privk = rsa.generate_keys()                               # gerando as chaves publica e privada (p e q primos com no mínimo de 1024 bits)
    
    #print("$$ Chave publica: ", pubk)
    #print("$$ Chave privada: ", privk)
    
    msgCifrada = rsa.OAEPencrypt(mensagem, pubk)                    # cifrando e decifrando RSA usando OAEP
    
    #print("## Mensagem cifrada: ", msgCifrada, "\n")
    
    msgDecifrada = rsa.OAEPdecrypt(msgCifrada, privk)
    
    #print("## Mensagem decifrada: ", msgDecifrada)
    
    hash_sha3 = hashlib.sha3_256(mensagem).digest()                 # calculando os hashes da mensagem em claro usando a função de hash SHA-3 
    print(">>> Gerando o hash sha3 da menssagem")
    #print("Hash sha3: ", hash_sha3)

    msgAssinatura = rsa.OAEPencrypt(hash_sha3, pubk)                # assinatura da mensagem (cifrando o hash da mensagem) 
    print(">>> Cifrando o hash com RSA-OAEP")
    
    #print("Mensagem de assinatura: ", msgAssinatura)

    msgCodBase64 = base64.b64encode(dumps(msgAssinatura))           # colocando a mensagem de assinatura em BASE64
    print(">>> Codificando em base64")
    #print("Mensagem codificada em BASE64: ", msgCodBase64)

    msgDecodBase64 = base64.b64decode(msgCodBase64)                 # parsing do documento assinado e decifração da mensagem (de acordo com a formatação de BASE64) 
    msgAssinatura = loads(msgDecodBase64)
    print("---------------\n>>> Decodificando base64")

    hashDecod = rsa.OAEPdecrypt(msgAssinatura, privk)               # quebrando a assinatura (decifrando o hash) 
    print(">>> Decodificando o hash da mensagem com RSA-OEAP")

    # Verificação do calculo e comparando o hash do arquivo pra ver se a mensagem eh autentica 
    
    # Mensagem modificada
    #mensagem = "Outra mensagem".encode()
    hash_sha3_file = hashlib.sha3_256(mensagem).digest()
    
    if hash_sha3_file == hashDecod:
        print("[!] Verificacao realizada com sucesso")
    else:
        print("[X] Falha na verificacao")

def aes():

    filename = input('Digite o nome do arquivo em que esta contida a mensagem (o arquivo tem que esta na pasta /Testes).\n>>> ')
    
    try:
        with open(f'./Testes/{filename}', encoding="utf-8") as f:
            f.read()
    except FileNotFoundError:
        print(f'ERRO: O arquivo {filename} nao existe')
        return
    
    cifraOuDecifra=-1
    utils = Utils()
    mr = MillerRabin()

    while(cifraOuDecifra!=1 or cifraOuDecifra!=2):
        
        cifraOuDecifra = int(input("O que voce deseja fazer com a mensagem?\n1-Cifrar\n2-Decifrar\n3-Voltar\n"))

        if cifraOuDecifra == 1:
            # valor inicial de uma variavel auxiliar que sera usada na criacao de novas listas/sequencias/keystreams de chaves pra se usar na cifracao
            counter = mr.random_n_bits_number(128)

            # gerando uma chave de 128 bits a partir de um numero primo e calculando um hash pra isso pra ficar o, daquele jeito, seguranca total
            chave = mr.get_prime_n_bits(1024)
            chave = utils.hash_128_bits(chave)

            # salva a variavel auxiliar de gerar chaves e a chave gerada em um arquivo pra usar na decifracao 
            utils.write_on_file('counter.chave', f'{counter}\n{chave}\n')

            # cifrando a chave
            aes = AES(chave)

            plaintext = utils.padding(utils.read_from_file(f'Testes/{filename}', 'rb'))             # lendo o arquivo onde a mensagem esta e completando a mensagem com os bytes que faltam - ou nao - pra ser possivel aplicar AES na mensagem
            plaintext_splitted = utils.split_128bits(plaintext)                                     # quebrando a mensagem em blocos de 128 bits pra aplicar a chave de 128 bits

            result = bytes()
            for block in plaintext_splitted:
                counter_encrypted = aes.encrypt(counter)                                            # cifrando a variavel auxiliar pra usar ela no processo de cifracao da mensagem - ela gera uma lista de chaves/'keystream' (eu nao sei a traducao disso, mas a ideia eh clara) pra serem usadas nas rodadas de cifracao da mensagem completa
                
                block_integer = int.from_bytes(block, 'big')                                        # quebrando a mensagem em blocos pra cifrar pedaco por pedaco

                result += (block_integer ^ counter_encrypted).to_bytes(128 // 8, 'big')             # gerando a mensagem cifrada

                counter += 1                                                                        # sempre gerando um novo valor pra variavel auxiliar pra ela nunca tenha o mesmo valor, e consequentemente nunca gere a mesma keystream e evita que a mensagem seja quebrada por analise de frequencia

            utils.write_on_file('counter_encrypted.txt', utils.encode_to_base64(result))            # salvando a mensagem cifrada em um arquivo pra decifrar depois

            print("Mensagem cifrada. O resultado esta no arquivo 'counter_encrypted.txt'\n")
        
        elif cifraOuDecifra == 2:
            with open('counter.chave', 'r') as file:
                # pegando a chave e a variavel auxiliar a partir de um arquivo pra ajudar na decifracao                                                  
                counter = int(file.readline())
                chave = int(file.readline())

            # cifrando a chave
            aes = AES(chave)

            # quebrando a mensagem cifrada em blocos de 128 bits pra decifrar pedaco por pedaco
            blocks = utils.split_128bits(utils.decode_from_base64(utils.read_from_file('counter_encrypted.txt')))

            plaintext_decrypted = bytes()

            for block in blocks:
                counter_encrypted = aes.encrypt(counter)                                # cifrando a variavel auxiliar pra usar ela no processo de cifracao da mensagem - ela gera uma lista de chaves/'keystream' (eu nao sei a traducao disso, mas a ideia eh clara) pra serem usadas nas rodadas de cifracao da mensagem completa

                answer_result = counter_encrypted ^ int.from_bytes(block, 'big')        # refazendo o XOR feito no processo de cifracao pra deicfrar a mensagem

                plaintext_decrypted += answer_result.to_bytes(128//8, 'big')            # criando a resposta

                counter += 1                                                            # adicionando +1 unidade na variavel auxiliar pra poder decifrar a mensagem com os valores utilizados no processo de cifracao

            # tirando os blocos de bytes que foram adicionados no texto original pra que ele pudesse ser cifrado com AES
            plaintext_decrypted = utils.remove_padding(plaintext_decrypted)

            with open('output.txt', 'wb') as file:
                # gravando a mensagem decifrada em um arquivo
                file.write(plaintext_decrypted)
            
            print("Mensagem decifrada. O segredo esta em 'output.txt'\n")
                    
        elif cifraOuDecifra == 3:
        
            return
        else:
            print("Opcao Invalida\n")

def main():

    escolha = -1

    while escolha!=1 or escolha!=2 or escolha !=3:

        escolha = int(input("Qual cifra voce deseja testar?\n1 - RSA\n2 - AES\n3 - Sair\n"))

        if escolha == 1:
            # codificacao em RSA
                                
            message = input("Insira uma mensagem para ser cifrada: ").encode()

            rsa(message)
            escolha=-1
        elif escolha == 2:
            # codificacao em AES                                                     
            
            aes()
            escolha=-1
        elif escolha == 3:                                                      
            # sair do programa

            exit()
        else:          
            # usuario com entrada invalida                                                         
            
            print("Opcao Invalida.\n")

if __name__ == "__main__":
    main()
