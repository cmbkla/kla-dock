; Inno Setup Script for KLA Dock
; This script creates a Windows installer for KLA Dock

#define MyAppName "KLA Dock"
#define MyAppVersion "1.0"
#define MyAppPublisher "Kunz, Leigh & Associates"
#define MyAppURL "https://kla.com"
#define MyAppExeName "KLA Dock.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application
AppId={{KLA-DOCK-2025-UUID}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\KLA\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=Output
OutputBaseFilename=KLA_Dock_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Run KLA Dock on Windows startup (recommended)"; GroupDescription: "Startup Options:"; Flags: checkedonce

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Add to startup if user selected that option
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "KLADock"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[Code]
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  // Try to gracefully close KLA Dock if it's running
  if FindWindowByClassName('KLADockWindow') <> 0 then
  begin
    if MsgBox('KLA Dock is currently running. The installer will close it before continuing.' + #13#10 + #13#10 + 'Click OK to continue, or Cancel to exit the installer.', mbConfirmation, MB_OKCANCEL) = IDOK then
    begin
      // Kill the process
      Exec('taskkill', '/F /IM "KLA Dock.exe"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end
    else
    begin
      Result := 'Installation cancelled by user.';
      Exit;
    end;
  end;
  Result := '';
end;

[UninstallRun]
; Stop KLA Dock before uninstalling
Filename: "taskkill"; Parameters: "/F /IM ""KLA Dock.exe"""; Flags: runhidden; RunOnceId: "StopKLADock"
