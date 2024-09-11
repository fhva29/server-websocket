import asyncio
import websockets
import os


async def listen_to_server():
    """
    Escuta o servidor WebSocket e recebe o arquivo.
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                filename = await websocket.recv()

                file_data = await websocket.recv()

                save_path = os.path.join("./simulacoes_recebidas", filename)
                if not os.path.exists("./simulacoes_recebidas"):
                    os.makedirs("./simulacoes_recebidas")

                with open(save_path, "wb") as file:
                    file.write(file_data)

                print(f"Arquivo {filename} recebido e salvo em {save_path}")

                await rodar_simulacao(save_path, websocket)

            except websockets.ConnectionClosed:
                print("Conexão com o servidor fechada.")
                break


async def rodar_simulacao(file_path, websocket):
    """
    Função para rodar a simulação com base no arquivo recebido e notificar o servidor.
    """
    print(f"Simulação iniciada com {file_path}")

    await asyncio.sleep(5)

    message = f"Simulação com o arquivo {file_path} concluída."
    await websocket.send(message)
    print(f"Notificação enviada ao servidor: {message}")


if __name__ == "__main__":
    asyncio.run(listen_to_server())
