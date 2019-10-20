## CEDERJ 2019 - MIQUÉIAS DERNIER E VINICIUS ZANOVELLI (ORIENTADOR ALTOBELLI DE BRITO)

COLETA DIRECIONADA DE DADOS DA _INTERNET_ ATRAVÉS DE MECANISMOS 
DE AUTOMAÇÃO (_WEB SCRAPING_) COM FOCO EM ASPECTOS DA COMPOSIÇÃO 
E DA FORMULAÇÃO DE MEDICAMENTOS

Este repositório contém uma implementação de _software_ para coleta 
direcionada e automatizada de dados da _internet_ e uma aplicação
desta implementação voltada para a pesquisa de aspectos específicos
da composição e da formulação de medicamentos.

<br />

## Como instalar (console)

Crie um diretório para a solução e o acesse:

```console
mkdir scraping
cd scraping
``` 

Clone o repositório no caminho corrente:

```console 
git clone https://github.com/altobellibm/CEDERJ_2019_MIQUEIAS_DERNIER_E_VINICIUS_ZANOVELLI-.git .
``` 

Crie um ambiente virtual (exemplo usando _virtualenv_):

```console 
pip install virtualenv
virtualenv scraping
```

Alterne para um ambiente virtual (exemplo usando _virtualenv_):

```console 
souce scraping/bin/activate  # Linux/MacOS
```
```console
scraping\Scripts\activate  # Windows
```

Instale o pacote Python (e todas as dependências) para _scraping_:

```console
cd packages
python setup.py install
```

A partir deste ponto a biblioteca de _scraping_ (e todas
as suas dependências) estarão disponíveis no seu ambiente virtual.

<br />

## Como configurar a aplicação (console)

1. Verifique se você possui as versões dos drivers necessários
compatíveis com as versões dos navegadores de _internet_ 
instalados no seu sistema (vide Requisitos);

2. Com base no diretório raiz do repositório, verifique se
os parâmetros de inicialização da aplicação farmacêutica
apontam para as versões corretas dos drivers:

    * Abra o arquivo 
    ``./applications/pharmaceutical/pharmaceutical.py``
    no seu editor ou IDE favoritos;
    
    * Verifique os caminhos dos drivers nos parâmetros 
    ``geckodriver`` e ``chromedriver``:
    
```python
...
geckodriver='../../vendor/geckodriver/0.24.0/',          # Firefox 65+
chromedriver='../../vendor/chromedriver/76.0.3809.68/',  # Chrome 76
...
```

`Nota: Você pode utilizar caminhos relativos (como no exemplo acima)
ou absolutos do seu sistema de arquivos.`

<br />

## Como executar a aplicação (console)

Execute o arquivo .py principal da aplicação diretamente com Python:
```console
python ./applications/pharmaceutical/pharmaceutical.py
```

Onde o ``.`` representa o caminho do diretório do repositório clonado
no sistema de arquivos local.

<br />

## Como usar a biblioteca (para desenvolvedores)

Após a instalação do pacote a biblioteca estará disponível
para importação através da instrução ``import scraping`` e
pode ser implementada com poucas linhas de código conforme o
exemplo abaixo:

```python
from scraping import engine as microframework

scrap = microframework.Bot(dict(
    charset='utf-8',
    parser='html5lib',
    filesystem=dict(
        input='./input/',
        output='./output/',
        logs='./logs/',
        drivers=dict(
            geckodriver='{vendor}/geckodriver/{version}/',
            chromedriver='{vendor}/chromedriver/{version}/',
        ),
    ),
    verbose=True,
    debug=False,
))

scrap.run()
``` 

Onde ``{vendor}`` representa o caminho no sistema de arquivo local
para o diretório com os drivers dos navegadores de _internet_ e
``{version}`` representa o diretório com a versão específica instalada
no sistema.

``
IMPORTANTE: Para garantir que a biblioteca será capaz de resolver 
o caminho dos drivers corretamente para todos os sistemas operacionais
suportados, os diretórios dos drivers precisam respeitar a estrutura 
descrita acima, contendo ainda subdiretórios definindo os diferentes 
sistemas operacionais suportados (e suas arquiteturas) contendo, 
por sua vez, os binários dos respectivos drivers com seus nomes originais 
mantidos e sem mais subdiretórios.
`` 

