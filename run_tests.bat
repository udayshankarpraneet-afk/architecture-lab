@echo off
title ARCHITECTURE LAB - Test Suite Runner
color 0A

echo ======================================================================
echo             ARCHITECTURE LAB - AUTOMATED TEST SUITE RUNNER
echo ======================================================================
echo.

python -m pytest backend/tests -v
echo.
if errorlevel 0 (
    echo [SUCCESS] All 16 automated tests passed successfully!
) else (
    echo [FAILURE] Some tests failed. Please review the output above.
)
echo.
pause
