# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['calibrationWindow.py'],
             pathex=['C:\\Users\\PC\\PycharmProjects\\EyeTrackerBackground'],
             binaries=[],
             datas=[],
             hiddenimports=[
              'tobiiresearch.implementation.ExternalSignalData',
                'tobiiresearch.implementation.EyeImageData',
                'tobiiresearch.implementation.EyeTracker',
                'tobiiresearch.implementation.ScreenBasedCalibration',
                'tobiiresearch.implementation.HMDBasedCalibration',
                'tobiiresearch.implementation.ScreenBasedMonocularCalibration',
                'tobiiresearch',
                'tobiiresearch.implementation'
                ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('v', None, 'OPTION')],
          name='BackgroundEyeTrackerCalibration',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
