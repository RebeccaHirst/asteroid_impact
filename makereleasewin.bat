@REM makereleasewin.bat

@REM build documentation
cd doc
call make html
if errorlevel 1 goto somethingbad
cd ..

@REM build source zip
del "dist\AsteroidImpact Source.zip"
7z a "dist\AsteroidImpact Source.zip" *.py *.json *.txt data\ doc\ levels\
if errorlevel 1 goto somethingbad

@REM build standalone
pyinstaller.exe game-win.spec --noconfirm
if errorlevel 1 goto somethingbad

@REM build standalone zip
del "dist\AsteroidImpact Standalone Windows.zip"
cd dist
7z a "AsteroidImpact Standalone Windows.zip" game\
if errorlevel 1 goto somethingbad
cd ..

echo Success!
@goto end

:somethingbad
echo ERROR: See above.

:end
