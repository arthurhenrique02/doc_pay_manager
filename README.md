### Tópicos 

:small_blue_diamond: [Requisitos](#Requisitos)

:small_blue_diamond: [Instalando dependencias](#Instalando-dependencias)

:small_blue_diamond: [Configurando ambiente](#Configurando-ambiente)

:small_blue_diamond: [Rodando aplicação](#Rodando-aplicacao)

:small_blue_diamond: [Endpoints](#Endpoints)

:small_blue_diamond: [Tratamento de erro](#Tratamento-de-erro)

:small_blue_diamond: [Segurança de dados](#Seguranca-de-dados)

## Requisitos

### Python 3.12
- [Baixe aqui](https://www.python.org/downloads/)

### PostgresSQL
- [Baixe aqui](https://www.postgresql.org/download/)
- Será necessário criar a instancia do banco de dados; As tabelas serão criadas utilizando o Alembic

## Instalando dependencias
- Basta criar uma virtual enviroment (venv) e utilizar o pip para instalar
```sh
python -m venv venv
source venv/bin/activate  # No windows, use: `venv\Scripts\activate`
pip install -r requirements.txt
```

## Configurando ambiente

- Para a aplicação rodar corretamente, é necessário configurar um arquivo `.env` com os seguintes valores
  -  DB_URL: url que aponta para o banco de dados postgres criado
  -  SECRET_KEY: string hex 32 criada e utilizada para criptografia da senha do user
  -  ALGORITHM: Algoritmo de criptografia utilizado para criptografar a senha do user. Habilitado uso dos algoritmos HS. Para utilizar RS ou algum outro é necessário uma instalação adicional
  -  ACCESS_TOKEN_EXPIRE_MINUTES (não obrigatório. Padrão 30 min): Tempo de expiração do JWT
- Veja o arquivo `.example_env` para um melhor exemplo

## Rodando aplicação
- Para rodar a aplicação é necessário estar com o PostgrelSQL e a .env configurados
```sh
source venv/bin/activate  # No windows, use: `venv\Scripts\activate`
uvicorn main.app:app --port 8000 --reload # O cors está configurado para receber requisições da porta 8000
```

## Endpoints

### Autenticação

Um sistema de autenticação simples apenas para representar como as endpoints principais (procedure) seriam bloqueadas por ela.

#### **POST /auth/token**
Autentica um usuário e gera um token de acesso.

##### Requisição:
```json
{
  "username": "string",
  "password": "string"
}
```
##### Resposta
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```
#### **POST /auth/registry**
Cria um novo usuário

##### Requisição
```json
{
  "username": "string",
  "password": "string",
  "is_superuser": true
}
```

##### Resposta
```json
{
  "username": "string",
  "is_superuser": true
}
```

#### Médicos

Um sistema de adição de médicos para que os mesmos possam ser utilizados nas endpoints principais (procedure).
A ideia é apenas ter dados utilizáveis nas endpoints de procedure e não representar uma tabela real de médicos.

***POST /doctor/registry***
Registra um novo médico
- Necessário existir um usuário para que possa ser inserido ao cadastro

##### Requisição
```json
{
  "name": "string",
  "user_id": 1
}
```

##### Resposta
```json
{
  "id": 1,
  "name": "string",
  "user_id": 1
}
```

#### Pacientes

Um sistema de adição de pacientes para que os mesmos possam ser utilizados nas endpoints principais (procedure).
A ideia é apenas ter dados utilizáveis nas endpoints de procedure e não representar uma tabela real de pacientes.


***POST /patient/registry***
Registra um novo paciente

##### Requisição
```json
{
  "name": "string"
}
```

##### Resposta
```json
{
  "id": 1,
  "name": "string"
}
```

#### Procedimentos

API's principais e com funcionalidades referentes ao desafio.


***POST /procedure/registry***

Cria um novo procedimento médico
- Necessário doutor e paciente existentes na base de dados

##### Requisição
```json
{
  "doctor_id": 1,
  "patient_id": 1,
  "date": "2023-10-01",
  "value": 100.50,
  "payment_status": "paid"
}
```

##### Resposta
```json
{
  "id": 1,
  "doctor_id": 1,
  "patient_id": 1,
  "date": "2023-10-01",
  "value": 100.50,
  "payment_status": "paid"
}
```

***GET /procedure/report/daily***

Obtém um relatório diário de procedimentos para o médico atual ou um médico especificado (em caso de superuser).

- Parâmetros
  - doctor_id (opcional): O ID do médico.

##### Resposta
```json
[
  {
    "id": 1,
    "doctor_id": 1,
    "patient_id": 1,
    "date": "2023-10-01",
    "value": 100.50,
    "payment_status": "paid"
  }
]
```

***POST /procedure/report/glossed***

Obtém um relatório de procedimentos glosados dentro de um intervalo de datas especificado.

##### Requisição
```json
{
  "start": "2023-10-01",
  "end": "2023-10-31"
  "doctor_id: int | null
}
```
OBS.: doctor_id é um parâmetro opcional caso o usuário deseje pesquisar por suas glosas ou o superusuário pesquise pelo dele ou de algum outro médico.

##### Resposta
```json
[
  {
    "id": 1,
    "doctor_id": 1,
    "patient_id": 1,
    "date": "2023-10-01",
    "value": 100.50,
    "payment_status": "glossed"
  }
]
```

***GET /procedure/report/financial/{doctor_id}***

Obtém um relatório financeiro de procedimentos para um médico específico.

##### Requisição
`doctor_id: O ID do médico.`

##### Resposta
```json
[
  {
    "total_value": 1000.00,
    "procedures": 10,
    "status": "paid"
  },
  {
    "total_value": 500.00,
    "procedures": 5,
    "status": "pending"
  }
]
```

### Tratamento de erro

#### Para API de autenticação (auth)

Não foi focado o tratamento de erro para essa API por se tratar apenas de uma API para inserção de dados e utilização nas API's principais. Contudo, ainda temos:
  - Validação de keys, como: username, senha e token
  - Validação de existencia de usuário

#### Para API de médicos (doctor)

Não foi focado o tratamento de erro para essa API por se tratar apenas de uma API para inserção de dados e utilização nas API's principais. Contudo, ainda temos:
  - Checagem de tipo enviado na key `name`, permitindo apenas string
  - Checagem de id do usuário, validando se o mesmo existe ou não
  - As checagens ocorrem através do Pydantic

#### Para API de pacientes (patient)

Não foi focado o tratamento de erro para essa API por se tratar apenas de uma API para inserção de dados e utilização nas API's principais. Contudo, ainda temos:
  - Checagem de tipo enviado na key `name`, permitindo apenas string
  - A checagem ocorre através do Pydantic

#### Para API de procedimentos médicos

  - Utilizando a api de auth para permitir que apenas usuário logados tenham acessos as endpoints
  - Validação de tipo de dados através do pydantic
  - Validação de existência de id's enviados (FK's) de médicos e pacientes através do pydantic. Utilizando validators
  - Em caso do usuário logado ser superuser, o mesmo pode inserir/visualizar qualquer dado
  - Caso não seja superuser, insere e visualiza apenas os dados do usuário logado. Mesmo que envie outro id, receberá apenas seus dados.
  - Em caso de erro, retorna um mensagem através do próprio pydantic (http) ou uma mensagem customizada da API

### Segurança de dados

A segurança dos dados é dada a partir do login do usuário. Garantindo que apenas acessem dados relacionados aos mesmos, em caso de não superusuários




