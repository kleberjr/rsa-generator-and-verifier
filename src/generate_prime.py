import random
from .miller_rabin import MillerRabin

class GeneratePrime:

    def __init__(self) -> None:
        self.rng = random.SystemRandom()
        self.miller_rabin = MillerRabin()

    def gen_prime(self) -> int:
        # gerando um numero e vendo se esse numero eh primo a partir do teste de primalidade de Miller-Rabin

        while True:
            # pega um numero aleatorio entre dois numeros muito grandes
            isprime = (self.rng.randrange(1 << 1024 - 1, 1 << 1024) << 1) + 1

            # checando se esse numero eh primo por Miller-Rabin
            if self.miller_rabin.is_prime(isprime):
                # esse numero eh primo 

                return isprime
