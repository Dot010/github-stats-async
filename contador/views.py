import asyncio
import time

from django.conf import settings
from django.http import JsonResponse

CONTADORES = ["A", "B", "C"]
ATE = 5


def contar_sync(nome):
    for numero in range(1, ATE + 1):
        time.sleep(settings.CONTADOR_INTERVALO)
        print(f"Contador {nome}: {numero}")
    return {"contador": nome, "contou_ate": ATE}


def contador_sync(request):
    inicio = time.perf_counter()
    resultado = [contar_sync(nome) for nome in CONTADORES]
    tempo = time.perf_counter() - inicio
    print(f"Síncrono levou {tempo:.2f}s")
    return JsonResponse(
        {"modo": "sincrono", "tempo_segundos": round(tempo, 2), "contadores": resultado}
    )


async def contar_async(nome):
    for numero in range(1, ATE + 1):
        await asyncio.sleep(settings.CONTADOR_INTERVALO)
        print(f"Contador {nome}: {numero}")
    return {"contador": nome, "contou_ate": ATE}


async def contador_async(request):
    inicio = time.perf_counter()
    tarefas = [contar_async(nome) for nome in CONTADORES]
    resultado = await asyncio.gather(*tarefas)
    tempo = time.perf_counter() - inicio
    print(f"Assíncrono levou {tempo:.2f}s")
    return JsonResponse(
        {"modo": "assincrono", "tempo_segundos": round(tempo, 2), "contadores": resultado}
    )