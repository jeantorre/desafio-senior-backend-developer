# Desafios e Decisões Técnicas/Estratégicas do Projeto

O desenvolvimento deste projeto foi conduzido com foco em criar uma aplicação robusta, modular e de fácil reprodutibilidade, tanto em ambientes de desenvolvimento quanto de produção.

A arquitetura foi pensada para permitir escalabilidade e manutenção simplificada, utilizando boas práticas de desenvolvimento, tipagem e documentação de código.

## 🛠️ Ferramentas e Boas Práticas

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

## 📖 Documentação Automática

Pela API ter sido construída utilizando o FastAPI, foi gerada uma documentação automática e interativa via **Swagger UI** e **Redoc**. Permitindo um entendimento técnico e de interação de terceiros com os *endpoints* disponíveis.

## 🧱 Estrutura do Projeto

- **CRUD**: funções responsáveis pelas operações de criação, leitura, atualização e remoção de dados
- **Model**: definição das estruturas de dados e modelos relacionais do banco, com tipagem explícita e dicionário de dados
- **Schema**: validação de dados com Pydantic, garantindo integridade nas trocas entre cliente e servidor
- **Routers**: definição dos *endpoints* da API
- **Utils**: funções utilitárias compartilhadas entre partes da aplicação

## 🔐 Segurança

- **Senhas**: senhas são armazenadas de forma segura no banco de dados, utilizando algorístmos de *hashing*
- **Variáveis de ambiente**: estão centralizadas em arquivos `.env`. Esses arquivos estão incluídos no repositório apenas para facilitar a reprodução local.

## 🦾 Testes Automatizados

Para garantir a qualidade do código e prevenir quebras inesperadas em endpoints críticos, foi desenvolvido um `hook` local associado ao `pre-commit`. Esse hook executa testes automatizados (via `pytest`) sobre os *endpoints* da API, mas somente se o ambiente de desenvolvimento estiver rodando via Docker em segundo plano.

<div style="
  margin: 1em auto;
  padding: 1em;
  border-left: 4px solid #ccc;
  background-color: #f9f9f9;
  font-style: italic;
  text-align: center;
  max-width: 600px;
">
<b>Observação</b>: os testes dependem da execução do ambiente de desenvolvimento. Caso o ambiente de produção esteja ativo, os testes não serão executados, impedindo o commit e promovendo boas práticas de versionamento.
</div>
