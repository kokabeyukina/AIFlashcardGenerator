@ECHO OFF
SETLOCAL EnableDelayedExpansion
chcp 65001 >nul

set count=0
for %%F in (*_class.py) do (
    set option!count!=%%F
    set full_name=%%~nF
    set optionName!count!=!full_name:~0,-6!
    set /a count+=1
)
set /a maxIndex=%count% - 1

if %count%==0 (
    echo [91mNo class files found.[0m
    goto end
)

set unfoc=[40m
set foc=[7m
SET /a i=0

echo Choose the card formatting style. [33m(Use Arrow Keys and Enter to choose)[0m
echo.
echo.

:options
set "menuLine=    "
for /L %%n in (0,1,%maxIndex%) do (
    if %%n==%i% (set "color=%foc%") else (set "color=%unfoc%")
    set "menuLine=!menuLine!!color!!optionName%%n![0m"
    if not %%n==%maxIndex% set "menuLine=!menuLine! | "
)
echo [F!menuLine!

:keyloop
powershell -noprofile -command "while($true){$key=$Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');$code=$key.VirtualKeyCode;if($code -in 13,37,39){exit $code}}"
if %errorlevel%==13 goto execute
if %errorlevel%==37 (
    if %i% gtr 0 set /A i-=1
    goto options
)
if %errorlevel%==39 (
    if %i% lss %maxIndex% set /A i += 1
    goto options
)
goto keyloop

:execute 
echo.
echo The card will be formatted using !optionName%i%!.
for /f "delims=" %%F in ('powershell -command "Get-Clipboard"') do (set "clipboardContent=%%F")
echo --------------------------------------------
echo.
echo Clipboard content: [96m%clipboardContent%[0m
echo.
echo The Clipboard content will be passed as the List. 
set /p clipboardContent="Change list to [33m(or press Enter to keep current)[0m:"
echo --------------------------------------------
echo.
echo Calling [33mpython ./!option%i%! [96m%clipboardContent%[0m
echo.
python "./!option%i%!" %clipboardContent%

:end
echo [33mPress any key to shut the terminal...[0m
pause >nul