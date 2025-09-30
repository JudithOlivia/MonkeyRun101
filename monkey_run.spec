
block_cipher = None

a = Analysis(
    ['monkey_run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('StartBG.png', '.'),
        ('Background.png', '.'),
        ('Player2.png', '.'),
        ('Ground.png', '.'),
        ('snake.png', '.'),
        ('float.png', '.'),
        ('Thorn.png', '.'),
        ('lake.png', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MonkeyRun',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  
    icon='monkey_icon.ico' 
)