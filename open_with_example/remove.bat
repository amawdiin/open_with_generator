
@echo off

reg delete HKEY_CLASSES_ROOT\Directory\background\shell\OpenWithExample /f
reg delete HKEY_CLASSES_ROOT\*\shell\OpenWithExample /f
reg delete HKEY_CLASSES_ROOT\Directory\shell\OpenWithExample /f
    