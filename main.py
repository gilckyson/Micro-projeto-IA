# --- IMPORTS ---
from fastapi import FastAPI, Request, HTTPException, Form 
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY") 
# print(f"VALOR DA CHAVE LIDA: ->{GEMINI_KEY}<-") # Linha de debug opcional

# --- CONSTANTES GLOBAIS ---
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
TIMEOUT_SECS = 30
db_historico = [] 

# --- POO (Orientação a Objetos) ---
class Desculpa:
    """Representa uma desculpa dramática gerada pelo sistema."""
    
    def __init__(self, motivo: str, conteudo: str):
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


# --- ROTA GET / (Página Inicial) ---
@app.get("/", tags=["Rotas Principais"])
def home(request: Request):
    """Rota para a página inicial com o formulário de seleção."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "titulo": "Gerador de Desculpas Dramáticas"}
    )


# --- ROTA POST /gerar (Processamento da IA) ---
@app.post("/gerar", tags=["Rotas Principais"])
def gerar_desculpa(request: Request, motivo: str = Form(...)): 
    """Recebe o motivo do usuário, chama a Gemini API e retorna o resultado."""
    
    prompt_ia = f"""
    [1. CONTEXTO] Você é um dramaturgo esquizofrênico e mestre na arte da desculpa extrema.
    [2. TAREFA] Gere uma única desculpa com no mínimo 50 palavras, transformando o motivo abaixo em uma anomalia cósmica ou uma conspiração de alto drama.
    [3. RESTRIÇÕES] NUNCA use a palavra "eu" ou "meu". A desculpa deve ser longa e culpar forças externas. Comece a desculpa diretamente.
    [4. INPUT] Motivo da Desculpa: {motivo}
    """
    
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_KEY}
    json_data = {
        "contents": [{"parts": [{"text": prompt_ia}]}],
        "config": {"temperature": 0.9} 
    }
    
    try:
        # Chama a API do Gemini com timeout
        response = requests.post(
            GEMINI_URL, 
            headers=headers, 
            params=params, 
            json=json_data, 
            timeout=TIMEOUT_SECS
        )
        response.raise_for_status() # Lança exceção para erros HTTP
        
        data = response.json()
        texto_desculpa = data['candidates'][0]['content']['parts'][0]['text']
        
        # Cria o objeto Desculpa e adiciona ao histórico
        nova_desculpa = Desculpa(motivo, texto_desculpa)
        db_historico.append(nova_desculpa)
        
        return templates.TemplateResponse(
            "resultado.html",
            {"request": request, "titulo": "Desculpa Gerada", "desculpa": nova_desculpa}
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504, 
            detail="A IA demorou muito para processar a desculpa (Timeout excedido)."
        )
    except requests.exceptions.RequestException as e:
        # Tratamento de erro: Conexão, 4xx (como a chave inválida), 5xx
        status_code = response.status_code if 'response' in locals() else 500
        raise HTTPException(
            status_code=status_code, 
            detail=f"Erro na comunicação com a API Gemini (Código: {status_code}). Detalhe: {e}"
        )


# --- ROTA GET /historico (Rota Adicional) ---
@app.get("/historico", tags=["Rotas Adicionais"])
def ver_historico(request: Request):
    """Exibe uma lista de todas as desculpas geradas e salvas."""
    return templates.TemplateResponse(
        "historico.html",
        {"request": request, "titulo": "Histórico de Desculpas", "historico": db_historico}
    )