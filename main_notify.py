import asyncio
import websockets
import json

# Lista de clientes conectados
clients = set()


async def notify_simulation_machine(file_path):
    """
    Notifica todas as máquinas de simulação conectadas sobre o novo arquivo.
    """
    if clients:
        message = json.dumps({"action": "run_simulation", "file_path": file_path})
        # Converter as corrotinas para tarefas explícitas usando asyncio.create_task()
        await asyncio.wait(
            [asyncio.create_task(client.send(message)) for client in clients]
        )


async def server(websocket, path):
    """
    Lida com conexões de clientes (aplicação e máquinas de simulação).
    """
    # Adiciona o cliente conectado à lista
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            if data["action"] == "upload_complete":
                # Um novo arquivo foi enviado pela aplicação
                file_path = data["file_path"]
                print(f"Novo arquivo recebido: {file_path}")

                # Notifica a máquina de simulação
                await notify_simulation_machine(file_path)

    finally:
        # Remove o cliente da lista ao desconectar
        clients.remove(websocket)


# Inicia o servidor WebSocket
async def main():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()  # Mantém o servidor rodando


# Rodar o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(main())
