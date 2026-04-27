Autores: Edinei Xavier - 2310369 \
Autores: Matheus Norões - 2224600 \
Autores: Lucas Falcão - 2315036 \
Autores: Samir Alves - 2315046 \

# Resumo

Este teste de carga analisa a disponibilidade de um serviço **WordPress** em múltiplas instancias. Foi utilizada a framework de testes de carga **Locust**, O balanceador de carga **nginx** e contêineres feitos em **Docker** foram utilizados para: Hospedagem do serviço, framework e balanceador de carga, armazenamento das postagens do blog em um banco de dados **MySQL**

# Metodologia

O teste carga realizado no Locust foram realizados em 3 postagens do blog.  A primeira postagem contia uma imagem de 1MB, a segunda contia uma imagem de 300KB e a terceira postagem contia um texto de 400KB, os testes foram separados em três categorias: Leve, Medio e Pesado. Cade teste foi realizado em um tempo máximo de 2 minutos com um numero crescente de usuários gerados e instancias do serviço.

# Resultados e Discussão

O resultados obtidos, por meio do Locust, mostraram o comportamento da disponibilidade do serviço considerando diferentes instancias disponíveis e usuários entrando por segundo.

| Teste | Instâncias WordPress | Usuários simultâneos | Conteúdos acessados                      |
| ----- | -------------------: | -------------------: | ---------------------------------------- |
| T1    |                    1 |                  150 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T2    |                    1 |                  300 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T3    |                    1 |                 1500 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T4    |                    2 |                  150 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T5    |                    2 |                  300 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T6    |                    2 |                 1500 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T7    |                    3 |                  150 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T8    |                    3 |                  300 | imagem 1 MB, imagem 300 KB, texto 400 KB |
| T9    |                    3 |                 1500 | imagem 1 MB, imagem 300 KB, texto 400 KB |

## 1 Instancia

![imagem](data/imagens/resultados.png)

| Teste      | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ---------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga leve | Imagem 1MB   |          1 |      150 |        2933 |      0 |     0,00 |              109 |           83 |      270 | 24,50 |
| Carga leve | Imagem 300KB |          1 |      150 |        2803 |      0 |     0,00 |              106 |           83 |      260 | 23,42 |
| Carga leve | Texto 400KB  |          1 |      150 |        2864 |      0 |     0,00 |              112 |           90 |      260 | 23,93 |

| Teste       | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ----------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga média | Imagem 1MB   |          1 |      300 |        5376 |      0 |     0,00 |              280 |          210 |      680 | 44,84 |
| Carga média | Imagem 300KB |          1 |      300 |        5195 |      0 |     0,00 |              273 |          190 |      670 | 43,33 |
| Carga média | Texto 400KB  |          1 |      300 |        5200 |      0 |     0,00 |              289 |          220 |      700 | 43,38 |

| Teste        | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |    RPS |
| ------------ | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | -----: |
| Carga pesada | Imagem 1MB   |          1 |     1500 |       14820 |  12411 |    83,74 |             1605 |          210 |     9700 | 123,25 |
| Carga pesada | Imagem 300KB |          1 |     1500 |       14824 |  12397 |    83,63 |             1583 |          240 |     9600 | 123,28 |
| Carga pesada | Texto 400KB  |          1 |     1500 |       14823 |  12399 |    83,65 |             1631 |          240 |     9700 | 123,27 |

No teste pesado com 1 instância, o Locust indicou uso elevado de CPU e encerrou os testes precocemente. Mesmo assim, os dados foram úteis pois mostram que houve saturação do serviço web. A taxa de erro ficou em 83,67%, com falhas principalmente por RemoteDisconnected, erro HTTP 500 e ConnectionResetError. Isso indica que uma única instância do WordPress não conseguiu sustentar a carga de 1500 usuários no ambiente local.
Na carga pesada, a diferença mais importante é a taxa de erro: com 1 instância, o erro foi 83,67%; com 3 instâncias, caiu para 53,23%. Ou seja, mesmo que o cenário pesado tenha causado instabilidade nos dois casos, aumentar o número de instâncias reduziu bastante a proporção de falhas.

## 2 Instancias

| Teste      | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ---------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga leve | Imagem 1MB   |          2 |      150 |        2793 |      0 |     0,00 |              131 |          110 |      320 | 23,31 |
| Carga leve | Imagem 300KB |          2 |      150 |        2896 |      0 |     0,00 |              130 |          100 |      310 | 24,17 |
| Carga leve | Texto 400KB  |          2 |      150 |        2771 |      0 |     0,00 |              141 |          110 |      330 | 23,13 |

| Teste       | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ----------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga média | Imagem 1MB   |          2 |      300 |        4786 |      0 |     0,00 |              473 |          400 |     1000 | 40,06 |
| Carga média | Imagem 300KB |          2 |      300 |        4854 |      0 |     0,00 |              469 |          400 |     1000 | 40,62 |
| Carga média | Texto 400KB  |          2 |      300 |        4841 |      0 |     0,00 |              499 |          430 |     1000 | 40,52 |

