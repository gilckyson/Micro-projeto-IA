# 🎮 Gerador de: Piores Desculpas Dramáticas do Cenário
> É uma Aplicação Web de entretenimento que utiliza Inteligência Artificial (Gemini) para transformar motivos simples em desculpas extremamente dramáticas, exageradas e criativas, permitindo o armazenamento em histórico e o compartilhamento dos resultados, proporcionando diversão ao usuário.

## 👥 Integrantes:
1. Rafaela
2. Gilkyson Gabriel
3. Diogo Emanuel
4. Victor Gabriel
5. Lion César

## 🚀 Tecnologias:
Python 3.11
FastAPI 0.104
Jinja2 3.1
TailwindCSS 3.3
Gemini API 1.5

## 📦 Como Instalar:

1. Clone o repositório;
2. Crie arquivo .env com sua API key;
3. Instale dependências: `uv sync`
4. Rode: `uv run uvicorn main:app --reload`
5. Acesse: http://localhost:8000

## 🎯 Funcionalidades:
I. Funcionalidades de Lógica do Servidor 
(Back-end)

1- Geração de Conteúdo IA: Função central que utiliza o SDK oficial da Gemini para receber o prompt do usuário e gerar a desculpa personalizada (título, texto e pontuação de drama).

2- Cálculo da Pontuação de Drama: Implementação de lógica de Programação Orientada a Objetos (POO) para extrair e classificar a pontuação de drama da resposta da IA em níveis (Baixo, Médio, Alto, Cósmico).

3- Gerenciamento de Requisições: O framework FastAPI gerencia as rotas (incluindo o POST para /gerar), processa os dados de formulário e renderiza os templates HTML com os resultados via Jinja2.

4- Persistência de Sessão: Armazena dados temporários (como o histórico de desculpas) na sessão do usuário.

5-Configuração Segura de Ambiente: Carrega a chave da API (GEMINI_API_KEY) do arquivo .env para o servidor, garantindo a segurança e a proteção de credenciais.

6- Código Defensivo e Estabilidade: Implementação de rotinas de Descoberta Dinâmica de Modelo (genai.list_models()) e tratamento de exceções (try...except) para garantir que a aplicação funcione mesmo diante de falhas de permissão (403) ou cota (429) da API externa.

II. Funcionalidades da Interface (Front-end)

1- Seleção de Motivo: Permite escolher o tipo de catástrofe pessoal em uma lista predefinida.

2- Campo "Outro" Dinâmico: Exibe um campo de texto adicional via JavaScript quando a opção "Outro" é selecionada, permitindo a descrição detalhada do problema 

3-Estado de Loading: Desabilita o botão de envio e exibe um spinner de carregamento e uma mensagem informativa durante a espera pela resposta da IA (melhoria da experiência do usuário, UX).

4-Exibição Formatada do Resultado: Apresenta a desculpa gerada, o Nível de Drama e a pontuação final de forma clara e visualmente hierarquizada.

5- Ações de Compartilhamento: Oferece botões rápidos para copiar o texto da desculpa ou compartilhá-lo em plataformas externas (ex: WhatsApp).

6- Histórico de Desculpas: Mantém e exibe um registro das desculpas geradas durante a sessão de uso.

## 📸 Screenshots:
![IMG-20251216-WA0008](https://github.com/user-attachments/assets/a722e88d-1a76-4510-965f-8eb36f6629f7)
![IMG-20251216-WA0011](https://github.com/user-attachments/assets/c4e7aebe-9dde-4fef-bd60-75617e9f32ca)
![IMG-20251216-WA0012](https://github.com/user-attachments/assets/ce29ed92-60a1-4df1-bcb2-cc6e09342d07)
![IMG-20251216-WA0010](https://github.com/user-attachments/assets/b2ce6def-618f-44b7-a88b-f88c7ff8fe0b)
![IMG-20251216-WA0009](https://github.com/user-attachments/assets/c05e2754-0f88-4672-9176-8bf30ca66215)
![IMG-20251216-WA0013](https://github.com/user-attachments/assets/a69cd3be-21e9-4a16-b177-0d5c95dea710)

## 🎥 Demo:
https://youtu.be/8W8ioGj8r1k?si=EHkuLhN19zGufWX2

## 🤔 Desafios e Aprendizados:
O desenvolvimento do projeto enfrentou dois desafios críticos. O primeiro foi de Configuração de Ambiente no Windows, onde o servidor Uvicorn falhava ao ser executado devido à política de segurança padrão do PowerShell (ExecutionPolicy). A solução exigiu a elevação temporária do nível de segurança para RemoteSigned via modo Administrador para permitir a ativação do ambiente virtual. O segundo e maior desafio foi garantir a Estabilidade da Integração com a Gemini API, enfrentando erros de permissão (403) e limite problema foi a migração completa para o SDK (Software Development Kit) oficial da Google GenAI. A partir disso, foi possível implementar a Descoberta Dinâmica de Modelos (usando genai.list_models() para encontrar um modelo compatível) e um código defensivo (try...except) que trata falhas externas de forma elegante, convertendo erros de API em respostas HTTP 500 informativas para o usuário

Lição Aprendida: O projeto reforçou o valor da Robustez de Código e da Configuração Defensiva. É fundamental não apenas escrever um código que funcione, mas que seja resiliente a variáveis externas—sejam elas as políticas de segurança do sistema operacional ou as restrições de acesso e uso de APIs de terceiros—garantindo assim a portabilidade e a estabilidade da aplicação em diferentes ambientes de execução.
