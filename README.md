Autores: Edinei Xavier - 2310369 \
Autores: Matheus Norões - 2224600 \
Autores: Lucas Falcão - 2315036 \
Autores: Samir Alves - 2315046 

# Comparação de Tecnologias de Invocação de Serviços Remotos

## Resumo

Este trabalho compara quatro tecnologias de invocação de serviços remotos - **REST**, **SOAP**, **GraphQL** e **gRPC** - por meio da implementação de um serviço de streaming de músicas em **Java** e **Kotlin**, seguida de testes de carga com a ferramenta **Locust**. Toda a infraestrutura é containerizada via **Docker Compose**.

## Pendências Resolvidas / Mudanças Feitas
Os testes agora estão sendo feitos no conteiner do Locust usando uma biblioteca de requisição gPRC.

## Infraestrutura

- **Spring Boot**: framework utilizado para implementar todos os serviços, tanto em Java quanto em Kotlin
- **H2**: banco de dados em memória embutido em cada serviço, populado automaticamente na inicialização
- **Locust**: gerador de carga, executado como container Docker
- **Docker Compose**: orquestração de todos os serviços

## Serviço Implementado

O serviço gerencia três recursos — **Usuários**, **Músicas** e **Playlists** — e expõe as seguintes operações em cada tecnologia:

| Operação | Descrição |
|---|---|
| Todos os usuários | Retorna todos os usuários cadastrados |
| Todas as músicas | Retorna todas as músicas cadastradas |
| Playlists por usuário | Retorna as playlists de um determinado usuário |
| Playlists por música | Retorna as playlists que contêm uma determinada música |

Cada serviço foi implementado nas quatro tecnologias e nas duas linguagens, totalizando **8 serviços** independentes, cada um em seu próprio container:

| Serviço | Porta |
|---|---|
| REST Java | 8080 |
| SOAP Java | 8081 |
| gRPC Java | 8082 |
| GraphQL Java | 8083 |
| REST Kotlin | 8084 |
| SOAP Kotlin | 8085 |
| gRPC Kotlin | 8086 |
| GraphQL Kotlin | 8087 |


## Metodologia

Os testes simulam usuários realizando as quatro operações do serviço de forma simultânea. Cada tecnologia foi testada sob três níveis de carga, com duração de **3 minutos** por teste:

| Nível | Usuários simultâneos | Spawn rate |
|---|---|---|
| Leve | 100 | 15/s |
| Médio | 200 | 30/s |
| Pesado | 300 | 75/s |

As métricas coletadas foram: tempo médio de resposta, mediana, P95 e throughput (requisições/s). Os resultados são salvos em CSV pelo Locust e processados pelo script `graficos.py`.

## Resultados e Discussão

### Tabela Geral dos Testes

| Linguagem | API | Carga | Requisições | Falhas | Erro (%) | Tempo médio (ms) | Mediana (ms) | P95 (ms) | RPS |
|---|---|---|---|---|---|---|---|---|---|
| Java | GraphQL | Leve | 8.743 | 0 | 0,00 | 11 | 8 | 18 | 48,91 |
| Java | GraphQL | Médio | 17.684 | 0 | 0,00 | 7 | 5 | 16 | 98,47 |
| Java | GraphQL | Pesado | 26.728 | 0 | 0,00 | 6 | 4 | 13 | 148,85 |
| Java | gRPC | Leve | 8.630 | 0 | 0,00 | 6 | 6 | 10 | 48,23 |
| Java | gRPC | Médio | 17.641 | 0 | 0,00 | 4 | 4 | 7 | 98,59 |
| Java | gRPC | Pesado | 26.630 | 0 | 0,00 | 3 | 2 | 6 | 148,85 |
| Java | REST | Leve | 8.731 | 0 | 0,00 | 24 | 17 | 59 | 48,88 |
| Java | REST | Médio | 17.529 | 0 | 0,00 | 21 | 16 | 52 | 97,57 |
| Java | REST | Pesado | 25.895 | 0 | 0,00 | 51 | 20 | 185 | 145,68 |
| Java | SOAP | Leve | 8.802 | 0 | 0,00 | 24 | 12 | 42 | 48,98 |
| Java | SOAP | Médio | 17.625 | 0 | 0,00 | 17 | 11 | 47 | 98,11 |
| Java | SOAP | Pesado | 22.026 | 0 | 0,00 | 389 | 12 | 2200 | 123,12 |
| Kotlin | GraphQL | Leve | 8.778 | 0 | 0,00 | 20 | 9 | 18 | 48,85 |
| Kotlin | GraphQL | Médio | 17.684 | 0 | 0,00 | 7 | 5 | 15 | 98,66 |
| Kotlin | GraphQL | Pesado | 26.817 | 0 | 0,00 | 6 | 4 | 14 | 149,36 |
| Kotlin | gRPC | Leve | 8.622 | 0 | 0,00 | 6 | 6 | 10 | 48,16 |
| Kotlin | gRPC | Médio | 17.614 | 0 | 0,00 | 4 | 4 | 7 | 98,40 |
| Kotlin | gRPC | Pesado | 26.636 | 0 | 0,00 | 3 | 2 | 6 | 148,89 |
| Kotlin | REST | Leve | 8.497 | 0 | 0,00 | 90 | 17 | 57 | 47,29 |
| Kotlin | REST | Médio | 17.628 | 0 | 0,00 | 22 | 15 | 56 | 98,12 |
| Kotlin | REST | Pesado | 26.385 | 0 | 0,00 | 24 | 15 | 60 | 147,73 |
| Kotlin | SOAP | Leve | 8.630 | 0 | 0,00 | 62 | 13 | 46 | 48,04 |
| Kotlin | SOAP | Médio | 17.675 | 0 | 0,00 | 17 | 11 | 47 | 98,39 |
| Kotlin | SOAP | Pesado | 26.624 | 0 | 0,00 | 17 | 10 | 46 | 148,22 |

