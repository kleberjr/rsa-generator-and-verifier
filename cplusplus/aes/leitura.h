
#include<bits/stdc++.h>

using namespace std;

vector<char> lerArquivo()
{
    FILE *f;
    int tamanho;
    char * buffer;
    size_t arquivo;
    vector<char> listaRetorno;

    f = fopen("in.txt", "r");

    if(f == NULL)
    {
        cout << "Erro ao abrir o arquivo.\n";
    }else
    {
        // pegando o tamanho do arquivo pra iterar sobre ele
        fseek(f, 0, SEEK_END);
        tamanho = ftell(f);
        rewind(f);

        // alocando o tamanho do arquivo
        buffer = (char*) malloc(tamanho * sizeof(char));

        if(buffer == NULL)
        {
            cout << "Arquivo corrompido.\n";
        }

        // colocando o texto do arquivo na estrutura char * pra tratar no programa
        arquivo = fread(buffer, 1, tamanho,f);

        if(arquivo!=tamanho)
        {
            cout << "Problema na leitura do arquivo\n";
        }

        int count=0;
        while(count<tamanho)
        {
            listaRetorno.push_back(buffer[count]);
            //cout << buffer[count] << " ";
            count++;
        }
    }

    fclose(f);
    free(buffer);

    for(int i=0; i<listaRetorno.size(); i++)
    {
        
    }

    return listaRetorno;
}