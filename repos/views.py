import os

from dotenv import load_dotenv


import time
import asyncio
import httpx
from django.http import JsonResponse

load_dotenv()
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

REPOS = [
    "Dot010/Psycare",
    "Dot010/SelfCheckApp",
    "Dot010/personal-portfolio",
    "Dot010/portfolio-django",
]

def buscar_repo_sync(cliente, repo):
    print(f" Buscando {repo}...")
    resposta = cliente.get(f"https://api.github.com/repos/{repo}")
    dados = resposta.json()


    if resposta.status_code != 200:
        print(f"❌ {repo} falhou: {dados.get('message')}")
        return {"nome": repo, "erro": dados.get("message")}

    print(f" Repositório {repo} encontrado!")
    return{
        "nome": dados["name"],
        "estrelas": dados["stargazers_count"],
        "linguagem": dados["language"],
        "atualizado": dados["pushed_at"],
    }

def repos_sync(request):
    inicio = time.perf_counter()
    with httpx.Client(headers=HEADERS) as cliente:
        resultado = [buscar_repo_sync(cliente, repo) for repo in REPOS]
    tempo = time.perf_counter() - inicio
    print(f"🐢 Síncrono levou {tempo:.2f}s")
    return JsonResponse({"modo": "sincrono", "tempo": round(tempo, 2), "repos": resultado})

async def buscar_repo_async(cliente, repo):
    print(f" Buscando {repo}...")
    resposta = await cliente.get(f"https://api.github.com/repos/{repo}")
    dados = resposta.json()


    if resposta.status_code != 200:                          
        print(f"❌ {repo} falhou: {dados.get('message')}")    
        return {"nome": repo, "erro": dados.get("message")}  

    print(f" Repositório {repo} encontrado!")
    return{
        "nome": dados["name"],
        "estrelas": dados["stargazers_count"],
        "linguagem": dados["language"],
        "atualizado": dados["pushed_at"],
    }

async def repos_async(request):
    inicio = time.perf_counter()
    async with httpx.AsyncClient(headers=HEADERS) as cliente:
        tarefas = [buscar_repo_async(cliente, repo) for repo in REPOS]
        resultado = await asyncio.gather(*tarefas)
    tempo = time.perf_counter() - inicio
    print(f"🐇 Assíncrono levou {tempo:.2f}s")
    return JsonResponse({"modo": "assincrono", "tempo": round(tempo, 2), "repos": resultado})
