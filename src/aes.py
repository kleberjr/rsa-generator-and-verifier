sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb
        , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb
        , 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e
        , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25
        , 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92
        , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84
        , 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06
        , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b
        , 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73
        , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e
        , 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b
        , 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4
        , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f
        , 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef
        , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61
        , 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]

rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

class AES():
    def __init__(self) -> None:
        self.value = 0

    def mul2_galois(self, valor):                                               # metodo implementado para fazer a multiplicacao de Galois
        temp = valor
        temp = temp>>7
        temp = temp and 0x1b

        return ((valor<<1)^temp)


    def CifraDecifra(self, estado, chave, encordec):                            # decifrando - encordec=1; cifrando - encordec=0
        if(encordec):                                                           # se estiver decifrando uma mensagem,
            for rodada in range(0,10,1):                                        # computando a ultima chave usada na cifracao antes de comecar a decifrar
                chave[0] = sbox[chave[13]]^chave[0]^rcon[rodada]
                chave[1] = sbox[chave[14]]^chave[1]
                chave[2] = sbox[chave[15]]^chave[2]
                chave[3] = sbox[chave[12]]^chave[3]

                for i in range(4,16,1):
                    chave[i] = chave[i]^chave[i-4]

            # aqui, a chave computada acima sera a primeira chave utilizada no processo de cifracao

            for i in range(0,16,1):                                             # primeiro 'AddRoundKey' da decifracao 
                estado[i] = estado[i]^chave[i]

        for rodada in range(0,10,1):                                            # 9 rodadas de cifracao, ja que uma chave de 128 bits exige 10 loops - o primeiro foi feito acima
            if(encordec):
                for i in range(15,3,-1):                                        # calculando as chaves de tras pra frente pra decifrar cada etapa da mensagem
                    chave[i] = chave[i]^chave[i-4]

                chave[0] = sbox[chave[13]]^chave[0]^rcon[9-rodada]
                chave[1] = sbox[chave[14]]^chave[1]
                chave[2] = sbox[chave[15]]^chave[2]
                chave[3] = sbox[chave[12]]^chave[3]
            else:
                for i in range(0,16,1):                                         # cifrando a mensagem original de acordo com a tabela de referencia - a sbox
                    estado[i] = sbox[estado[i]^chave[i]]
                
                aux = estado[1]                                                 # dando o tal 'shift' da primeira linha a partir do texto cifrado pela tabela sbox - se voce estiver decifrando, esse aqui eh o momento em que damos shift nas colunas
                estado[1] = estado[5]
                estado[5] = estado[9]
                estado[9] = estado[13]
                estado[13] = aux

                aux1 = estado[2]                                                # dando o tal 'shift' da segunda linha a partir do texto cifrado pela tabela sbox - se voce estiver decifrando, esse aqui eh o momento em que damos shift nas colunas
                aux2 = estado[6]
                estado[2] = estado[10]
                estado[6] = estado[14]
                estado[10] = aux1
                estado[14] = aux2

                aux = estado[15]                                                # dando o tal 'shift' da terceira linha a partir do texto cifrado pela tabela sbox - se voce estiver decifrando, esse aqui eh o momento em que damos shift nas colunas
                estado[15] = estado[11]
                estado[11] = estado[7]
                estado[7] = estado[3]
                estado[3] = aux
            
            if (rodada>0 and encordec) or (rodada<9 and not encordec):                              # esse trambique aqui eh pra cifrar o texto fazendo multiplicacao de Galois com o tal do metodo GCM
                for i in range(0,4,1):
                    aux = i<<2 # isso aqui ta com uma cara de que ta errado

                    if(encordec):                                                                   # fazendo a multiplicacao twist carpado de Galois pra voltar pro 'block cipher' depois que
                        aux1 = self.mul2_galois(self.mul2_galois(estado[aux]^estado[aux+2]))        # as colunas do 'block cipher' foram rodadas
                        aux2 = self.mul2_galois(self.mul2_galois(estado[aux+1]^estado[aux+3]))

                        estado[aux] = estado[aux]^aux1
                        estado[aux+1] = estado[aux+1]^aux2
                        estado[aux+2] = estado[aux+2]^aux1
                        estado[aux+3] = estado[aux+3]^aux2

                    aux1 = estado[aux]^estado[aux+1]^estado[aux+2]^estado[aux+3]                    # daqui pra frente eh cifrando pelo algoritmo as colunas restantes do bloco de 16 elementos do 'block cipher'
                    aux2 = estado[aux]                                                              # essa cifracao - referente ao passo MixColumns do processo - faz a multiplicacao de Galois pra gerar um novo 'block cipher'

                    aux3 = estado[aux]^estado[aux+1]
                    aux3 = self.mul2_galois(aux3)
                    estado[aux] = estado[aux]^aux3^aux1

                    aux3 = estado[aux+1]^estado[aux+2]
                    aux3 = self.mul2_galois(aux3)
                    estado[aux+1] = estado[aux+1]^aux3^aux1

                    aux3 = estado[aux+2]^estado[aux+3]
                    aux3 = self.mul2_galois(aux3)
                    estado[aux+2] = estado[aux+2]^aux3^aux1

                    aux3 = estado[aux+3]^aux2
                    aux3 = self.mul2_galois(aux3)
                    estado[aux+3] = estado[aux+3]^aux3^aux1
                
            if(encordec):                                                                           # se estiver decifrando,                                               
                aux = estado[13]                                                                    # de o shift nas linhas pra voltar pro estado original
                estado[13] = estado[9]
                estado[9] = estado[5]
                estado[5] = estado[1]
                estado[1] = aux
                
                aux = estado[10]                                                                    
                aux1 = estado[14]
                estado[10] = estado[2]
                estado[14] = estado[6]
                estado[2] = aux
                estado[6] = aux1
                
                aux = estado[3]                                                                     
                estado[3] = estado[7]
                estado[7] = estado[11]
                estado[11] = estado[15]
                estado[15] = aux

                for i in range(0,16,1):                                                             # pela sbox reversa - rsbox, consegue-se voltar ao texto original a cada rodada
                    estado[i] = rsbox[estado[i]]^chave[i]
            else:
                chave[0] = sbox[chave[13]]^chave[0]^rcon[rodada]                # calculando a chave a ser usada para cifrar o 'block cipher' da rodada
                chave[1] = sbox[chave[14]]^chave[1]
                chave[2] = sbox[chave[15]]^chave[2]
                chave[3] = sbox[chave[12]]^chave[3]

                for i in range(4,16,1):
                    chave[i] = chave[i]^chave[i-4]
                
        if(not encordec):                                                      # calculando o novo 'block cipher' com a chave calculada anteriormente
            for i in range(0,16,1):
                estado[i] = estado[i]^chave[i]

        return estado
    