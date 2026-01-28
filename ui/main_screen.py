import os
import threading
import logging
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window

from core.downloader import DownloaderCore
from core.utils import normalize_url
from .components import MediaBox 
from .popups import QualitySelectorPopup 

logger = logging.getLogger(__name__)

class MainScreen(BoxLayout):
    status_text = StringProperty("")
    status_color = ListProperty([1, 1, 1, 1]) 
    is_analyzing = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core = DownloaderCore()
        self.media_boxes = {} 
        self.download_states = {} 
        Window.bind(on_focus=self._global_refresh)

    def _global_refresh(self, window, focus):
        if focus:
            for card in list(self.media_boxes.values()):
                state = self.download_states.get(card.url, {})
                if not state.get("running"):
                    v_id = card.data.get("id")
                    n_ent = card.data.get("n_entries", 1)
                    status, path, count = self.core.check_existing_status(v_id, n_ent)
                    card.data["status_disco"] = status
                    card.data["path_real"] = path
                    card.data["count_disco"] = count
                    card.refresh_visual_state()

    def handle_search(self):
        raw_input = self.ids.url_input.text.strip()
        if not raw_input or self.is_analyzing: return
        self.is_analyzing = True
        self.show_status("Iniciando análise...", [0.37, 0.64, 0.88, 1])
        # A análise precisa de thread para não travar a barra de busca
        threading.Thread(target=self._search_thread, args=(raw_input,), daemon=True).start()

    def _search_thread(self, raw_input):
        try:
            url = normalize_url(raw_input)
            if not url or url in self.media_boxes:
                msg = "URL Inválida ou duplicada."
                Clock.schedule_once(lambda dt: self.show_status(msg, [0.9, 0.3, 0.3, 1]))
                return

            info = self.core.get_info(url)
            if not info: 
                Clock.schedule_once(lambda dt: self.show_status("Vídeo indisponível.", [0.9, 0.3, 0.3, 1]))
                return
            
            video_id = info.get("id", "unk")
            n_entries = info.get("n_entries", 1)
            status, path, count = self.core.check_existing_status(video_id, n_entries)
            
            data = {
                "id": video_id, "title": info.get("title", "Sem título"),
                "n_entries": n_entries, "status_disco": status,
                "path_real": path, "count_disco": count,
                "type": "playlist" if n_entries > 1 else "video"
            }
            Clock.schedule_once(lambda dt: self._process_search_result(url, data))
        except Exception as e:
            logger.error(f"Erro: {e}")
            Clock.schedule_once(lambda dt: self.show_status("Erro ao analisar link.", [0.9, 0.3, 0.3, 1]))
        finally:
            Clock.schedule_once(lambda dt: setattr(self, 'is_analyzing', False))

    def _process_search_result(self, url, data):
        self.add_media_card(url, data)
        self.ids.url_input.text = ""
        self.show_status("Link adicionado!", [0.2, 0.8, 0.4, 1])

    def add_media_card(self, url, data):
        card = MediaBox(url=url, data=data)
        card.on_download = lambda: self.start_download(url, data, card)
        card.on_remove = lambda: self.remove_card(card, url)
        card.on_open_folder = lambda: self.open_folder(data.get("path_real"), card)
        self.ids.container.add_widget(card)
        self.media_boxes[url] = card

    def start_download(self, url, data, card):
        def execute_download(quality_key):
            self.download_states[url] = {"running": True}
            card.set_downloading_mode(True) 
            
            # O progress_callback agora apenas repassa o dicionário para o componente
            # O componente MediaBox (que corrigimos antes) já sabe ler esse dicionário
            def progress_callback(d):
                if url not in self.download_states or not self.download_states[url]["running"]:
                    return
                
                # Se o download terminou de vez
                if d.get('status') == 'complete_all':
                    self.download_states[url]["running"] = False
                    s, p, c = self.core.check_existing_status(data['id'], data['n_entries'])
                    data.update({"status_disco": s, "path_real": p, "count_disco": c})
                    card.update_progress(d) # Avisa o card para finalizar
                else:
                    card.update_progress(d)

            # NÃO use threading.Thread aqui, o core.start_download já faz isso!
            self.core.start_download(url, progress_callback, data['id'], data['title'], quality_key)
        
        if data.get("status_disco") == "concluido":
            self.show_status("Este vídeo já foi baixado.", [0.2, 0.8, 0.4, 1])
        else:
            QualitySelectorPopup(data, execute_download).open()

    def remove_card(self, card, url):
        if url in self.download_states: self.download_states[url]["running"] = False
        if url in self.media_boxes: del self.media_boxes[url]
        self.ids.container.remove_widget(card)

    def show_status(self, mensagem, cor):
        self.status_text = mensagem
        self.status_color = cor
        Clock.unschedule(self._clear_status)
        Clock.schedule_once(self._clear_status, 5)

    def _clear_status(self, dt): self.status_text = ""

    def open_folder(self, path, card):
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            self.show_status("Pasta não encontrada.", [0.9, 0.3, 0.3, 1])