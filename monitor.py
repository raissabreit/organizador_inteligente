import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import EXTENSOES, PASTA_MONITORADA, PASTA_ORGANIZADA
from database import registrar_movimentacao, criar_banco

class OrganizadorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Novo arquivo detectado: {event.src_path}")
            self.organizar_arquivo(event.src_path)
    
    def organizar_arquivo(self, caminho_arquivo):
        nome_arquivo = os.path.basename(caminho_arquivo)
        _, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower()
        
        categoria = "Outros"
        for cat, exts in EXTENSOES.items():
            if extensao in exts:
                categoria = cat
                break
        
        pasta_destino = os.path.join(PASTA_ORGANIZADA, categoria)
        os.makedirs(pasta_destino, exist_ok=True)
        
        destino_final = os.path.join(pasta_destino, nome_arquivo)
        try:
            shutil.move(caminho_arquivo, destino_final)
            registrar_movimentacao(nome_arquivo, categoria)
            print(f"✅ Arquivo {nome_arquivo} movido para {categoria}")
        except Exception as e:
            print(f"❌ Erro ao mover {nome_arquivo}: {e}")

def iniciar_monitoramento():
    criar_banco()
    os.makedirs(PASTA_ORGANIZADA, exist_ok=True)
    
    observer = Observer()
    event_handler = OrganizadorHandler()
    observer.schedule(event_handler, PASTA_MONITORADA, recursive=False)
    observer.start()
    
    print(f"👀 Monitorando pasta: {PASTA_MONITORADA}")
    return observer