| Teste        | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ------------ | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga pesada | Imagem 1MB   |          2 |     1500 |        9100 |   4721 |    51,88 |             3609 |         1600 |    18000 | 74,14 |
| Carga pesada | Imagem 300KB |          2 |     1500 |        9203 |   4708 |    51,16 |             3678 |         1600 |    18000 | 74,98 |
| Carga pesada | Texto 400KB  |          2 |     1500 |        9261 |   4776 |    51,57 |             3801 |         1700 |    19000 | 75,45 |

Nos testes com 2 instâncias, as cargas leve e média foram concluídas sem falhas, mantendo 0,00% de erro. Já no teste pesado, com 1500 usuários, o sistema apresentou 51,53% de erro, com falhas do tipo erro HTTP 500, conexões encerradas sem resposta e reset de conexão. Isso indica que, nesse nível de carga, a arquitetura local entrou em saturação, mesmo utilizando duas instâncias do WordPress.

## 3 Instancias

| Teste      | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ---------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga leve | Imagem 1MB   |          3 |      150 |        2722 |      0 |     0,00 |              128 |           97 |      320 | 22,73 |
| Carga leve | Imagem 300KB |          3 |      150 |        2872 |      0 |     0,00 |              133 |           99 |      310 | 23,99 |
| Carga leve | Texto 400KB  |          3 |      150 |        2807 |      0 |     0,00 |              135 |          110 |      320 | 23,44 |

| Teste       | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ----------- | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga média | Imagem 1MB   |          3 |      300 |        5409 |      0 |     0,00 |              240 |          160 |      600 | 45,28 |
| Carga média | Imagem 300KB |          3 |      300 |        5304 |      0 |     0,00 |              234 |          160 |      570 | 44,40 |
| Carga média | Texto 400KB  |          3 |      300 |        5312 |      0 |     0,00 |              248 |          170 |      600 | 44,47 |

| Teste        | Conteúdo     | Instâncias | Usuários | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) |   RPS |
| ------------ | ------------ | ---------: | -------: | ----------: | -----: | -------: | ---------------: | -----------: | -------: | ----: |
| Carga pesada | Imagem 1MB   |          3 |     1500 |       11607 |   6241 |    53,77 |             2489 |         1100 |    11000 | 95,62 |
| Carga pesada | Imagem 300KB |          3 |     1500 |       11614 |   6133 |    52,81 |             2487 |         1100 |    11000 | 95,68 |
| Carga pesada | Texto 400KB  |          3 |     1500 |       11877 |   6309 |    53,12 |             2590 |         1200 |    12000 | 97,84 |

No teste de carga leve, foram utilizadas 3 instâncias do WordPress, com duração de 2 minutos, máximo de 150 usuários simultâneos e taxa de criação de 75 usuários por segundo. O teste acessou três tipos de conteúdo: um post com imagem de aproximadamente 1 MB, um post com imagem de aproximadamente 300 KB e um post com texto de aproximadamente 400 KB.
Ao final da execução, foram realizadas 8401 requisições, sem ocorrência de falhas, resultando em uma taxa de erro de 0,00%. O tempo médio de resposta agregado foi de 132 ms, com mediana de 100 ms e tempo máximo de 1118 ms. A taxa média de requisições foi de 70,16 requisições por segundo.
Os resultados indicam que, para a carga leve aplicada, a arquitetura com Nginx balanceando três instâncias do WordPress conseguiu atender às requisições de forma estável, sem falhas e com baixo tempo médio de resposta.

No teste de carga média, foram utilizadas 3 instâncias do WordPress, com duração de 2 minutos, máximo de 300 usuários simultâneos e taxa de criação de 150 usuários por segundo. O teste realizou 16025 requisições no total, sem ocorrência de falhas, resultando em 0,00% de erro.
O tempo médio de resposta agregado foi de 241 ms, com mediana de 170 ms, P95 de 590 ms e P99 de 860 ms. A taxa média de requisições foi de 134,15 requisições por segundo. Em comparação com o teste leve, houve aumento no tempo médio de resposta, mas a aplicação continuou estável, sem falhas registradas.

No teste pesado, com 1500 usuários e taxa de criação de 75 usuários por segundo, a aplicação apresentou forte degradação. Foram realizadas 35098 requisições, porém 18683 falharam, resultando em 53,23% de erro. O tempo médio agregado subiu para 2523 ms e o P95 chegou a 11000 ms, indicando que parte significativa das requisições teve alto tempo de resposta.
Os principais erros foram 500 Internal Server Error, conexões encerradas sem resposta e reset de conexão. Isso indica que a carga aplicada ultrapassou a capacidade da arquitetura local, mesmo com 3 instâncias do WordPress. Portanto, esse cenário pode ser usado para demonstrar o ponto em que o sistema deixa de se manter estável.

# Conclusão

Neste teste de carga foi analisado a disponibilidade de um serviço replicado em múltiplas instancias usando o nginx como balanceador de carga. A partir destes testes foi possível observar como o serviço se comporta com uma quantidade crescente de usuários o acessando simultaneamente ---------------