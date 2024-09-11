import asyncio
import websockets
import json


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
                file_path = data["file_path"]
                print(f"Rodando simulação com o arquivo: {file_path}")
                rodar_simulacao(file_path)


def rodar_simulacao(file_path):
    """
    Função para rodar a simulação com base no arquivo recebido.
    """
    # Aqui você pode colocar a lógica de rodar a simulação com o arquivo
    print(f"Simulação iniciada com {file_path}")


# Exemplo de uso
if __name__ == "__main__":
    asyncio.run(listen_to_server())
