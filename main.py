import hashlib, base64
from src.rsa import RSA
from src.aes import AES
from src.utils import Utils
from pickle import dumps, loads
from src.miller_rabin import MillerRabin

def rsa(mensagem):
    # A mensagem já vem encodada UTF-8, resolvendo a questão dos caracteres especiais.
    rsa = RSA()
     
    # Parte II - Geração de chaves e cifra RSA ----------------------------------- #
    # a) Geração de chaves (p e q primos com no mínimo de 1024 bits) testando 
    # primalidade com Miller-Rabin
    print("\n>>>> Gerando as chaves publica e privada...")
    chave_publica, chave_privada, modulo = rsa.gerar_chaves()
    
    print("$$ Chave publica: ", chave_publica)
    print("$$ Chave privada: ", chave_privada)
    
    # b e c) Cifração/decifração assimétrica RSA usando OAEP
    msgCifrada = rsa.cifrar_com_oaep(mensagem, chave_publica, modulo)
    msgDecifrada = rsa.decifrar_com_oaep(msgCifrada, chave_privada, modulo).decode()
    
    # print("## Mensagem cifrada: ", msgCifrada, "\n")
    # print("## Mensagem decifrada: ", msgDecifrada)
    
    # Parte III - Assinatura RSA ------------------------------------------------- #
    # O digest retorna o hash de fato
    hash_sha3 = hashlib.sha3_256(mensagem).digest()
    print(">>>> Gerando o hash sha3 da menssagem")

    # print("Hash sha3: ", hash_sha3)

    # a) Assinatura da mensagem (cifração do hash da mensagem)
    msgAssinatura = rsa.cifrar_com_oaep(hash_sha3, chave_publica, modulo)
    print(">>>> Cifrando o hash com RSA-OAEP")
    
    # print("Mensagem de assinatura: ", msgAssinatura)

    # b) Formatação do resultado (caracteres especiais e informações para 
    # verificação em BASE64)
    msgCodBase64 = base64.b64encode(dumps(msgAssinatura))
    print(">>>> Codificando em base64")
    # print("Mensagem codificada em BASE64: ", msgCodBase64)

    # Parte IV - Verificação ----------------------------------------------------- #
    # a) Parsing do documento assinado e decifração da mensagem (de acordo com a 
    # formatação usada, no caso BASE64)
    msgDecodBase64 = base64.b64decode(msgCodBase64)
    msgAssinatura = loads(msgDecodBase64)
    print(">>>> Decodificando base64")

    # b) Decifração da assinatura (decifração do hash)
    hashDecod = rsa.decifrar_com_oaep(msgAssinatura, chave_privada, modulo)     # Quebrando a assinatura (decifrando o hash) 
    print(">>>> Decodificando o hash da mensagem com RSA-OEAP")

    # c) Verificação (cálculo e comparação do hash do arquivo) 
    
    # Mensagem modificada para falha na verificação
    # mensagem = "Outra mensagem".encode()
    
    if hash_sha3 == hashDecod:
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
