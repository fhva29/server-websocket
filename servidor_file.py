import asyncio
import websockets
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class UploadHandler(FileSystemEventHandler):
    """
    Manipulador para monitorar novos arquivos na pasta de simulação.
    """

    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory:
            print(f"Novo arquivo detectado: {event.src_path}")
            asyncio.run_coroutine_threadsafe(enviar_arquivo(event.src_path), self.loop)


async def enviar_arquivo(file_path):
    """
    Envia o arquivo via WebSocket.
    """
    uri = "ws://localhost:8765"
    try:
        while not os.path.exists(file_path):
            await asyncio.sleep(1)

        await asyncio.sleep(1)

        async with websockets.connect(uri) as websocket:
            with open(file_path, "rb") as file:
                file_data = file.read()

            filename = os.path.basename(file_path)
            await websocket.send(filename)
            await websocket.send(file_data)

            print(f"Arquivo {filename} enviado com sucesso!")

            while True:
                response = await websocket.recv()
                if (
                    isinstance(response, str)
                    and "Simulação" in response
                    and "concluída" in response
                ):
                    print(f"Resposta de finalização da simulação: {response}")
                await asyncio.sleep(1)

    except Exception as e:
        print(f"Erro ao enviar o arquivo {file_path}: {e}")


def start_watchdog(path, loop):
    """
    Inicia o watchdog em uma thread separada para monitorar a pasta sem bloquear o asyncio.
    """
    event_handler = UploadHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    watchdog_thread = threading.Thread(
        target=start_watchdog, args=("./simulacoes", loop), daemon=True
    )
    watchdog_thread.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
