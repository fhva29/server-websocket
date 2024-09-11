import asyncio
import websockets
import os

# Lista de clientes conectados
clients = set()


async def notify_simulation_machine(filename, file_data):
    """
    Notifica todas as máquinas de simulação conectadas e envia o arquivo.
    """
    if clients:
        for client in clients:
            try:
                await client.send(filename)
                await client.send(file_data)
            except websockets.ConnectionClosed as e:
                print(f"Conexão fechada com o cliente: {e}")


async def server(websocket, path):
    """
    Lida com conexões de clientes (aplicação e máquinas de simulação).
    """
    clients.add(websocket)
    print("Cliente conectado")

    try:
        while True:
            message = await websocket.recv()
            if isinstance(message, str):
                if message.endswith(".txt"):
                    filename = message
                    print(f"Recebendo arquivo: {filename}")

                    file_data = await websocket.recv()
                    print(f"Arquivo {filename} recebido com sucesso")

                    await notify_simulation_machine(filename, file_data)

                else:
                    print(f"Notificação da simulação: {message}")
                    for client in clients:
                        if client != websocket:
                            await client.send(message)

            else:
                print("Recebido um dado inesperado")

    except websockets.ConnectionClosedError as e:
        print(f"Conexão fechada inesperadamente: {e}")
    except websockets.ConnectionClosedOK:
        print("Conexão fechada normalmente.")
    finally:
        clients.remove(websocket)
        print("Cliente desconectado")


# Inicia o servidor WebSocket
async def main():
    async with websockets.serve(server, "localhost", 8765):
        await asyncio.Future()


# Rodar o servidor WebSocket
if __name__ == "__main__":
    print("Iniciando o servidor WebSocket...")
    asyncio.run(main())
