; Script gerado para o projeto DownloadHelper de José Izata Quivula

[Setup]
AppId={{D1A2B3C4-E5F6-4A7B-8C9D-0E1F2G3H4I5J}
AppName=DownloadHelper
AppVersion=1.0
AppPublisher=José Izata Quivula
DefaultDirName={autopf}\DownloadHelper
DefaultGroupName=DownloadHelper
AllowNoIcons=yes
; O ícone do instalador
SetupIconFile=C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\assets\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; O executável principal
Source: "C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\dist\DownloadHelper\DownloadHelper.exe"; DestDir: "{app}"; Flags: ignoreversion
; Todos os arquivos da pasta gerada pelo PyInstaller (incluindo _internal, assets, ffmpeg, etc)
Source: "C:\Users\José Izata Quinvula\Documents\my_dev_projects\desktops\downloadhelper\dist\DownloadHelper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\DownloadHelper"; Filename: "{app}\DownloadHelper.exe"
Name: "{group}\{cm:UninstallProgram,DownloadHelper}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DownloadHelper"; Filename: "{app}\DownloadHelper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\DownloadHelper.exe"; Description: "{cm:LaunchProgram,DownloadHelper}"; Flags: nowait postinstall skipifsilent