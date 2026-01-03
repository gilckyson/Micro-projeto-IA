# --- IMPORTS ---
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

# --- CARREGA VARIÁVEIS DE AMBIENTE ---
load_dotenv()

# --- APP FASTAPI ---
app = FastAPI(title="Gerador de Desculpas Dramáticas")
templates = Jinja2Templates(directory="templates")

# --- BANCO EM MEMÓRIA ---
db_historico = []

# --- POO (Orientação a Objetos) ---
class Desculpa:
    def __init__(self, motivo: str, conteudo: str):
        self.motivo = motivo
        self.conteudo = conteudo
        self.caracteres = len(conteudo)

    def calcular_pontuacao_drama(self) -> str:
        if self.caracteres > 200:
            return "NÍVEL: CATACLISMO ESPAÇO-TEMPORAL 🌌"
        elif self.caracteres > 100:
            return "NÍVEL: CONSPIRAÇÃO GALÁCTICA 🌠"
        return "NÍVEL: FRACO, MAS DRAMÁTICO ✨"


# --- ROTA GET / ---
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# --- ROTA POST /gerar ---
@app.post("/gerar")
def gerar_desculpa(request: Request, motivo: str = Form(...)):
    GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")

    if not GEMINI_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chave da API Gemini não encontrada no .env"
        )

    prompt_ia = f"""
    [1. CONTEXTO] Você é um dramaturgo exageradamente dramático e especialista em criar desculpas absurdas.
    [2. TAREFA] Gere UMA única desculpa com no mínimo 50 palavras, transformando o motivo abaixo em uma conspiração ou evento fora da realidade.
    [3. RESTRIÇÕES] Não use a palavra "eu" nem "meu". Culpe forças externas. Comece a desculpa diretamente.
    [4. INPUT] Motivo da Desculpa: {motivo}
    """

    try:
        # Import defensivo (não quebra o boot do FastAPI)
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_KEY)

        # 🔍 Descobre automaticamente um modelo compatível
        modelos = genai.list_models()

        modelo_texto = None
        for m in modelos:
            if "generateContent" in m.supported_generation_methods:
                modelo_texto = m.name
                break

        if not modelo_texto:
            raise RuntimeError("Nenhum modelo Gemini compatível encontrado.")

        model = genai.GenerativeModel(modelo_texto)

        resposta = model.generate_content(prompt_ia)
        texto_desculpa = resposta.text

        nova_desculpa = Desculpa(motivo, texto_desculpa)
        db_historico.append(nova_desculpa)

        return templates.TemplateResponse(
            "resultado.html",
            {
                "request": request,
                "desculpa": nova_desculpa,
                "modelo_usado": modelo_texto
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar conteúdo com Gemini: {e}"
        )


# --- ROTA GET /historico ---
@app.get("/historico")
def ver_historico(request: Request):
    return templates.TemplateResponse(
        "historico.html",
        {
            "request": request,
            "historico": db_historico
        }
    )
