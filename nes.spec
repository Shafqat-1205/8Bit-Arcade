# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['nes.py'],
    pathex=[],
    binaries=[],
    datas=[('NES Games', 'NES Games'), ('NES Games\\fceux.exe', 'NES Games'), ('new_arrow.png', '.'), ('move.mp3', '.'), ('move.wav', '.'), ('select.wav', '.'), ('PressStart2P.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='nes',
)
