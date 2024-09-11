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


async def rodar_simulacao(data, websocket):
    """
    Função para rodar a simulação com base no arquivo recebido.
    """
    # Aqui você pode colocar a lógica de rodar a simulação com o arquivo
    print(f"Simulação iniciada com {data}")

    # AQUI VAI SER A PARTE DE SUBSTITUIR AS VARIAVEIS NO ARQUIVO
    with open(f'{data["simulation_name"]}.json', "w") as json_file:
        json.dump(data, json_file, indent=4)

    time.sleep(10)
    # Ler os arquivos (simulados) e enviar como base64
    with open(f'{data["simulation_name"]}.jpg', "rb") as jpg_file:
        jpg_content = base64.b64encode(jpg_file.read()).decode("utf-8")

    print("Simulação concluída com sucesso")

    resultado_simulacao = {
        "action": "simulation_result",
        "simulation_name": data["simulation_name"],
        "status": "completed",
        "message": "Simulação concluída com sucesso",
        "result_data": {"jpg": jpg_content},
    }

    await websocket.send(json.dumps(resultado_simulacao))


# Exemplo de uso
if __name__ == "__main__":
    asyncio.run(listen_to_server())
