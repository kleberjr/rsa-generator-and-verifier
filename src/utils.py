import hashlib
import base64

class Utils():
    """
    Class for utility functions.
    """
    def extended_gcd(self, a, b):
        """
        Computes the greatest common divisor (gcd) and the coefficients of Bezout's identity using the extended Euclidean algorithm.

        Args:
            a (int): An integer.
            b (int): An integer.

        Returns:
            Tuple[int, int, int]: A tuple containing the gcd of a and b, and the coefficients x and y of Bezout's identity.
        """
        if b == 0:
            return a, 1, 0
        else:
            gcd, x, y = self.extended_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    def xor(self, a, b):
        """
        Computs a xor operation between two strings

        Args:
            a: A string
            b: A string

        Returns:
            A string resulted of a xor operation

        """
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


