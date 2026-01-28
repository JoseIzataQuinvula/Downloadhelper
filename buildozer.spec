[app]
# (str) Título do seu aplicativo
title = Download Helper

# (str) Nome do pacote (sem espaços ou acentos)
package.name = downloadhelper

# (str) Domínio do pacote
package.domain = org.izata

# (str) Onde está o seu main.py
source.dir = .

# (list) Extensões de arquivos que o Buildozer deve incluir no APK
source.include_exts = py,png,jpg,kv,atlas,ico,txt

# (str) Versão do App
version = 1.0

# (list) Bibliotecas necessárias (MUITO IMPORTANTE)
# Adicionei yt-dlp, requests e certifi para o download funcionar
requirements = python3,kivy==2.3.0,yt-dlp,requests,certifi,urllib3,chardet,idna

# (str) Ícone do App (se tiver na pasta assets)
icon.filename = %(source.dir)s/assets/app_icon.ico

# (list) Orientações suportadas
orientation = portrait

#
# Android specific
#

# (bool) Se o app deve ser tela cheia
fullscreen = 0

# (list) Permissões do Android (Essencial para salvar arquivos)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (int) API alvo (API 31 é o padrão atual do Google)
android.api = 31

# (int) API mínima (Roda desde Android 5.0)
android.minapi = 21

# (bool) Aceitar licenças automaticamente
android.accept_sdk_license = True

# (list) Arquiteturas para celulares modernos e antigos
android.archs = arm64-v8a, armeabi-v7a

# (bool) Ativar AndroidX (melhora compatibilidade)
android.enable_androidx = True

[buildozer]
# (int) Nível de log (2 mostra tudo o que está acontecendo)
log_level = 2

# (int) Aviso se rodar como root
warn_on_root = 1