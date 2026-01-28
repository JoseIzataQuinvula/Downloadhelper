# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from kivy_deps import sdl2, glew

# Aumenta o limite para o KivyMD não travar a análise
sys.setrecursionlimit(10000)

block_cipher = None

# Mapeamento preciso das pastas
added_files = [
    ('assets', 'assets'),
    ('kv', 'kv'),
    ('ffmpeg', 'ffmpeg'),
    ('core', 'core'),
    ('ui', 'ui'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    # Adicionamos dependências que o PyInstaller costuma "perder" no 3.13
    hiddenimports=[
        'yt_dlp', 
        'kivy', 
        'kivymd', 
        'kivymd.icon_definitions', 
        'kivymd.effects.stiffscroll',
        'ffpyplayer'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DownloadHelper',
    debug=False, # Mantenha False para evitar logs infinitos
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DownloadHelper',
)