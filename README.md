# Implementação de um Gerador e Verificador de assinaturas RSA em arquivos

O programa deve conter as seguintes funcionalidades:

### Parte I: Cifração de decifração AES, chave de 128 bits
- [ ] Geração de chave de 128 bits
- [ ] Cifração e decifração
- [ ] Extra: cifração autenticada modo XTR – Contador de Galois
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
