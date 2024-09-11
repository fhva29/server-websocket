import asyncio
import websockets
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class UploadHandler(FileSystemEventHandler):
    """
    Manipulador para monitorar novos arquivos na pasta de simulação.
    """

    def on_created(self, event):
        print(f"Novo arquivo detectado: {event.src_path}")
        # Enviar notificação ao WebSocket
        asyncio.run(enviar_notificacao(event.src_path))


async def enviar_notificacao(file_path):
    """
    Envia uma notificação ao WebSocket informando que um novo arquivo foi carregado.
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        data = {
            "action": "upload_complete",
            "file_path": file_path,
        }
        await websocket.send(json.dumps(data))
        print(f"Notificação enviada para o arquivo: {file_path}")


# Função para monitorar a pasta usando watchdog
def monitorar_pasta(path):
    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Caminho para a pasta que deve ser monitorada
if __name__ == "__main__":
    monitorar_pasta("./simulacoes")
