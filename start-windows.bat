@echo off
echo Checking environment, please wait...
SETLOCAL ENABLEDELAYEDEXPANSION


FOR /F "tokens=*" %%A IN ('REG Query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /F "%~1" /D /S 2^>NUL ^| FINDSTR /R /C:"HKEY_"') DO (
	SET Found=0
	(REG Query "%%~A" /F DisplayName /V /E | FINDSTR /R /I /C:" DisplayName .* .*Oracle VM VirtualBox" && SET Found=1) >NUL 2>&1
	IF !Found! EQU 1 (
		echo OK: Oracle Virtual Box is installed 
		goto :NEXT1
	)
)
WMIC.EXE Path Win32_Processor Get DataWidth 2>NUL | FIND "64" >NUL

IF ERRORLEVEL 1 (
  ECHO.
) ELSE (
	FOR /F "tokens=*" %%A IN ('REG Query HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall /F "%~1" /D /S 2^>NUL ^| FINDSTR /R /C:"HKEY_"') DO (
		SET Found=0
		(REG Query "%%~A" /F DisplayName /V /E | FINDSTR /R /I /C:" DisplayName .* .*Oracle VM VirtualBox" && SET Found=1) >NUL 2>&1
		IF !Found! EQU 1 (
		  echo OK: Oracle Virtual Box is installed
		  goto :NEXT1	
		)
)
)
:NEXT1
if !Found! EQU 0 (
	    echo You need to download and install Oracle Virtual Box from https://www.virtualbox.org/wiki/Downloads
        echo Run the script again after Oracle Virtual Box is installed on your machine.
)

REM --------------------------------------------------------------

FOR /F "tokens=*" %%A IN ('REG Query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /F "%~1" /D /S 2^>NUL ^| FINDSTR /R /C:"HKEY_"') DO (
	SET Found2=0
	(REG Query "%%~A" /F DisplayName /V /E | FINDSTR /R /I /C:" DisplayName .* .*Vagrant" && SET Found2=1) >NUL 2>&1
	IF !Found2! EQU 1 (
		echo OK: Vagrant is installed 
		goto :NEXT2
	)
)
WMIC.EXE Path Win32_Processor Get DataWidth 2>NUL | FIND "64" >NUL

IF ERRORLEVEL 1 (
  ECHO.
) ELSE (
	FOR /F "tokens=*" %%A IN ('REG Query HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall /F "%~1" /D /S 2^>NUL ^| FINDSTR /R /C:"HKEY_"') DO (
		SET Found2=0
		(REG Query "%%~A" /F DisplayName /V /E | FINDSTR /R /I /C:" DisplayName .* .*Vagrant" && SET Found2=1) >NUL 2>&1
		IF !Found2! EQU 1 (
		  echo OK: Vagrant is installed 
		  goto :NEXT2
		)
)
:NEXT2
if !Found2! EQU 0 (

 	    echo You need to download and install Vagrant from https://www.vagrantup.com/downloads.html
        echo Run the script again after Vagrant is installed on your machine.
)
)

if !Found! EQU 1 (
 if !Found2! EQU 1 (
     echo All requirements are met - please run "vagrant up <ENV>"
 )
)

ENDLOCAL