A estrutura final do caminho dos drivers deverá se parecer com:
```
{vendor}
├───chromedriver
│   └───{version}
│       ├───linux64
│       ├───mac64
│       └───win32
└───geckodriver
    └───{version}
        ├───linux32
        ├───linux64
        ├───mac64
        ├───win32
        └───win64
```

Os caminhos de ``logs`` e ``output`` definidos na inicialização da biblioteca
serão automaticamente criados e o caminho de ``input`` precisa existir com
um ou mais _scripts_ de _scraping_ conforme ilustrado abaixo:

Arquivo ``script1.py``
```python
def script1(api):
    # code goes here
    pass
```

Arquivo ``script2.py``
```python
def script2(api):
    # code goes here
    pass
```

Não há limite para o número de _scripts_ (representando uma variável de 
entrada cada) no caminho de ``input`` e cada arquivo deve implementar 
uma função com o mesmo nome do arquivo que a contém para ser utilizado
como _trigger_ (gatilho/entrada) para a biblioteca (ou seja, a execução 
do _script_ será iniciada através de uma chamada a esta função).

``IMPORTANTE: Para evitar conflitos e respeitar as especificações da
linguagem de programação utilizada (Python), os nomes de arquivos e, 
por consequência, suas funções de gatilho devem respeitar as convenções
de nome da linguagem e não podem ser nomes de bibliotecas ou pacotes
nativos ou instalados no ambiente (por exemplo, mas não se limitando a:
os, sys, math, scraping, requests).``

Nota: a variável ``api`` recebida como parâmetro na função _trigger_ de
cada _script_ é uma instância da API de _Scraping_ fornecida pela
biblioteca da solução. Para mais informações consulte os exemplos
fornecidos. 

#### Demonstração e outros exemplos (para desenvolvedores)

Além da aplicação (farmacêutica) principal, duas outras aplicações
simples são disponibilizadas para (1) demonstração dos recursos
da biblioteca e (2) exemplificação de outros casos de uso. 

Para executá-las, configure as aplicações da mesma maneira feita para
a aplicação principal e execute o respectivo arquivo .py principal de 
cada aplicação diretamente com Python:

* Demonstração de uso da API da biblioteca:
```console
python ./applications/demo/demo.py
```

* Exemplos de outros casos de uso da biblioteca:
```console
python ./applications/examples/examples.py
```

Para melhor compreensão do uso da biblioteca, consulte os arquivos de 
_script_ no caminho de ``input`` de cada uma das aplicações acima. Por padrão:

``./applications/demo/input/`` <br />
``./applications/examples/input/``

*Onde, novamente, o ``.`` representa o caminho do diretório do repositório 
clonado no sistema de arquivos local.

<br />

## Como remover a solução

Exclua os arquivos e diretórios da solução e desinstale a biblioteca do 
seu ambiente:

```console
pip uninstall scraping
```

<br />

## Requisitos

Para executar os códigos disponibilizados neste repositório
você precisa de um ambiente Python devidamente configurado
no seu sistema operacional preferido (Linux, Mac ou Windows)
e precisa se certificar de que as versões dos navegadores
de internet instalados sejam compatíveis com as versões dos
respectivos drivers (listados abaixo).

As dependências de bibliotecas serão resolvidas automaticamente
durante a instalação do pacote de _scraping_.

##### Linguagens de programação:

* [Python 3.7.4](https://www.python.org/)

##### Bibliotecas utilizadas:

* [Requests 2.22.0](https://2.python-requests.org/en/master/)
* [Beautiful Soup 4.8.0](https://www.crummy.com/software/BeautifulSoup/)
* [Selenium 4.0.0a1](https://www.seleniumhq.org/)
* [html5lib 1.0.1](https://html5lib.readthedocs.io/en/latest/)
* [lxml 4.4.1](https://lxml.de/)
* [pandas 0.22.0](https://pandas.pydata.org/)

##### Dependências de drivers:

* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* [Chromedriver](https://chromedriver.chromium.org/downloads)
