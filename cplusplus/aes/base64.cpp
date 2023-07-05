#include<bits/stdc++.h>
#include "leitura.h"

using namespace std;

#define int long long
#define endl "\n"

char tabelaEquivalencias[64] = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/'};

int32_t main()
{
    cout << "Chamando a funcao de ler arquivo pra ver se ela funciona\n";

    vector<char> arquivo = lerArquivo();

    // for(int i=0; i<64; i++)
    // {
    //     cout << tabelaEquivalencias[i] << " ";
    // }

    // for(int i=0; i<arquivo.size(); i++)
    // {
    //     cout << arquivo[i] << " ";
    // }

    vector<int> binario;

    for(int i=0; i<arquivo.size(); i++)
    {
        int caractere = (int) arquivo[i];

        cout << "caractere a ser convertido: " << arquivo[i] << "\nDecimal do caractere: " << caractere << endl;

        if(caractere<128) binario.push_back(0);

        while(caractere>0)
        {
            binario.push_back(caractere%2);
            caractere/=2;
        }
    }

    // se chegar aqui, com certeza cada caractere transformado gerou um octeto

    if(binario.size()%3!=0)
    {
        int count = binario.size()%3;

        for(int i=0; i<count; i++) binario.push_back(0);
    }


    // 105 115 -> 01101001 01110011 -> 0110100101110011 -> 011010 010111 0011 -> 26 23 -> a X

    return 0;
}