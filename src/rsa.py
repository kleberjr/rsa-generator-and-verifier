from src.miller_rabin import MillerRabin
from .utils import Utils
import math
import struct
import hashlib
import os

funcao_hash = hashlib.sha256
COMPRIMENTO_HASH = funcao_hash().digest_size

class RSA():
    def __init__(self) -> None:
        self.utils = Utils()
        self.k = int(1024/8)

    # Essa função gera os expoentes de encriptação, decriptação
    # e o módulo.
    def gerar_chaves(self):      
        miller_rabin = MillerRabin()

        # Gera os 2 primos necessários testando a primalidade com Miller-Rabin  
        primo_p = miller_rabin.gera_primo()
        primo_q = miller_rabin.gera_primo()

        # O módulo que eventualmente vai ser utilizado no processo de cifração/decifração
        modulo = primo_p * primo_q
        
        # Resultado da função totiente; quantidade de coprimos do módulo
        phi = (primo_p - 1) * (primo_q - 1)
        
        # Procura o expoente de encriptação e
        e = 65001                               # Começamos com um valor inicial para e, mas que não seja tão pequeno

        while True:
            if math.gcd(e, phi) == 1:           # Verificamos se e é coprimo com phi
                break
        
            e += 2                              # Incrementamos e por 2 para verificar apenas valores ímpares
        
        # Ao invés de fazermos um trabalho mais pesado de procura do expoente de decifração
        # utilizando o Algoritmo Euclidiano normal, podemos encurtar o caminho utilizando 
        # o Algoritmo Euclidiano Extendido.
        d = self.utils.euclideano_extendido(e, phi)[1]

        # Se d < 0, então ele é o inverso multiplicativo modular de e (mod phi),
        # então o ajustamos para um múltiplo inteiro de phi.
        if (d < 0):
            d += phi        

        return e, d, modulo

    # Essa função aplica o algoritmo RSA.
    def aplicar_rsa(self, mensagem, chave, modulo):
        resultado = []

        for letra in mensagem:
            resultado.append(pow(letra, chave, modulo))   # letra_cifrada = letra^chave (mod n)
        
        return resultado

    def gerar_bloco_de_dados(self, l_hash, mensagem):
        padding = bytearray()

        tamanho_completo = self.k - len(mensagem) - (2 * COMPRIMENTO_HASH) - 2 

        for i in range(tamanho_completo):
            padding.append(0) 
        
        return l_hash + padding + b'\x01' + mensagem

    # Essa função cifra uma mensagem utilizando o método OAEP,
    # juntamente com o algoritmo RSA.
    def cifrar_com_oaep(self, mensagem, chave_publica, modulo, rotulo=""):
        rotulo = rotulo.encode()                        # Transforma o rótulo em bytes                             
        
        tamanho_limite = self.k - 2 * COMPRIMENTO_HASH - 2    # Cálcula o tamanho limite

        if (len(mensagem) > tamanho_limite):
            raise ValueError("Mensagem é muito longa para ser codificada usando OAEP.")

        hash_rotulo = funcao_hash(rotulo).digest()        # Aplica o hash ao rótulo usando sha256

        # Gerar uma string de preenchimento e realiza
        # as concatenações com hash_rotulo, o byte único e
        # a mensagem
        bloco_de_dados = self.gerar_bloco_de_dados(hash_rotulo, mensagem)

        # Gera uma semente e uma máscara aleatórias
        # com tamanhos apropriados
        seed = os.urandom(COMPRIMENTO_HASH)                                               # Gera semente
        mascara_bloco = self.mgf1(seed, self.k - COMPRIMENTO_HASH - 1, funcao_hash)    # Gera máscara com mgf1

        # Aplica a máscara ao bloco de dados, gera
        # uma máscara de tamanho h_len pra semente e
        # aplica a mascara na semente também
        bloco_mascarado = bytes(self.utils.xor(bloco_de_dados, mascara_bloco))      # Aplica máscara no bloco com xor
        mascara_seed = self.mgf1(bloco_mascarado, COMPRIMENTO_HASH, funcao_hash)       # Gera máscara da seed
        seed_mascarada = bytes(self.utils.xor(seed, mascara_seed))                  # Aplica máscara na seed com xor

        # A mensagem codificada (com preenchimento) é sempre o 
        # byte 0x00 concatenado com a semente mascarada e 
        # o bloco de dados mascarado
        mensagem_cifrada = b'\x00' + seed_mascarada + bloco_mascarado
        mensagem_cifrada = self.aplicar_rsa(mensagem_cifrada, chave_publica, modulo)

        return mensagem_cifrada

    # Essa função decifra uma mensagem codificada utilizando o método OAEP,
    # juntamente com o algoritmo RSA.
    def decifrar_com_oaep(self, mensagem_codificada, chave_privada, modulo, rotulo=""):        
        rotulo = rotulo.encode()

        # Como a mensagem vem cifrada de acordo com RSA, primeiro temos 
        # que decifrá-la de acordo.
        mensagem_codificada = self.aplicar_rsa(list(mensagem_codificada), chave_privada, modulo)
        hash_rotulo = funcao_hash(rotulo).digest()                            # Hasheamento do rótulo usando o algoritmo sha256

        # Temos que pegar as partes distintas da mensagem concatenadas 
        # anteriormente
        seed_mascarada = bytes(mensagem_codificada[1 : COMPRIMENTO_HASH + 1])     # Pega a seed com a mask
        bloco_mascarado = bytes(mensagem_codificada[COMPRIMENTO_HASH + 1:])       # Pega o bloco com a mask

        # Gerar a máscara da semente que foi utilizada anteriormente e
        # então recupera a semente
        mascara_seed = self.mgf1(bloco_mascarado, COMPRIMENTO_HASH, funcao_hash)
        seed = bytes(self.utils.xor(seed_mascarada, mascara_seed))

        # Gera a máscara do bloco de dados que foi usada anteriormente
        # e então recupera o bloco de dados
        mascara_bloco = self.mgf1(seed, self.k - COMPRIMENTO_HASH - 1, funcao_hash)
        bloco_de_dados = bytes(self.utils.xor(bloco_mascarado, mascara_bloco))

        hash_rotulo_gerado = bloco_de_dados[:COMPRIMENTO_HASH]                         # Pega o hash contido no bloco resgatado

        # Se os hashs  coincidirem, então a mensagem é válida
        if hash_rotulo_gerado != hash_rotulo:
            raise ValueError("A mensagem decodificada possui um hash de rótulo incorreto.")
        
        # Acha onde a mensagem começa
        inicio_mensagem = COMPRIMENTO_HASH + bloco_de_dados[COMPRIMENTO_HASH:].find(b'\x01') + 1
        mensagem = bloco_de_dados[inicio_mensagem:]
        
        return mensagem

    # Essa função implementa a função geradora de máscara OAEP: a MGF1.
    def mgf1(self, seed, tamanho_mascara, funcao_hash):        
        tamanho_limite = 2**32 * COMPRIMENTO_HASH

        if (tamanho_mascara > tamanho_limite):
            raise ValueError("Máscara muito longa.")
        
        T = bytearray()

        for contador in range(math.ceil(tamanho_mascara / COMPRIMENTO_HASH)):
            c = struct.pack(">I", contador)
            T += funcao_hash(seed + c).digest()
        
        return T[:tamanho_mascara]
