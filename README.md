# protoServidor

Alunos:
    Guilherme Neri Bustamante Sá
    Rafael Fernandes

Trabalho da disciplina de Redes de Computadores e blablabla.

A ideia do trabalho é bastante interessante. Já havíamos feito um cliente/servidor em outra disciplina (implementando um MUD), mas este trabalho sem dúvidas foi bem mais completo no que diz respeito à troca de informações entre máquinas. Além do mais, a prática nos fez entender bem melhor como funcionam as requisições HTTP do que se fosse apenas com teoria.
Nós demoramos um pouquinho para entender o funcionamento do protobuf, mas depois de entender como ele funcionava e para que era utilizado foi bem simples fazer a implementação. Outra questão que vale ressaltar é que um dos membros da dupla não tinha muita noção de Python e com este trabalho foi possível entender muita coisa sobre a linguagem, principalmente sobre a biblioteca socket e como funciona o sistema de threads.


Para executar:
    servidor:
        python3 server.py <IP> <PORTA>
    
    cliente:
        python3 client.py <IP> <PORTA>