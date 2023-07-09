import hashlib
import base64

class Utils():
    def extended_gcd(self, a, b):
        # algoritmo do gcd (maximo divisor comum) extendido postulado por Euclides em que os numeros usados pra se calcular
        # o gcd sao reutilizados na criacao de uma equacao diofantina com dois outros numeros que,
        # quando colocados na mesma equacao, compoem o gcd dos dois numeros

        # sendo a e b dois numeros inteiros, tem-se dois coeficientes x e y tais que

        # a*x + b*y = gcd(a,b)

        if b == 0:
            # se b=0, entao a*x+0*y = a*x, e ainda, gcd(a,0) = a, entao => a*1 = a, e assim x=1 e y=0
            return a, 1, 0
        else:
            # depois que voltar da iteracao em que gcd = a, x=1 e y=0 (do caso base), a recursiva
            # vai construindo a resposta voltando na arvore ate chegar nos a e b que foram dados

            gcd, x, y = self.extended_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    def xor(self, a, b):
        # fazendo a operacao XOR ao longo de duas strings binarias de mesmo tamanho e retornando essa string

        return [a[i] ^ b[i] for i in range(len(a))]

    def write_on_file(self, path, content, mode='w'):
        # metodo para escrever em arquivo

        with open(path, mode) as file:
            file.write(f'{content}\n')

    def read_from_file(self, path, mode='r'):
        # metodo pra ler de arquivo

        with open(path, mode) as file:
            return file.read()

    def encode_to_base64(self, message):
        # metodo pra codificar em base64

        return base64.b64encode(message).decode('ascii')

    def decode_from_base64(self, message):
        # metodo pra decodificar de base64

        return base64.b64decode(message)
    
    def hash_128_bits(self, key):
        # metodo pra gerar um hash de 128 bits em hexadecimal

        return int(hashlib.sha3_256(str(key).encode()).hexdigest(), base=16)
    
    def padding(self, message):
        # adicionando os bytes que faltam pra completar o tamanho da mensagem ate ser possivel aplicar o algoritmo de cifracao

        remainder = 16 - len(message) % 16

        return message + bytes([remainder] * remainder) # adicionando os bytes que faltam na mensagem pra ela ficar do tamanho certo

    def remove_padding(self, message):
        # tirando os bytes a mais que foram colocados na mensagem pra ela ficar do tamanho certo pra aplicar a cifra AES

        return message[:-message[-1]]

    def split_128bits(self, message):
        # quebrando a mensagem em blocos de 128 bits

        return [message[i:i+16] for i in range(0, len(message), 16)]


