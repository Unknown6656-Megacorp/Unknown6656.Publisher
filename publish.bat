@echo off
IF EXIST publish.py (
    python publish.py "%~f0"
) ELSE (
    IF EXIST ../Unknown6656.Publisher/publish.py (
        python ../Unknown6656.Publisher/publish.py "%~f0"
    ) ELSE (
        echo "The file 'publish.py' does not seem to exist in the current dir or inside of '../Unknown6656.Publisher'."
        echo "Please clone 'https://github.com/Unknown6656-Megacorp/Unknown6656.Publisher' into the current or corresponding directoy."
    )
)