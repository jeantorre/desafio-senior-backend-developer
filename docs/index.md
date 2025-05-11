# Desafio Técnico - Desenvolvedor Backend Sênior | Iplan Rio

<div style="text-align: center;">
<img src="./src/logo-carteira-digital.png" alt="logo-carteira-digital">
</div>

## API Carteira Digital

Seja bem vindo a fase de teste da API da Carteira Digital, uma aplicação responsável por centralizar diferentes documentos do cidadão, realizar recargas e também consultar saldo do vale transporte, tudo em tempo real!  

Para testar é preciso ter usuário e senha, mas não se preocupe... Por ser uma aplicação gratuita, todos podem fazer o cadastro e aproveitar mais esse benefício que está sendo entregue a população!  

## Como a aplicação funciona 

<div style="text-align: center;">
<img src="./src/pipeline-backend.png" alt="pipeline-backend">
</div>


## Vamos fazer um teste?

### Iniciando o repositório

Clone o repositório:  
`git clone https://github.com/jeantorre/desafio-senior-backend-developer` 

Vá até o repositório:
`cd desafio-senior-backend-developer`

### Inicializando a aplicação 

Primeiro é necessário garantir que esteja rodando o [Docker desktop](https://www.docker.com/products/docker-desktop/).  

Neste momento já foram criados dois ambientes: o de *produção* e o de *desenvolvimento*. São bancos de dados distintos, com usuários e portas de acesso também separada, garantindo ambientes seguros para suas propostas.

Veja a diferença e escolha o que faz mais sentido:
* Desenvolvimento - um ambiente para testar e desenvolver novas *features*. Com uma inserção automática de usuários, tipos de transporte, tipos de transação e alguns documentos, é possível já testar os *endpoints* bastando apenas fazer o login. Este

Os comandos a seguir precisam ser realizados na raíz do projeto.  

Comandos | Desenvolvimento | Produção 
- | - | -
Inicialização | ./script/start-dev.sh | ./script/start-prod.sh
Encerramento | ./script/stop-dev.sh | | ./script/stop-prod.sh