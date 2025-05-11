# Desafio Técnico - Desenvolvedor Backend Sênior | Iplan Rio

## API Carteira Digital

Seja bem vindo a fase de teste da API da Carteira Digital, uma aplicação responsável por centralizar diferentes documentos do cidadão, realizar recargas de cartões de benefícios e também consultar saldo do vale transporte, tudo em tempo real! 😲  

## Iniciando o repositório

1. Clone o repositório:  
`git clone https://github.com/jeantorre/desafio-senior-backend-developer`

2. Vá até o repositório:  
`cd desafio-senior-backend-developer`

### Inicializando a aplicação

Primeiro é necessário garantir que esteja rodando o [Docker Desktop](https://www.docker.com/products/docker-desktop/) em segundo plano.  

3. Escolha o ambiente que deseja e utiulize algum dos comandos a seguir. Os mesmos precisam ser realizados na raíz do projeto.  

| Comandos | Desenvolvimento | Produção |
| - | - | - |
| Inicialização | ./scripts/start-dev.sh | ./scripts/start-prod.sh |
| Encerramento | ./scripts/stop-dev.sh | ./scripts/stop-prod.sh |

4. É possível testá-los em ferramentas específicas que interagem com API ou diretamente pela documentação da API. 

|  | Desenvolvimento | Produção |
| - | - | - |
| Local de teste | http://localhost:8090/docs/ | http://localhost:8091/docs/ |

## Desafios e Decisões Técnicas/Estratégicas do Projeto

<div style="text-align: center;">
<img src="docs/src/pipeline-backend.png" alt="pipeline-backend">
</div>

No desenvolvimento deste desafio foi pensado, e realizado, uma aplicação com lógica e arquitetura que pode ser reproduzida em ambientes de "desenvolvimento" e "produção" para empresas de tecnologia.  

Com um repositório de estrutura modular, é possível garantir fácil manutenção e também de fácil escalabilidade, se aplicável. Além disso pode ser encontrado `doc hint` e `type hint` em todo o desenvolvimento.  

Para gerenciamento de ambiente virtual é utilizado o `poetry` e para padronizar todo o repositório foram utilizados `hooks` padrões, como por exmeplo:

- Bandit
- Isort
- Black
- Flake8
- E também `hook` desenvolvido localmente para este projeto.

Para garantir que todos consigam replicar essa aplicação com facilidade, são utilizados diferentes `docker-compose.yml` e `Dockerfile`.


### Estrutura

#### CRUD
São encontradas as funções relacionadas ao CRUD das rotas.  

#### MODEL
São encontrados dodos os modelos das tabelas que são criadas no banco de dados, com o dicionário de dados e "tipagem" de cada coluna.  

#### SCHEMA
Modelo `pydantic` que garante validação dos dados em todas as transferência entre cliente <-> banco de dados <-> cliente.  

#### ROUTER
São encontradas todos os *endpoints* desenvolvidos.

#### UTILS
São encontrados código de uso em comum no repositório.

### Segurança

Dados sensíveis, como as senhas, são salvas no banco de dados após passar pelo processo de *hashing*.    
As variáveis de ambiente `(.env)` foram expostas para facilitar a reprodutibilidade da aplicação

### Testes Automatizados

Devida a complexidade na estrutura desenvolvida de ambiente de desenvolvimento e produção, foi criado `hook` local, e associado ao `pre-commit` para garantir testes unitários em rotas cruciais antes de "commitar" qualquer atualização.  Este teste só roda em ambiente de desenvolvimento quando o mesmo está rodando em segundo plano pelo Docker, pois os testes desenvolvidos utilizam os *endpoints*.  
Dessa forma se o ambiente de produção estiver ligado, ao rodar o `pre-commit` não achará as funções do `pytests`, impossibilitando o commit do código.

## Documentação Completa

Clique na imagem a seguir a leia a documentação completa.  

<div style="text-align: center;">
<a href="https://jeantorre.github.io/desafio-senior-backend-developer/">
<img src="docs/src/logo-carteira-digital.png" alt="logo-carteira-digital">
</a>
</div>