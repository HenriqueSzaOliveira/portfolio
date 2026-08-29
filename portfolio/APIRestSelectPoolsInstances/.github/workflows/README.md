# Workflows do repositório

Este diretório guarda os workflows do GitHub Actions.

**Mova a pasta .github para a raiz do repositório para funcionar o actions**

## CI

O workflow de CI está em `ci.yml` e valida:

- instalação das dependências
- execução da suíte de testes
- cobertura mínima de 95%
- falha se algum teste quebrar

## CD

O workflow de CD está em `cd.yml` e, após a validação na branch `main`, faz:

- testes novamente
- build da imagem Docker
- login no Docker Hub
- publicação da imagem com as tags `latest` e `sha`

## Secrets obrigatórios no GitHub

Para o deploy no Docker Hub, configure estes secrets no repositório:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

### Como criar as secrets

1. Acesse o repositório no GitHub.
2. Vá em `Settings` → `Secrets and variables` → `Actions`.
3. Clique em `New repository secret`.
4. Crie a secret `DOCKERHUB_USERNAME` com o seu nome de usuário do Docker Hub.
5. Crie a secret `DOCKERHUB_TOKEN` com o token gerado no Docker Hub.

### Como gerar o token no Docker Hub

1. Acesse https://hub.docker.com
2. Faça login.
3. Vá em `Account Settings` → `Security`.
4. Clique em `New Access Token`.
5. Copie o valor gerado.
6. Cole esse valor na secret `DOCKERHUB_TOKEN`.

> Os nomes das secrets precisam ser exatamente `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` para que o workflow funcione.

## Observação importante

O GitHub Actions reconhece workflows somente em `.github/workflows` na raiz do repositório. A lógica da aplicação pode rodar dentro da pasta do projeto, mas o arquivo do workflow precisa ficar na raiz do repositório para funcionar.