### Taxa de Erros

A taxa de erros foi **0% em todos os 24 cenários testados**, para ambas as linguagens e todos os níveis de carga. Isso indica que todas as implementações são funcionalmente estáveis dentro dos limites testados, e que as diferenças de desempenho observadas dizem respeito exclusivamente à latência e ao throughput, não à confiabilidade.

### Gráficos — Visão Geral

Os gráficos a seguir comparam todas as tecnologias e linguagens simultaneamente nas três métricas principais.

**Latência média por tecnologia e linguagem:**

![Latência média geral](graficos/todos/01_latencia_media.png)

**P95 por tecnologia e linguagem:**

![P95 geral](graficos/todos/02_p95.png)

**Requisições por segundo:**

![RPS geral](graficos/todos/03_requests_per_second.png)

**Taxa de erro comparativa:**

![Taxa de erro geral](graficos/todos/04_taxa_erro_comparativo.png)

O gRPC se destaca com as menores latências em ambas as linguagens, seguido pelo GraphQL. O SOAP Java apresentou colapso severo na carga pesada, com latência média de 389ms e P95 de 2200ms. O throughput foi equivalente entre todas as tecnologias nas cargas leve e média, divergindo na pesada devido à saturação do SOAP Java.

### Gráficos — Java por nível de carga

**Latência média — Java:**

![Latência média Java](graficos/todos/latencia_media_java.png)

**P95 — Java:**

![P95 Java](graficos/todos/p95_java.png)

**RPS — Java:**

![RPS Java](graficos/todos/rps_java.png)

**Taxa de erro — Java:**

![Taxa de erro Java](graficos/todos/taxa_erro_java.png)

Em Java, o comportamento foi consistente entre REST, GraphQL e gRPC em carga leve e média. O ponto crítico foi o SOAP na carga pesada: enquanto as outras tecnologias mantiveram latências abaixo de 55ms, o SOAP saltou para 389ms de média e P95 de 2200ms, além de registrar queda no throughput (123 RPS contra ~149 das demais).

### Gráficos — Kotlin por nível de carga

**Latência média — Kotlin:**

![Latência média Kotlin](graficos/todos/latencia_media_kotlin.png)

**P95 — Kotlin:**

![P95 Kotlin](graficos/todos/p95_kotlin.png)

**RPS — Kotlin:**

![RPS Kotlin](graficos/todos/rps_kotlin.png)

**Taxa de erro — Kotlin:**

![Taxa de erro Kotlin](graficos/todos/taxa_erro_kotlin.png)

Em Kotlin, o comportamento geral foi mais uniforme. O SOAP Kotlin se saiu bem melhor que o Java na carga pesada (17ms vs 389ms), mantendo estabilidade em todos os níveis. O REST Kotlin apresentou latência elevada (90ms) na carga leve, normalizando para ~22ms no médio e ~24ms no pesado — comportamento atribuído ao tempo de aquecimento da JVM (warm-up) no início do teste.

