# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TechMaster.py'],
    pathex=[],
    binaries=[],
    datas=[('BGmusic.wav', '.'), ('correct.wav', '.'), ('wrong.wav', '.'), ('1 TO 10.wav', '.'), ('10 TO 15.wav', '.'), ('15 TO 20.wav', '.'), ('highscores.json', '.'), ('leaderboard.json', '.'), ('players.json', '.')],
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
    a.binaries,
    a.datas,
    [],
    name='TechMaster',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
