# PyInstaller spec for LegalAI desktop application (windowed, no console).

from pathlib import Path

block_cipher = None
project_root = Path(SPECPATH)

hiddenimports = [
    "app",
    "app.desktop_ui",
    "app.settlement",
    "app.workbook",
    "app.call_script",
    "app.call_agent",
    "app.settings",
    "app.paths",
    "openpyxl",
]
datas = [
    (str(project_root / "data" / "sample_leads.csv"), "data"),
    (str(project_root / "web" / "index.html"), "web"),
]

a = Analysis(
    [str(project_root / "run_desktop.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["uvicorn", "fastapi", "httpx", "pytest"],
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
    name="LegalAI",
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
