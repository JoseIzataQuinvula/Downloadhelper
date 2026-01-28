from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.clock import Clock

class MediaBox(BoxLayout):
    title = StringProperty("")
    status_text = StringProperty("")
    status_color = ListProperty([0.5, 0.5, 0.5, 1])
    progress_val = NumericProperty(0)
    
    on_download = ObjectProperty(None)
    on_remove = ObjectProperty(None)
    on_open_folder = ObjectProperty(None)

    def __init__(self, url, data, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.data = data
        raw_title = data.get("title", "Vídeo sem título")
        self.title = (raw_title[:57] + "...") if len(raw_title) > 60 else raw_title
        Clock.schedule_once(lambda dt: self.refresh_visual_state())

    def set_downloading_mode(self, active):
        if active:
            self.progress_val = 0.01 
            self.status_text = "Iniciando..."
            self.status_color = [0.37, 0.64, 0.88, 1] 
        else:
            self.refresh_visual_state()

    def refresh_visual_state(self):
        status = self.data.get("status_disco", "novo")
        count = self.data.get("count_disco", 0)
        total = self.data.get("n_entries", 1)

        self.progress_val = 0 

        if status == "concluido":
            self.status_text = f"✓ Concluído ({total}/{total})"
            self.status_color = [0.18, 0.54, 0.34, 1] 
        elif status == "incompleto":
            self.status_text = f"Pausado: {count}/{total}"
            self.status_color = [0.9, 0.5, 0.1, 1] 
        else:
            self.status_text = f"Pronto para baixar"
            self.status_color = [0.5, 0.5, 0.5, 1] 

    def update_progress(self, d):
        """
        Esta função é chamada via Clock.schedule_once do DownloaderCore.
        """
        # Se 'status' não vier no dicionário, não fazemos nada para evitar erro
        status = d.get('status')
        
        if status == 'error':
            self.status_text = d.get('msg', 'Erro no download')
            self.status_color = [0.8, 0.2, 0.2, 1]
            self.progress_val = 0
            return

        if status == 'downloading':
            # Tenta pegar a porcentagem real do yt-dlp se o ui_percent falhar
            try:
                # O yt-dlp envia o progresso em d['_percent_str'] ou d['downloaded_bytes']/d['total_bytes']
                p_val = d.get('ui_percent')
                if p_val is None:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                    p_val = downloaded / total

                self.progress_val = max(0.01, p_val)
                self.status_text = d.get('ui_msg', f"Baixando... {int(p_val*100)}%")
                self.status_color = [0.37, 0.64, 0.88, 1]
            except:
                pass

        elif status == 'finished':
            self.progress_val = 0.95
            self.status_text = "Processando arquivo final..."
            self.status_color = [0.8, 0.4, 0.9, 1]

        elif status == 'complete_all':
            self.data['status_disco'] = "concluido"
            self.refresh_visual_state()