
#include<bits/stdc++.h>

using namespace std;

int main()
{
    FILE *in;
    FILE *out;
    char buffer[5];

    in = fopen("entrada.txt", "r");
    out = fopen("saida.txt", "w");

    if(in == NULL)
    {
        cout << "Erro ao abrir o arquivo.\n";
        return 0;
    }else
    {
        while(!feof(in))
        {
            if(fgets(buffer, 5, in)==NULL) break;
            fputs(buffer, out);
        }

        fclose(in);
    }

    return 0;
}