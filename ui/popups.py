import logging
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from core.config import QUALITY_PROFILES, get_asset_file

logger = logging.getLogger(__name__)

class QualitySelectorPopup(Popup):
    info_text = StringProperty("")
    icon_src = StringProperty("")

    def __init__(self, data, callback, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.callback = callback
        self.icon_src = get_asset_file("app_icon.ico")
        self.quality_buttons = [] 
        
        # Filtro de segurança para resoluções
        raw_res = self.data.get("available_qualities", [])
        self.available_res = []
        for r in raw_res:
            try:
                if r is not None: self.available_res.append(int(r))
            except: continue
        
        total = self.data.get("n_entries", 1)
        self.v_max = max(self.available_res) if self.available_res else 0
        
        tipo = 'Playlist' if total > 1 else 'Vídeo'
        res_display = f"{self.v_max}p" if self.v_max > 0 else "Auto Detect"
        self.info_text = f"{tipo} | {total} item(s) (Máximo: {res_display})"

        Clock.schedule_once(lambda dt: self._build_options())

    def _build_options(self):
        mapping = {
            "ULTRA_4K": 2160, "QUAD_HD": 1440, "FULL_HD": 1080, 
            "HD_720P": 720, "SD_480P": 480
        }
        
        self.ids.options_list.clear_widgets()
        self.quality_buttons = []

        # O SEGREDO: Se não detectou (0), assumimos 1080p para liberar os botões
        effective_v_max = self.v_max if self.v_max > 0 else 1080

        for key, profile in QUALITY_PROFILES.items():
            is_audio = (key == "AUDIO_ONLY")
            needed_res = mapping.get(key, 0)
            
            # Libera se for áudio ou se a resolução detectada (ou presumida) permitir
            is_available = is_audio or (effective_v_max >= needed_res)

            item_box = BoxLayout(orientation='vertical', size_hint_y=None, height='60dp', spacing='2dp')
            
            # Define o padrão visual: 720p se disponível, senão SD
            state_val = 'normal'
            if key == "HD_720P" and is_available:
                state_val = 'down'
            elif key == "SD_480P" and not any(b.state == 'down' for b in self.quality_buttons):
                state_val = 'down'

            btn = ToggleButton(
                text=profile["label"],
                group='quality',
                state=state_val,
                disabled=not is_available,
                size_hint_y=None, height='40dp',
                background_normal='',
                background_down='',
                background_color=(0.12, 0.32, 0.55, 1) if state_val == 'down' else (0.15, 0.15, 0.15, 1),
                color=(1, 1, 1, 1),
                bold=True
            )
            btn.quality_key = key
            btn.bind(state=self._update_button_ui)
            
            status_desc = profile.get("description", "") if is_available else f"Indisponível ({self.v_max}p)"
            
            desc = Label(
                text=status_desc, font_size='11sp', 
                color=(0.6, 0.6, 0.6, 1) if is_available else (0.8, 0.3, 0.3, 1),
                size_hint_y=None, height='15dp'
            )

            item_box.add_widget(btn)
            item_box.add_widget(desc)
            self.ids.options_list.add_widget(item_box)
            
            if is_available:
                self.quality_buttons.append(btn)

    def _update_button_ui(self, instance, state):
        instance.background_color = (0.12, 0.32, 0.55, 1) if state == 'down' else (0.15, 0.15, 0.15, 1)

    def confirm(self):
        selected = "AUDIO_ONLY"
        for btn in self.quality_buttons:
            if btn.state == 'down':
                selected = btn.quality_key
                break
        
        self.ids.options_list.disabled = True
        self.dismiss()
        Clock.schedule_once(lambda dt: self._safe_callback(selected), 0.2)

    def _safe_callback(self, quality):
        try:
            self.callback(quality)
        except Exception as e:
            logger.error(f"Erro no callback de qualidade: {e}")