# Desafio Técnico - Desenvolvedor Backend Sênior | Iplan Rio

<div style="text-align: center;">
<img src="./src/logo-carteira-digital.png" alt="logo-carteira-digital">
</div>

## API Carteira Digital

Seja bem vindo à fase de teste da API da Carteira Digital, uma aplicação responsável por centralizar diferentes documentos do cidadão, realizar recargas de cartões de benefícios e também consultar saldo do vale transporte, tudo em tempo real! 😲  

Para testar é preciso ter usuário e senha, mas não se preocupe! Por ser público, todos podem fazer o cadastro e avaliar essa aplicação!  

## Como a aplicação funciona

<div style="text-align: center;">
<img src="./src/pipeline-backend.png" alt="pipeline-backend">
</div>


## Vamos fazer um teste?

### Iniciando o repositório

No terminal **bash** do seu computador execute os comandos a seguir:

1. 👨‍💻 Clone o repositório:  
`git clone https://github.com/jeantorre/desafio-senior-backend-developer`

2. 👩‍💻 Vá até o repositório:  
`cd desafio-senior-backend-developer`

### Inicializando a aplicação

Primeiro é necessário garantir que esteja rodando o [Docker Desktop](https://www.docker.com/products/docker-desktop/) em segundo plano.  

Antes de prosseguir... você sabia que neste momento já foram criados dois ambientes? 🤔  
Isso mesmo, ambientes de *desenvolvimento* e de *produção*. São bancos de dados distintos, com usuários e portas de acesso também separada, garantindo ambientes seguros para suas propostas.

Veja a diferença e escolha o que faz mais sentido neste momento:

* **Desenvolvimento**: um ambiente para testar e desenvolver novas funcionalidades, *endpoints* e o que mais desejar. Com um *reload* automático, as alterações no código já refletem na aplicação.  
Possui uma inserção automática de usuários, tipos de transporte, tipos de transação e alguns documentos e suas relações com usuários teste, sendo possível já testar os *endpoints* bastando apenas fazer o login para ter acesso ao token. E não se preocupe com qualquer alteração que fizer, a exclusão e reinclusão dos dados no banco é feita sempre que existe uma mudança no código!  

* **Produção**: ambiente onde as inserções de dados como usuários e as associações de documentos entre eles precisa ser feita de forma manual pelo usuário final. As informações inseridas e todas suas alterações são mantidas no banco.


Os comandos a seguir precisam ser realizados na pasta raiz do projeto.  

| Comandos | Desenvolvimento | Produção |
| - | - | - |
| Inicialização | ./scripts/start-dev.sh | ./scripts/start-prod.sh |
| Encerramento | 1 - pressione CTRL+C para parar o container<br>2 - ./scripts/stop-dev.sh | ./scripts/stop-prod.sh |

### Acessando o banco de dados

Essa parte é opcional, logo se desejar fazer a leitura diretamente no banco de dados, escolha o gerenciador de sua preferência e configure da seguinte maneira:  

- **Tipo de conexão**: banco PostgreSQL

| Configurações | Desenvolvimento | Produção |
| - | - | - |
| Host | localhost | localhost |
| Database | db-desafio-dev | db-desafio-prod |
| Porta | 5433 | 5434 |
| Usuário | usuario_dev | usuario_prod |
| Senha | dev123 | prod123 |

Caso prefira testar diretamente os *endpoints* pelo **Swagger UI** é só prosseguir para a [próxima etapa](#acessando-os-endpoints).  

#### Diagrama Entidade-Relacionamento
<div style="text-align: center;">
<img src="./src/rl-database.png" alt="pipeline-backend">
</div>

### Acessando os *endpoints*

É possível testá-los em ferramentas específicas que interajam com API ou diretamente pelo **Swagger UI**.  
Na documentação que é gerada automaticamente pela FastAPI são encontradas todas as descrições de cada *endpoint* de forma bem clara e suas respectivas variáveis para execução, quando aplicável.

|  | Desenvolvimento | Produção |
| - | - | - |
| Local de teste | http://localhost:8090/docs/ | http://localhost:8091/docs/ |

No ambiente de desenvolvimento já é criado usuário de teste de forma automática, ao iniciar a aplicação, com as seguintes credenciais para o *endpoint* `/auth/login`:

- username: teste1@teste.com
- password: teste1234

Como resposta são retornados bearer tokens, onde:
``` json
{

  "token_acesso": "token_que_expira_em_30_minutos",
  "token_refresh": "token_que_expira_em_7_dias",
}
```

Apenas os *endpoints* `/auth/login` e `/usuario/registrar` podem ser utilizados sem o token de acesso. Todos os outros são preciso autorização que pode ser passada no **Swagger UI**, que está localizada na parte superior identificada por um cadeado escrito *Authorize*, ou na ferramenta de interação com API de sua escolha e na seção *Auth* como "Bearer Token".  

<div style="
  margin: 1em auto;
  padding: 1em;
  border-left: 4px solid #ccc;
  background-color: #f9f9f9;
  font-style: italic;
  text-align: center;
  max-width: 600px;
">
<b>Observação</b>: Lembre-se de criar seu próprio usuário e senha antes de testar o ambiente de produção, ok? Após isso execute os mesmos passos explicados anteriormente.
</div>


#### Carteirito, o Chatbot

Para uma maior interação entre você e nossa aplicação, apresento o "Carteirito, o Chatbot".

<div style="text-align: center;">
<img src="./src/cateirito-chatbot.png" alt="pipeline-backend">
</div>

Aproveite este *endpoint* e faça alguma das perguntas abaixo:

- "Olá"
- "Qual seu nome?"
- "Pode verificar meu saldo?"
- "Meu VT serve em quais transportes?"
- "Tchau"


### Testes automatizados

Para esta aplicação foi desenvolvido um `hook` para ambiente local que está associado ao `.pre-commit-config.yaml`.  
O mesmo só funciona em *ambiente de desenvolvimento*, visto que para sua execução é necessário passar o ID no Docker do `backend-desafio-dev`, caso contrário não será permitido "commitar" as alterações, garantindo resiliência das funcionalidades cruciais da aplicação.  

Caso desejar, também é possível rodar os testes unitários de forma manual com o comando a seguir:
```bash
docker exec -it backend-desafio-dev pytest
```

## Documentação Técnica

Para uma leitura em tom mais técnico e explicativo, acesse a seção ["O Projeto"](project.md).

## Desafio Técnico - Desenvolvedor Backend Sênior | Iplan Rio

Esta aplicação foi desenvolvida para o processo seletivo da Iplan Rio. [Clique aqui](https://github.com/prefeitura-rio/desafio-senior-backend-developer) e acesse o repositório original.
