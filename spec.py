block_cipher = None

a = Analysis(
    ["vpn_gui.py"],
    pathex=["."],
    binaries=[],
    datas=[("/opt/cisco/secureclient/bin/vpn", ".")],
    hiddenimports=[],
    hookspath=[],
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
    name="VPN_Connector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch="x86_64",
    codesign_identity="Developer ID Application: YOUR_ID",
    entitlements_file="entitlements.plist",
)

app = BUNDLE(
    exe,
    name="VPN_Connector.app",
    icon="vpn_icon.icns",
    bundle_identifier="com.yourcompany.vpnconnector",
    info_plist={
        "NSHighResolutionCapable": "True",
        "LSUIElement": "False",
        "CFBundleShortVersionString": "1.0.0",
    },
)
