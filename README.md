# Implementação de um Gerador e Verificador de assinaturas RSA em arquivos

O programa contém as seguintes funcionalidades:

### Parte I: Cifração de decifração AES, chave de 128 bits
- [ ] Geração de chave de 128 bits
- [ ] Cifração e decifração
- [ ] Extra: cifração autenticada modo GCM – Contador de Galois
### Parte II: Geração de chaves e cifra RSA
- [ ] Geração de chaves (p e q primos com no mínimo de 1024 bits) testando primalidade com Miller-Rabin
- [ ] OAEP
- [ ] Cifração/decifração assimétrica RSA usando OAEP
### Parte III: Assinatura RSA
- [ ] Assinatura da mensagem (cifração do hash da mensagem)
- [ ] Formatação do resultado (caracteres especiais e informações para verificação em BASE64)
### Parte II: Verificação
- [ ] Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64)
- [ ] Decifração da assinatura (decifração do hash)
- [ ] Verificação (cálculo e comparação do hash do arquivo)

## Execução do Programa

Para que o programa seja testado, é necessário executar a seguinte linha de comando no *bash*

``python3 main.py``

Para tanto, faz-se necessário o uso dos pacotes da biblioteca **Python3** para que o projeto possa ser analisado.

### Observações

A cifra **AES** requer um arquivo com a mensagem a ser cifrada para o correto funcionamento. A pasta **Testes** é o local onde este arquivo deve ser armazenado, e é crucial que o arquivo de entrada esteja no local refereido. Por outro lado, a cifra **RSA** requer apenas que a mensagem seja passada pela linha de comando, não sendo necessário realizar etapas anteriores ao teste de funcionamento, como deve ser feito para a cifra **AES**. O correto funcionamento do projeto é descrito no menu de interação com o usuário, presente na execução do arquivo principal ``main.py``
