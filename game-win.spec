# -*- mode: python -*-
a = Analysis(['game.py'],
             pathex=['C:\\Users\\nwint_000\\Documents\\GitHub\\AsteroidImpact'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='game.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('data', prefix='data'),
               strip=None,
               upx=True,
               name='game')
