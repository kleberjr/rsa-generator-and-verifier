from rsa import RSA

def main():
  mensagem = input("Digite uma mensagem: ").encode()
  
  rsa = RSA()
  
  # Parte I - Geração de chaves e cifra RSA ----------------------------------- #
  # a) Geração de chaves (p e q primos com no mínimo de 1024 bits) testando primalidade com Miller-Rabin
  print("\nGerando as chaves publica e privada...")
  chave_publica, chave_privada = rsa.gerar_chaves()
  
  print(">>>> Chave publica: ", chave_publica)
  print(">>>> Chave privada: ", chave_privada)
  
  # b) Cifração/decifração assimétrica RSA usando OAEP
  mensagem_criptografada = rsa.criptografar_com_OAEP(mensagem, chave_publica)
  
  print(">>>> Mensagem cifrada: ", mensagem_criptografada, "\n")
  
  # Descriptografamos a mensagem utilizando a chave privada gerada anteriormente
  mensagem_descriptografada = rsa.descriptografar_com_OAEP(mensagem_criptografada, chave_privada)
  
  print(">>>> Mensagem decifrada: ", mensagem_descriptografada)

if __name__ == "__main__":
  main()