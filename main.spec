# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Percorso al file __version__ di Pinecone
#pinecone_version_file = '/opt/miniconda3/envs/chunker/lib/python3.12/site-packages/pinecone/__version__'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('/opt/miniconda3/envs/chunker/lib/python3.12/site-packages/pinecone/__version__', 'pinecone')],
    hiddenimports=['pydantic', 'pydantic_core', 'pydantic-settings', 'pydantic.deprecated.decorator', 'tiktoken_ext.openai_public', 'tiktoken_ext.openai_public', 'numpy'],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
