import asyncio
import base64
import websockets
import json

# Lista de clientes conectados
clients = set()


async def notify_simulation_machine(data):
    """
    Notifica todas as máquinas de simulação conectadas sobre o novo arquivo.
    """
    if clients:
        data["action"] = "run_simulation"
        message = json.dumps(data)
        # Converter as corrotinas para tarefas explícitas usando asyncio.create_task()
        await asyncio.gather(*(client.send(message) for client in clients))


async def notify_start_server_machine(data):
    """
    Notifica todas as máquinas de simulação conectadas sobre o novo arquivo.
    """
    if clients:
        data["action"] = "simulation_started"
        message = json.dumps(data)
        # Converter as corrotinas para tarefas explícitas usando asyncio.create_task()
        await asyncio.gather(*(client.send(message) for client in clients))


async def notify_finish_server_machine(data):
    """
    Notifica todas as máquinas de simulação conectadas sobre o novo arquivo.
    """
    if clients:
        data["action"] = "simulation_result"
        message = json.dumps(data)
        # Converter as corrotinas para tarefas explícitas usando asyncio.create_task()
        await asyncio.gather(*(client.send(message) for client in clients))


async def server(websocket, path):
    """
    Lida com conexões de clientes (aplicação e máquinas de simulação).
    """
    # Adiciona o cliente conectado à lista
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            if data["action"] == "simulation":
                del data["action"]
                # Um novo arquivo foi enviado pela aplicação
                print(f"Nova simulacao recebida: {data}")

                # Notifica a máquina de simulação
                await notify_simulation_machine(data)

            elif data["action"] == "simulation_started":
                del data["action"]
                print(f"Simulação {data['simulation_name']} iniciada com sucesso")
                # Notifica o servidor com os resultados
                await notify_start_server_machine(data)

            elif data["action"] == "simulation_result":
                del data["action"]
                print(f"Novo resultado de simulação: {data}")
                # Notifica o servidor com os resultados
                await notify_finish_server_machine(data)

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
