import random

TENTATIVAS = 20

LISTA_PRIMOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                     31, 37, 41, 43, 47, 53, 59, 61, 67,  
                     71, 73, 79, 83, 89, 97, 101, 103,  
                     107, 109, 113, 127, 131, 137, 139,  
                     149, 151, 157, 163, 167, 173, 179,  
                     181, 191, 193, 197, 199, 211, 223, 
                     227, 229, 233, 239, 241, 251, 257, 
                     263, 269, 271, 277, 281, 283, 293, 
                     307, 311, 313, 317, 331, 337, 347, 349] 

class MillerRabin:
    def __init__(self) -> None:
        self.rng = random.SystemRandom()

    def low_level_prime(n): 
        while True:
            prime_candidate = MillerRabin.random_n_bits_number(n)  
            for divisor in LISTA_PRIMOS: 
                if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                    # se o candidato a primo for divisivel por um primo, ou algum primo ao quadrado
                    # for menor ou igual ao candidato a primo, ele nao eh primo

                    break
            else:
                return prime_candidate

    def trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two):
        # isso aqui eh um metodo auxiliar pra testar se um numero eh primo por meio do teste de primalidade do Miller-Rabin,
        # mas eu nao sei explicar nadica de nada disso, entao fica aqui a implementacao
        
        if pow(round_tester, even_component, prime_candidate) == 1: 
            return False

        for i in range(max_divisions_by_two): 
            if pow(round_tester, 2**i * even_component, prime_candidate) == prime_candidate-1: 
                return False
        return True

    def miller_rabin(prime_candidate):
        # eu realmente nao sei explicar o metodo de miller-rabin

        max_divisions_by_two = 0
        even_component = prime_candidate-1

        while even_component % 2 == 0: 
            even_component >>= 1
            max_divisions_by_two += 1
        assert(2 ** max_divisions_by_two * even_component == prime_candidate-1) 
    
        for _ in range(TENTATIVAS): 
            round_tester = random.randrange(2, prime_candidate) 
            if MillerRabin.trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two): 
                return False
        return True

    @staticmethod
    def random_n_bits_number(n):
        # retornando um numero aleatorio de 128 bits em dua representacao decimal

        return random.randrange(2 ** (n-1) + 1, 2 ** n - 1)             
    
    @staticmethod
    def get_prime_n_bits(n):
        prime = 0
        while True: 
            prime_candidate = MillerRabin.low_level_prime(n) 
            
            if not MillerRabin.miller_rabin(prime_candidate): 
                # se o candidato a primo nao passou no teste de primalidade, ele nao eh primo

                continue
            else:
                # se ele passar o teste de primalidade, ele eh o primeiro primo de n bits que da pra pegar
                
                prime = prime_candidate
                break

        return prime

    def single_test(self, number: int, witness: int) -> bool:
        # fazendo teste unitario da primalidade usando Miller-Rabin
        
        exp, rem = number - 1, 0
        while not exp & 1:  # check if exp is even
            exp >>= 1
            rem += 1
        x = pow(witness, exp, number)
        if x == 1 or x == number - 1:
            return True
        for _ in range(rem - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                return True
        return False

    def is_prime(self, number: int, k=40) -> bool:
        # testando a primalidade de um numero a partir do metodo de Miller-Rabin
        # eu nao sei explicar como que isso aqui funciona

        if number <= 1: return False
        if number <= 3: return True
        if number % 2 == 0 or number % 3 == 0: return False

        for _ in range(k):
            witness = self.rng.randrange(2, number - 1)
            if not self.single_test(number, witness): return False
        return True
