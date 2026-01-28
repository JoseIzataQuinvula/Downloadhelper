; Script profissional para o projeto DownloadHelper
; Desenvolvido por José Izata Quivula

[Setup]
AppId={{D1A2B3C4-E5F6-4A7B-8C9D-0E1F2G3H4I5J}
AppName=DownloadHelper
AppVersion=1.0
AppPublisher=José Izata Quivula
DefaultDirName={autopf}\DownloadHelper
DefaultGroupName=DownloadHelper
AllowNoIcons=yes
; O ícone que aparecerá no arquivo de instalação
SetupIconFile=C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\assets\app_icon.ico
; Nome do arquivo instalador final que será criado
OutputBaseFilename=DownloadHelper_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; O executável principal que o PyInstaller gerou
Source: "C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\dist\DownloadHelper\DownloadHelper.exe"; DestDir: "{app}"; Flags: ignoreversion
; Todos os arquivos dependentes (pasta _internal, assets, ffmpeg, etc.)
Source: "C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\dist\DownloadHelper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\DownloadHelper"; Filename: "{app}\DownloadHelper.exe"
; Atalho de Desinstalação
Name: "{group}\{cm:UninstallProgram,DownloadHelper}"; Filename: "{uninstallexe}"
; Atalho na Área de Trabalho
Name: "{autodesktop}\DownloadHelper"; Filename: "{app}\DownloadHelper.exe"; Tasks: desktopicon

[Run]
; Opção para abrir o app assim que terminar a instalação
Filename: "{app}\DownloadHelper.exe"; Description: "{cm:LaunchProgram,DownloadHelper}"; Flags: nowait postinstall skipifsilent
