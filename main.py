# main.py

# --- IMPORTS OBRIGATÓRIOS E AUXILIARES ---
from fastapi import FastAPI, Request, HTTPException, Form 
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests # Requisito: Usar biblioteca requests para chamar API 
import os
from dotenv import load_dotenv # Para ler o arquivo .env
import json # Usado para formatar o JSON do print em debug

# Carrega a chave da API do arquivo .env
load_dotenv()
# VÁLIDO: Busca o valor da variável de ambiente que tem o NOME "GEMINI_KEY"
GEMINI_KEY = os.getenv("GEMINI_KEY") # <--- CORREÇÃO CRÍTICA AQUI!

# --- CONSTANTES GLOBAIS ---
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
TIMEOUT_SECS = 30 # Requisito: Implementar timeout de 30 segundos 
db_historico = [] # Lista simples para simular um "banco de dados" de histórico

# --- 1. POO (Orientação a Objetos) ---
# Requisito: Criar pelo menos 1 classe que represente algo do projeto
class Desculpa:
    """Representa uma desculpa dramática gerada pelo sistema."""
    
    def __init__(self, motivo: str, conteudo: str):
        # Atributos (dados da desculpa)
        self.motivo = motivo
        self.conteudo = conteudo
        self.caracteres = len(conteudo)
        
    def calcular_pontuacao_drama(self) -> str:
        """Método de negócio: Avalia o drama com base no tamanho."""
        if self.caracteres > 200:
            return "NÍVEL: CATACLISMO ESPAÇO-TEMPORAL 🌌"
        elif self.caracteres > 100:
            return "NÍVEL: CONSPIRAÇÃO GALÁCTICA 🌠"
        else:
            return "NÍVEL: FRACO, MAS DRAMÁTICO ✨"


app = FastAPI(title="Gerador de Desculpas Dramáticas")
templates = Jinja2Templates(directory="templates")


# --- 2. ROTA GET / (Página Inicial) ---
# Requisito: 1 rota para página inicial (GET)
@app.get("/", tags=["Rotas Principais"])
def home(request: Request):
    """Rota para a página inicial com o formulário de seleção."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "titulo": "Gerador de Desculpas Dramáticas"}
    )


# --- 3. ROTA POST /gerar (Processamento da IA) ---
# Requisito: 1 rota para processar entrada do usuário (POST /processar)
@app.post("/gerar", tags=["Rotas Principais"])
# CORREÇÃO: Recebe o 'motivo' como dado de formulário (Form)
def gerar_desculpa(request: Request, motivo: str = Form(...)): 
    """Recebe o motivo do usuário, chama a Gemini API e retorna o resultado."""
    
    
    # O Prompt (A "Receita" para a IA, responsabilidade P3)
    prompt_ia = f"""
    [1. CONTEXTO Quem a IA deve ser]
    Você é um dramaturgo esquizofrênico e mestre na arte da desculpa extrema.
    [2. TAREFA O que fazer]
    Gere uma única desculpa com no mínimo 50 palavras, transformando o motivo abaixo em uma anomalia cósmica ou uma conspiração de alto drama.
    [3. RESTRIÇÕES Regras a seguir]
    - NUNCA use a palavra "eu" ou "meu".
    - A desculpa deve ser longa e culpar forças externas ou efeitos borboleta.
    - Comece a desculpa diretamente, sem introduções.
    [4. INPUT Dados do usuário]
    Motivo da Desculpa: {motivo}
    """
    
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_KEY}
    json_data = {
        "contents": [{"parts": [{"text": prompt_ia}]}],
        # Temperatura alta (0.9) para máxima criatividade
        "config": {"temperature": 0.9} 
    }
    
    try:
        # Chama a API do Gemini com a biblioteca requests
        response = requests.post(
            GEMINI_URL, 
            headers=headers, 
            params=params, 
            json=json_data, 
            timeout=TIMEOUT_SECS # Aplicação do Timeout 
        )
        response.raise_for_status() # Lança exceção para erros HTTP (4xx/5xx)
        
        # Pega o texto da resposta
        data = response.json()
        texto_desculpa = data['candidates'][0]['content']['parts'][0]['text']
        
        # Cria o objeto Desculpa (Usando POO para armazenar e processar)
        nova_desculpa = Desculpa(motivo, texto_desculpa)
        
        # Adiciona ao histórico (para a Rota 3)
        db_historico.append(nova_desculpa)
        
        # Requisito: Passar dados do backend (o objeto Desculpa) para o frontend 
        return templates.TemplateResponse(
            "resultado.html",
            {"request": request, "titulo": "Desculpa Gerada", "desculpa": nova_desculpa}
        )

    except requests.exceptions.Timeout:
        # Tratamento de erro: Timeout 
        raise HTTPException(
            status_code=504, 
            detail="A IA demorou muito para processar a desculpa (Timeout de 30s excedido). Tente um motivo mais simples."
        )
    except requests.exceptions.RequestException as e:
        # Tratamento de erro: Conexão, 4xx, 5xx, etc. 
        status_code = response.status_code if 'response' in locals() else 500
        raise HTTPException(
            status_code=status_code, 
            detail=f"Erro na comunicação com a API Gemini (Código: {status_code}). Verifique a chave ou o limite de uso. Detalhe: {e}"
        )


# --- 4. ROTA GET /historico (Rota Adicional) ---
# Requisito: 1 rota adicional de sua escolha (ex: histórico)
@app.get("/historico", tags=["Rotas Adicionais"])
def ver_historico(request: Request):
    """Exibe uma lista de todas as desculpas geradas e salvas."""
    # Passa a lista de objetos Desculpa para o template
    return templates.TemplateResponse(
        "historico.html",
        {"request": request, "titulo": "Histórico de Desculpas", "historico": db_historico}
    )