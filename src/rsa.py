from .generate_prime import GeneratePrime
from .utils import Utils
import math
import struct
import hashlib
import os

class RSA():

    def __init__(self) -> None:

        self.gen_prime = GeneratePrime()
        self.utils = Utils()
        self.hash_func = hashlib.sha256
        self.k = int(1024/8)
        self.h_len = self.hash_func().digest_size

    def generate_keys(self):
        # gerando as chaves publica e privada para aplicar o metodo RSA de criptografia
        
        p = self.gen_prime.gen_prime()  
        q = self.gen_prime.gen_prime()  

        modulus = p * q
        
        totient = (p - 1) * (q - 1)
        
        encExp = 65537
        
        gcdExtendido = self.utils.extended_gcd(encExp, totient)
        decExp = gcdExtendido[1]

        if decExp < 0: 
            decExp += totient
        
        pubKey = [modulus, encExp]
        privKey = [modulus, decExp]

        return (pubKey, privKey)

    def RSAEncrypt(self, mensagem, pubKey):

        msgCifrada = []
        for i in mensagem:
            # pra cada inteiro da lista da mensagem criptografada (a lista passada como paramentro eh a mensagem,
            # quebrada em inteiros), a equacao abaixo eh computada, e um pedaco da mensagem eh cifrado

            # c = m^e (mod n) ->  m      e            mod n
            msgCifrada.append(pow(i, pubKey[1], pubKey[0]))
        
        # lista de inteiros que representam a mensagem criptografada
        return msgCifrada

    def RSADecrypt(self, msgCifrada, privKey):

        mensagem = []
        for i in msgCifrada:
            # para cada inteiro da lista da mensagem criptografada (a lista passada como paramentro eh a mensagem
            # criptografada, quebrada em inteiros), a equacao abaixo eh computada, e um pedaco da mensagem
            # original eh decifrado

            # m = c^d (mod n)-> c      d          mod n
            mensagem.append(pow(i, privKey[1], privKey[0]))
        
        # lista de inteiros que representam a mensagem original
        return mensagem

    def form_data_block(self, hashMsg, mensagem):
        # formatando a mensagem pra que seja possivel aplicar OAEP

        ps = bytearray()
        for _ in range(self.k - len(mensagem) - ( 2 * self.h_len ) - 2):
            # contando quantos 0's faltam pra mensagem ficar no tamanho certo pra
            # aplicar OAEP

            ps.append(0) 

        # concatenando o hash da mensagem, os 0's e o byte 0x01 com a mensagem porque agora da pra aplicar OAEP
        return hashMsg + ps + b'\x01' + mensagem

    def OAEPencrypt(self, mensagem, pubKey, label=""):

        label = label.encode()

        # se a mensagem for maior que o tamanho maximo que pode ser codificado usando OAEP, um erro eh lancado
        if len(mensagem) > self.k - 2 * self.h_len - 2:
            raise ValueError("Mensagem grande demais para ser codificada usando OAEP\n")

        # pegando o hash do label passado (ou nao) como paramento opcional
        l_hash = self.hash_func(label).digest()

        # formatando a mensagem com o hash da label pra que seja possivel aplicar OAEP
        dado = self.form_data_block(l_hash, mensagem)

        # 4) generate a random seed of length h_len
        semente = os.urandom(self.h_len)

        # gerando um 'mask' pra mensagem formmata pra OAEP
        mascaraDado = self.mgf1(semente, self.k - self.h_len - 1, self.hash_func)

        # mascarando a mensagem em bloco com a 'mask' gerada
        dadoMascarado = bytes(self.utils.xor(dado, mascaraDado))

        # gerando outra 'mask' pra semente
        mascaraSemente = self.mgf1(dadoMascarado, self.h_len, self.hash_func)
        
        # mascarando a semeste com a 'mask' gerada
        sementeMascara = bytes(self.utils.xor(semente, mascaraSemente))

        # concatenando o byte 0x00 com a semente mascarada e a mensagem mascarada em OAEP
        msgCodificada = b'\x00' + sementeMascara + dadoMascarado

        # cifra a mensagem com RSA e voila, mensagem criptografada
        return self.RSAEncrypt(msgCodificada, pubKey)

    def OAEPdecrypt(self, msgCodificada, privKey, label=""):

        # em resumo, o processo inverso de codificacao OAEP ta sendo feito aqui
        
        label = label.encode()

        msgCodificada = self.RSADecrypt(list(msgCodificada), privKey)

        l_hash = self.hash_func(label).digest()
        
        if len(msgCodificada) != self.k:
            raise ValueError("Mensagem codificada tem tamanho incorreto\n")

        sementeMascarada = bytes(msgCodificada[1 : self.h_len + 1])
        dadoMascarado = bytes(msgCodificada[self.h_len + 1:])

        # recuperando a mascara usada no processo de codificacao
        sementeMascara = self.mgf1(dadoMascarado, self.h_len, self.hash_func)

        # recuperando a semente usada no processo de codificacao
        semente = bytes(self.utils.xor(sementeMascarada, sementeMascara))

        mascaraDado = self.mgf1(semente, self.k - self.h_len - 1, self.hash_func)

        dado = bytes(self.utils.xor(dadoMascarado, mascaraDado))

        lHashGerado = dado[:self.h_len]

        if lHashGerado != l_hash:
            # se depois de recuperar as informacoes e refazer o processo de codificacao,
            # a mensagem nao gera o mesmo hash, o processo falhou porque alguma informacao tava errada

            raise ValueError("Mensagem decodificada nao gerou hash da label correto\n")
        
        # refazendo a mensagem que foi formatada pra aplicar OAEP
        comecoMsg = self.h_len + dado[self.h_len:].find(b'\x01') + 1
        mensagem = dado[comecoMsg:]
        
        # mensagem completamente recuperada
        return mensagem

    def mgf1(self, semente, tamanhoMascara, hash_func):
        # implementacao da funcao MGF1 usada no processo de codificacao e decodificacao OAEP
        
        if tamanhoMascara > 2**32 * self.h_len: raise ValueError("Mascara grande demais\n")
        
        T = bytearray()
        for counter in range(math.ceil(tamanhoMascara / self.h_len)):
            c = struct.pack(">I", counter)
            T += hash_func(semente + c).digest()
        return T[:tamanhoMascara]