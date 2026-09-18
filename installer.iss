#define MyAppName "Glass Reminder"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Glass Reminder Team"
#define MyAppExeName "GlassReminder.exe"

[Setup]
AppId={{8F932D10-4A9B-4C92-A234-92A5123985F1}
AppName=Glass Reminder
AppVersion=2.0.0
AppPublisher=Glass Reminder Team
DefaultDirName={autopf}\GlassReminder
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=GlassReminder-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\GlassReminder.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Glass Reminder"; Filename: "{app}\GlassReminder.exe"
Name: "{autodesktop}\Glass Reminder"; Filename: "{app}\GlassReminder.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GlassReminder.exe"; Description: "Launch Glass Reminder"; Flags: nowait postinstall skipifsilent