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

O desenvolvimento deste projeto foi conduzido com foco em criar uma aplicação robusta, modular e de fácil reprodutibilidade, tanto em ambientes de desenvolvimento quanto de produção.

A arquitetura foi pensada para permitir escalabilidade e manutenção simplificada, utilizando boas práticas de desenvolvimento, tipagem e documentação de código.

### 🛠️ Ferramentas e Boas Práticas

- **Framework Web**: via [FastAPI](https://fastapi.tiangolo.com/), selecionado devida a sua alta performance, tipagem nativa e documentação automática integrada (Swagger e Redoc)
- **Gerenciamento de ambiente virutal**: via `poetry`.
- **Padronização de código**: com uso de `pre-commit hooks`, incluido:
    - `bandit` - análise de segurança
    - `isort` - organização de *imports*
    - `black` - formatação automática do código
    - `flake8` - verificação de estilo
    - `hook` personalizado, desenvolvido especificamente para este projeto
- **Controle de versão do banco de dados**: via [Alembic](https://alembic.sqlalchemy.org/en/latest/), permitindo o versionamento seguro das migrações do banco de dados.
- **Container e orquestração**: com fornecimento de diferentes configurações de `docker-compose.yml` e `Dockerfile` facilita a replicação de ambientes de desenvolvimento e produção.

### 📖 Documentação Automática

Pela API ter sido construída utilizando o FastAPI, foi gerada uma documentação automática e interativa via **Swagger UI** e **Redoc**. Permitindo um entendimento técnico e de interação de terceiros com os *endpoints* disponíveis.

### 🧱 Estrutura do Projeto

- **CRUD**: funções responsáveis pelas operações de criação, leitura, atualização e remoção de dados
- **Model**: definição das estruturas de dados e modelos relacionais do banco, com tipagem explícita e dicionário de dados 
- **Schema**: validação de dados com Pydantic, garantindo integridade nas trocas entre cliente e servidor
- **Routers**: definição dos *endpoints* da API
- **Utils**: funções utilitárias compartilhadas entre partes da aplicação

### 🔐 Segurança

- **Senhas**: senhas são armazenadas de forma segura no banco de dados, utilizando algorístmos de *hashing*
- **Variáveis de ambiente**: estão centralizadas em arquivos `.env`. Esses arquivos estão incluídos no repositório apenas para facilitar a reprodução local.

### 🦾 Testes Automatizados

Para garantir a qualidade do código e prevenir quebras inesperadas em endpoints críticos, foi desenvolvido um `hook` local associado ao `pre-commit`. Esse hook executa testes automatizados (via `pytest`) sobre os *endpoints* da API, mas somente se o ambiente de desenvolvimento estiver rodando via Docker em segundo plano.

<b>Observação</b>: os testes dependem da execução do ambiente de desenvolvimento. Caso o ambiente de produção esteja ativo, os testes não serão executados, impedindo o commit e promovendo boas práticas de versionamento.

## Documentação Completa

Clique na imagem a seguir a leia a documentação completa.  

<div style="text-align: center;">
<a href="https://jeantorre.github.io/desafio-senior-backend-developer/">
<img src="docs/src/logo-carteira-digital.png" alt="logo-carteira-digital">
</a>
</div>