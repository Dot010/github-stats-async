# Contador síncrono x assíncrono em Django

Exercício do Módulo 11 (Concorrência em Django) da formação Desenvolvedor Full Stack Python da EBAC.

O projeto tem duas views que fazem a mesma tarefa: três contadores (A, B e C) contam de 1 a 5, com uma pausa de 0,5 segundo entre cada número. A diferença está em como a espera acontece.

| Rota | View | Como conta |
|---|---|---|
| `/contador/sync/` | `contador_sync` | Um contador de cada vez, com `time.sleep` (bloqueia) |
| `/contador/async/` | `contador_async` | Os três ao mesmo tempo, com `asyncio.sleep` e `asyncio.gather` (não bloqueia) |

As duas views medem o tempo com `time.perf_counter()` e devolvem o resultado em JSON. O terminal mostra a ordem em que cada número foi contado.

## Como rodar

Requisitos: Python 3.12 ou superior.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do exemplo:

```bash
# Windows
copy .env.example .env
# Linux/macOS
cp .env.example .env
```

Crie as tabelas internas do Django (evita o aviso de migrações pendentes):

```bash
python manage.py migrate
```

Suba o servidor ASGI e acesse as rotas:

```bash
uvicorn config.asgi:application --reload
```

- http://127.0.0.1:8000/contador/sync/
- http://127.0.0.1:8000/contador/async/

O `python manage.py runserver` também funciona.

## Variáveis de ambiente

| Variável | Para que serve | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | valor só para desenvolvimento |
| `DEBUG` | Modo de depuração | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | `localhost,127.0.0.1` |
| `CONTADOR_INTERVALO` | Pausa em segundos entre cada número | `0.5` |

## Resultado

| Modo | Tempo |
|---|---|
| Síncrono | ~7,5 s (3 contadores × 5 números × 0,5 s) |
| Assíncrono | ~2,5 s (os 3 contadores esperam ao mesmo tempo) |

A versão assíncrona foi cerca de 3x mais rápida. Enquanto um contador espera no `await asyncio.sleep`, o event loop passa a vez para os outros, então as esperas acontecem em paralelo. No modo síncrono, o `time.sleep` trava a execução e cada contador só começa quando o anterior termina.

Saída no terminal da view assíncrona (os contadores se alternam):

```
Contador A: 1
Contador B: 1
Contador C: 1
Contador A: 2
...
Assíncrono levou 2.51s
```

## Testes

```bash
python manage.py test
```

Os testes zeram o `CONTADOR_INTERVALO` para rodar rápido.