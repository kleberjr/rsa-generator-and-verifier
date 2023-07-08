import random

NUMBER_OF_TRIES = 20

FIRST_PRIMES_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
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
        """
        Initializes the MillerRabin object
        """
        self.rng = random.SystemRandom()

    def low_level_prime(n): 
        while True: 
            prime_candidate = MillerRabin.random_n_bits_number(n)  
            for divisor in FIRST_PRIMES_LIST: 
                    if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate: 
                            break
            else:
                return prime_candidate

    def trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two): 
        if pow(round_tester, even_component, prime_candidate) == 1: 
            return False

        for i in range(max_divisions_by_two): 
            if pow(round_tester, 2**i * even_component, prime_candidate) == prime_candidate-1: 
                return False
        return True

    def miller_rabin(prime_candidate): 
        max_divisions_by_two = 0
        even_component = prime_candidate-1

        while even_component % 2 == 0: 
            even_component >>= 1
            max_divisions_by_two += 1
        assert(2 ** max_divisions_by_two * even_component == prime_candidate-1) 
    
        for _ in range(NUMBER_OF_TRIES): 
            round_tester = random.randrange(2, prime_candidate) 
            if MillerRabin.trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two): 
                return False
        return True

    @staticmethod
    def random_n_bits_number(n): 
        return random.randrange(2 ** (n-1) + 1, 2 ** n - 1)             # retornando um numero aleatorio de 128 bits em dua representacao decimal
    
    @staticmethod
    def get_prime_n_bits(n):
        prime = 0
        while True: 
            prime_candidate = MillerRabin.low_level_prime(n) 
            
            if not MillerRabin.miller_rabin(prime_candidate): 
                    continue
            else: 
                    prime = prime_candidate
                    break
        return prime

    def single_test(self, number: int, witness: int) -> bool:
        """
        Perform a single test of the Miller-Rabin primality test
        
        Args:
            number (int): The number to be tested for primality.
            witness (int): A random integer in the range [2, number-1].
        
        Returns:
            bool: True if number is probably prime, False otherwise
        """
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
        """
        Test a number:param rimality using the Miller-Rabin primality test

        Args:
            number (int): The number to be tested for primality
            k (int, optinal): The number of iterations of the single_test function to perform. Default is 40.
        
        Returns
            bool: True if number is probably prime, False otherwise
        """
        if number <= 1: return False
        if number <= 3: return True
        if number % 2 == 0 or number % 3 == 0: return False

        for _ in range(k):
            witness = self.rng.randrange(2, number - 1)
            if not self.single_test(number, witness): return False
        return True
