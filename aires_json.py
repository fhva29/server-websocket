import asyncio
import base64
import websockets
import json
import time


async def listen_to_server():
    """
    Escuta o servidor WebSocket e inicia a simulação quando um novo arquivo for recebido.
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data["action"] == "run_simulation":
                del data["action"]
                await rodar_simulacao(data, websocket)


async def executar_simulacao(data, websocket):
    """
    Função que executa a simulação e envia o resultado após a conclusão.
    """
    # Simulação placeholder (usar asyncio.sleep para operações não-bloqueantes)
    print(f"Executando a simulação: {data}")
    await asyncio.sleep(10)  # Simula o tempo de execução da simulação

    # Ler os arquivos (simulados) e enviar como base64
    with open(f'{data["simulation_name"]}.jpg', "rb") as jpg_file:
        jpg_content = base64.b64encode(jpg_file.read()).decode("utf-8")

    resultado_simulacao = {
        "action": "simulation_result",
        "simulation_name": data["simulation_name"],
        "status": "completed",
        "message": "Simulação concluída com sucesso",
        "result_data": {"jpg": jpg_content},
    }

    # Enviar o resultado da simulação
    await websocket.send(json.dumps(resultado_simulacao))


async def rodar_simulacao(data, websocket):
    """
    Função que apenas notifica que a simulação foi iniciada com sucesso
    e chama a função que efetivamente roda a simulação.
    """
    print(f"Simulação {data['simulation_name']} iniciada com sucesso")

    # Envia uma mensagem de início para o servidor
    mensagem_inicial = {
        "action": "simulation_started",
        "simulation_name": data["simulation_name"],
        "status": "started",
        "message": f"Simulação {data['simulation_name']} iniciada com sucesso",
    }
    await websocket.send(json.dumps(mensagem_inicial))

    # Chama a função que executa a simulação de fato
    await executar_simulacao(data, websocket)


# Exemplo de uso
if __name__ == "__main__":
    asyncio.run(listen_to_server())
