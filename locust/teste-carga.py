from locust import HttpUser, SequentialTaskSet, task, events
from urllib.parse import quote

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--request-name",
        type=str,
        env_var="REQUEST_NAME",
        default="/api/[link]",
        help="Nome exibido no relatório do Locust"
    )

class ExtracaoSequencial(SequentialTaskSet):

    links = [
        "https://unifor.br/web/graduacao/medicina",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/c/covid-19",
        "https://www.gov.br/pt-br",
        "https://g1.globo.com/sp/campinas-regiao/noticia/2026/05/09/produtos-ype-nao-recomendados-pela-anvisa-10-pontos-para-entender-o-caso.ghtml",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hantavirose",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/aids-hiv",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/autismo",
        "https://www.gov.br/saude/pt-br/assuntos/saude-com-ciencia",
        "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/s/sindrome-de-burnout",
        "https://g1.globo.com/saude/noticia/2026/05/09/brasil-casos-de-hantavirus-no-ano-sem-elo-com-genotipo-ligado-ao-surto-em-cruzeiro-entenda-contexto.ghtml"
    ]


    @task
    def executar(self):
        request_name = self.user.environment.parsed_options.request_name
        
        for link in self.links:

            # encoded_link = quote(link, safe='')

            self.client.get(
                f"/api/{link}",
                name=request_name
            )

class WebsiteUser(HttpUser):
    tasks = [ExtracaoSequencial]