import sys
import ctypes
import logging
import traceback
import os
from pathlib import Path

# --- CONFIGURAÇÃO PRÉ-KIVY ---
os.environ['KIVY_TEXT'] = 'sdl2'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from core.config import init_folders, BASE_DIR
from ui.main_screen import MainScreen 

logger = logging.getLogger(__name__)

# --- SISTEMA GLOBAL DE CURSOR (HOVER) ---
def setup_cursor_behavior():
    """ 
    Injeta o comportamento de mudar o cursor em qualquer widget 
    que tenha comportamento de botão (Button, ToggleButton, etc).
    """
    # Guardamos a função original de on_entree e on_leave se necessário, 
    # mas o Kivy Window.mouse_pos é mais direto para Desktop.
    
    def update_cursor(window, pos):
        # Verifica se o mouse está sobre algum widget clicável
        found_clickable = False
        
        # Percorre os widgets sob o mouse
        for widget in window.children:
            if hasattr(widget, 'walk'): # Navega na árvore de widgets
                for child in widget.walk():
                    if isinstance(child, ButtonBehavior) and child.collide_point(*child.to_widget(*pos)):
                        if not child.disabled:
                            found_clickable = True
                            break
            if found_clickable: break
        
        if found_clickable:
            Window.set_system_cursor('hand')
        else:
            Window.set_system_cursor('arrow')

    Window.bind(mouse_pos=update_cursor)

# --- CLASSE DO APP ---
class DownloadHelperApp(App):
    def build(self):
        self.title = "Download Helper - Gestão de Ativos"
        self.icon = str(Path(BASE_DIR) / "assets" / "app_icon.ico")
        
        try:
            # Ativa o cursor dinâmico
            setup_cursor_behavior()
            
            kv_path = Path(BASE_DIR) / "kv"
            
            # Carregamento dos arquivos de interface
            Builder.load_file(str(kv_path / 'components.kv'))
            Builder.load_file(str(kv_path / 'popups.kv'))
            Builder.load_file(str(kv_path / 'main_screen.kv'))
            
            # Configurações de Janela
            Window.size = (850, 650)
            Window.minimum_width = 800
            Window.minimum_height = 600
            
            return MainScreen()
            
        except Exception as e:
            logger.error(f"Erro ao carregar arquivos KV: {e}")
            print(traceback.format_exc())
            return None 

def main():
    # 1. Configuração de ID do Processo (Windows)
    if os.name == 'nt':
        try:
            app_id = "izata.downloadhelper.v1" 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception as e:
            logger.warning(f"Erro ao configurar AppUserModelID: {e}")

    # 2. Garante que as pastas existam
    init_folders()

    # 3. Inicia a aplicação
    try:
        logger.info("Iniciando loop principal do Kivy...")
        DownloadHelperApp().run()
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.critical(f"Erro fatal: {e}\n{error_msg}")
        print(error_msg)
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()