### Gráficos — Por nível de carga individual

**Java — Carga Leve:**

![Latência leve Java](graficos/java/leve/01_latencia_media.png)
![P95 leve Java](graficos/java/leve/02_p95.png)
![RPS leve Java](graficos/java/leve/03_requests_per_second.png)

**Java — Carga Média:**

![Latência média Java](graficos/java/medio/01_latencia_media.png)
![P95 médio Java](graficos/java/medio/02_p95.png)
![RPS médio Java](graficos/java/medio/03_requests_per_second.png)

**Java — Carga Pesada:**

![Latência pesada Java](graficos/java/pesado/01_latencia_media.png)
![P95 pesado Java](graficos/java/pesado/02_p95.png)
![RPS pesado Java](graficos/java/pesado/03_requests_per_second.png)

**Kotlin — Carga Leve:**

![Latência leve Kotlin](graficos/kotlin/leve/01_latencia_media.png)
![P95 leve Kotlin](graficos/kotlin/leve/02_p95.png)
![RPS leve Kotlin](graficos/kotlin/leve/03_requests_per_second.png)

**Kotlin — Carga Média:**

![Latência média Kotlin](graficos/kotlin/medio/01_latencia_media.png)
![P95 médio Kotlin](graficos/kotlin/medio/02_p95.png)
![RPS médio Kotlin](graficos/kotlin/medio/03_requests_per_second.png)

**Kotlin — Carga Pesada:**

![Latência pesada Kotlin](graficos/kotlin/pesado/01_latencia_media.png)
![P95 pesado Kotlin](graficos/kotlin/pesado/02_p95.png)
![RPS pesado Kotlin](graficos/kotlin/pesado/03_requests_per_second.png)

## Conclusão

Os testes de carga demonstraram diferenças expressivas de desempenho entre as tecnologias, especialmente sob alta concorrência.

O **gRPC** foi o melhor em desempenho absoluto nas duas linguagens: 3ms de latência média e P95 de 6ms na carga pesada. A serialização binária via Protocol Buffers e o transporte via HTTP/2 eliminam o overhead de parsing textual. A contrapartida é a maior complexidade de implementação — definição de contratos `.proto`, geração de stubs e configuração do servidor gRPC. Para microsserviços internos onde performance é crítica, é a escolha mais eficiente.

O **GraphQL** ficou em segundo lugar, com latências entre 5–6ms na carga pesada. Além do bom desempenho, trouxe a vantagem semântica de permitir que o cliente defina exatamente os campos desejados, evitando over-fetching. A implementação foi mais trabalhosa que REST — exige a definição de um schema `.graphqls` e resolvers por entidade — mas o resultado é uma API expressiva e eficiente. É especialmente útil em aplicações onde os clientes têm necessidades de dados variadas.

O **REST** apresentou desempenho moderado e estável. Com latência média entre 21–51ms em Java e 22–24ms em Kotlin na carga pesada, ficou bem acima do gRPC e GraphQL, mas manteve comportamento previsível e sem colapsos. Foi a tecnologia mais simples de implementar com Spring Boot e a mais familiar. Para APIs públicas ou integrações onde a facilidade de uso e adoção ampla importam mais que latência mínima, continua sendo a escolha mais prática.

O **SOAP** apresentou o pior resultado geral. Em Java, a carga pesada provocou um colapso severo: latência média de 389ms, P95 de 2200ms e queda de throughput para 123 RPS. A versão Kotlin se comportou melhor (17ms na carga pesada), sugerindo que a implementação Java do parser XML foi menos eficiente sob alta concorrência. De qualquer forma, o overhead do XML — tanto no tamanho das mensagens quanto no custo de serialização — torna o SOAP a pior opção para sistemas com alta demanda. Seu uso se justifica hoje apenas na integração com sistemas legados que já o adotam.

Quanto às linguagens, **Java e Kotlin apresentaram desempenho praticamente idêntico** em gRPC e GraphQL. As diferenças observadas em REST e SOAP nas cargas leve/média são explicadas pelo warm-up da JVM, não por características intrínsecas das linguagens. Dado que Kotlin compila para a mesma JVM e utiliza os mesmos frameworks Spring Boot, a convergência dos resultados era esperada.