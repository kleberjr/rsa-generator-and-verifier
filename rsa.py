import random
import hashlib
from os import urandom
import struct
import math

class RSA():
  def __init__(self) -> None:
    self.k = int(1024/8)
    self.h_len = hashlib.sha256().digest_size
  
  def gerar_chaves(self):
    # Gera aleatoriamente os primos p e q necessários
    p = self.gerar_primo()
    q = self.gerar_primo()

    modulo = p * q
    
    tociente = (p - 1) * (q - 1)
    
    expoente_de_cifraçao = 65537
    
    mdc = self.mdc_bezout(expoente_de_cifraçao, tociente)
    expoente_de_decifracao = mdc[1]

    if (expoente_de_decifracao < 0): 
      expoente_de_decifracao += tociente
    
    chave_publica = [modulo, expoente_de_cifraçao]
    chave_privada = [modulo, expoente_de_decifracao]

    return (chave_publica, chave_privada)
  
  def criptografar_com_OAEP(self, mensagem, chave_publica, label=""):
    label = label.encode()

    if (len(mensagem) > self.k - 2 * self.h_len - 2):
      raise ValueError("A mensagem é muito grande pra ser cifrada com OAEP.")

    # 1) hash the label using sha256
    l_hash = hashlib.sha256(label).digest()

    # 2) generate a padding string PS
    # 3) concatenate l_hash, ps, the single byte 0x01, and the mensagem M
    db = self.agrupa_bloco(l_hash, mensagem)

    # 4) generate a random seed of length h_len
    seed = urandom(self.h_len)

    # 5) generate a mask of the appropriate length for the data block
    db_mask = self.mgf1(seed, self.k - self.h_len - 1, hashlib.sha256)

    # 6) mask the data block with the generated mask
    masked_db = bytes(self.xor(db, db_mask))

    # 7) generate a mask of length hLen for the seed
    seed_mask = self.mgf1(masked_db, self.h_len, hashlib.sha256)
    
    # 8) mask the seed with the generated mask
    masked_seed = bytes(self.xor(seed, seed_mask))

    # 9) the encoded (padded) mensagem is the byte 0x00 concatenated with the masked_seed and masked_db
    encoded_mensagem = b'\x00' + masked_seed + masked_db

    # 10) encrypt mensagem with RSA
    return self.RSAEncrypt(encoded_mensagem, chave_publica)

  def descriptografar_com_OAEP(self, mensagem_cifrada, chave_privada, label=""):      
      label = label.encode()

      # 1) decrypt message with RSA
      mensagem_cifrada = self.RSADecrypt(list(mensagem_cifrada), chave_privada)

      # 2) hash the label using sha256
      l_hash = self.hash_func(label).digest()
      
      if len(mensagem_cifrada) != self.k:
        raise ValueError("A mensagem cifrada não tem o comprimento esperado.")

      # 3) reverse step 9: split the encoded message
      masked_seed = bytes(mensagem_cifrada[1 : self.h_len + 1])
      masked_db = bytes(mensagem_cifrada[self.h_len + 1:])

      # 4) generate the seed_mask which was used to mask the seed
      seed_mask = self.mgf1(masked_db, self.h_len, self.hash_func)

      # 5) reverse step 8: recover the seed
      seed = bytes(self.xor(masked_seed, seed_mask))

      # 6) generate the db_mask which was used to mask the data block
      db_mask = self.mgf1(seed, self.k - self.h_len - 1, self.hash_func)

      # 7) reverse step 6: recover the data block
      db = bytes(self.xor(masked_db, db_mask))

      # 8) verify if the decoded message is valid
      l_hash_gen = db[:self.h_len]

      if l_hash_gen != l_hash:
        raise ValueError("Decoded message has incorrect label hash.")
      
      # 9) split the message correctly
      message_start = self.h_len + db[self.h_len:].find(b'\x01') + 1
      message = db[message_start:]
      
      return message
  
  def gerar_primo(self):
    while True:
      numero = (random.SystemRandom().randrange(1 << 1024 - 1, 1 << 1024) << 1) + 1
      
      if (self.eh_primo(numero)):
        return numero
      else:
        raise Exception("Não foi possível gerar um número primo")
  
  def mdc_bezout(self, a, b):
    if b == 0:
      return a, 1, 0
    else:
      mdc, x, y = self.mdc_bezout(b, a % b)
      return mdc, y, x - (a // b) * y

  def eh_primo(self, numero, k=40):
    if (numero <= 1): 
      return False
    
    if (numero <= 3): 
      return True
    
    if (numero % 2 == 0 or numero % 3 == 0): 
      return False

    for i in range(k):
      aux = random.SystemRandom().randrange(2, numero - 1)
      
      if (not self.teste_unico(numero, aux)): 
        return False
    
    return True
  
  def teste_unico(self, numero, aux):
    exp, rem = numero - 1, 0
    
    # Checa se o expoente é par
    while (not exp & 1):
      exp >>= 1
      rem += 1
    
    x = pow(aux, exp, numero)
    
    if (x == 1 or x == numero - 1):
      return True
    
    for i in range(rem - 1):
      x = pow(x, 2, numero)
      
      if (x == numero - 1):
        return True
    
    return False
  
  def xor(self, a, b):
    return [a[i] ^ b[i] for i in range(len(a))]
  
  def agrupa_bloco(self, l_hash, mensagem):
    ps = bytearray()

    for c in range(self.k - len(mensagem) - ( 2 * self.h_len ) - 2):
      ps.append(0) 
    
    return l_hash + ps + b'\x01' + mensagem
  
  def mgf1(self, semente, comprimento_da_mascara, funcao_hash):
    if (comprimento_da_mascara > 2**32 * self.h_len): 
      raise ValueError("Mask too long.")
    
    T = bytearray()

    for counter in range(math.ceil(comprimento_da_mascara / self.h_len)):
      c = struct.pack(">I", counter)
      T += funcao_hash(semente + c).digest()

    return T[:comprimento_da_mascara]
  
  def RSAEncrypt(self, encoded_message, public_key):
      """
      Encrypts a message using RSA encryption.

      Args:
          encoded_message (list): The message to be encrypted, represented as a list of ints.
          public_key (tuple): The RSA public key, represented as a tuple of two ints (n, e).

      Returns:
          list: The encrypted message, represented as a list of ints.
      """
      cryptogram = []
      for i in encoded_message:
          # c = m^e \mod n
          cryptogram.append(pow(i, public_key[1], public_key[0]))
      return cryptogram

  def RSADecrypt(self, encoded_message, private_key):
      """
      Decrypts an RSA-encrypted message.

      Args:
      encoded_message (list): The encrypted message, represented as a list of ints.
          private_key (tuple): The RSA private key, represented as a tuple of two ints (n, d).

      Returns:
          list: The decrypted message, represented as a list of ints.
      """
      message = []
      for i in encoded_message:
          # m = c^d \mod n
          message.append(pow(i, private_key[1], private_key[0]))
      return message