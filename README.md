# Teste Técnico: Aplicação Django para Scraping

## Objetivo

Esta aplicação Django foi desenvolvida para coletar e gerenciar informações de produtos do site [Amigão](https://www.amigao.com). O projeto implementa funcionalidades de scraping, administração de dados e registro histórico.

A extração é feita a partir da URl de uma categoria, como por exemplo: `https://www.amigao.com/apucarana/mercearia-doce/cafe`

Todas as páginas dessas categorias são processadas e dentro delas todos os produtos.

Cada produto irá gerar um "Product" único (através do seu SKU) e a cada vez que o comando for rodado será gerado um novo "History", referindo-se ao estado do produto naquele momento (preços, promoções e afins), dessa forma, criando um histórico de preços para o produto.

---

## Funcionalidades

1. **Modelagem de Dados**
   - **Store**: Representa lojas.
   - **URL**: URLs para scraping associadas a uma loja.
   - **Product**: Produtos coletados.
   - **History**: Histórico de preços e promoções.

2. **Interface Administrativa Django**
   - **Store**: Operações completas (CRUD).
   - **URL**: Operações completas (CRUD).
   - **Product**: Somente leitura.
   - **History**: Somente leitura com filtros:
     - Descrição do produto.
     - Data.
     - Indicador de oferta (`offer`).

3. **Comando Customizado**
   - `python manage.py getprices`:
     - Realiza scraping de todas as URLs cadastradas.
     - Insere ou atualiza produtos no banco de dados.
     - Registra histórico de preços.
     - Trata promoções e mantém a idempotência.

---

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Framework**: Django
- **Banco de Dados**: SQLite
- **Requisições HTTP**: `requests`
- **Parsing HTML**: `BeautifulSoup`

---

## Configuração

### Pré-requisitos

- Python 3.8+

### Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/msotech/amigao-scraper/
    cd amigao_scraper
    ```

2. Crie e ative um ambiente virtual:

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Execute as migrações do banco de dados:

    ```sh
    python manage.py migrate
    ```

5. Crie um superusuário:

    ```sh
    python manage.py createsuperuser
    ```

6. Inicie o servidor de desenvolvimento:

    ```sh
    python manage.py runserver
    ```

## Uso

Com o servidor já iniciado, acesse `http://127.0.0.1:8000/admin` no seu navegador para acessar a interface de administração do Django.

Entre com os dados de superuser criado no passo 5 da `Instalação`.

Adicione uma `Store` e vários `URLs` de categorias do [Amigão](https://www.amigao.com) para serem extraídos futuramente.

Execute o comando `python manage.py getprices` no terminal (garantindo estar na mesma pasta que o arquivo "manage.py") para extrair os dados dos produtos.

### Exemplos de URL

Para facilitar o uso, segue exemplos de URLs para serem adicionadas:

- `https://www.amigao.com/apucarana/mercearia-doce/cafe`
- `https://www.amigao.com/apucarana/mercearia-doce/cha`
- `https://www.amigao.com/apucarana/mercearia-doce/gelatina`
- `https://www.amigao.com/apucarana/mercearia-doce/salgadinhos`
- `https://www.amigao.com/apucarana/alimentos-basicos/arroz`
- `https://www.amigao.com/apucarana/alimentos-basicos/leite-uht`
- `https://www.amigao.com/apucarana/alimentos-basicos/oleo`
- `https://www.amigao.com/apucarana/bebidas/cerveja`
- `https://www.amigao.com/apucarana/bebidas/cha-pronto`
- `https://www.amigao.com/apucarana/bebidas/destilados`

Nota1: Conforme observado acima, sempre envie o link da primeira página, visto que a aplicação é capaz de percorrer todas as páginas.
Caso você mande uma página diferente de primeira, como `https://www.amigao.com/apucarana/bebidas/cerveja?p=5`, o sistema irá automaticamente deletar a paginação e inserir no banco a versão sem query (sem o `?p=5`).

Nota2: Caso você envie uma página inválida, como `https://www.amigao.com/apucarana/bebidas/servejas` o sistema permitirá a inserção no banco, visto que não é feito uma validação aqui, mas o comando `getprices` conseguirá detectar que a página é inválida, avisará nos logs e irá para a próxima URL cadastrada.

## Prints da aplicação

<img src="images/print1.png" alt="Lista de urls" width="500">
<img src="images/print2.png" alt="Produtos extraidos" width="500">
<img src="images/print3.png" alt="Historico dos produtos" width="500">
<img src="images/print4.png" alt="Categorias extraidas." width="500">
