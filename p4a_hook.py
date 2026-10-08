from pathlib import Path
from pythonforandroid.toolchain import ToolchainCL

def after_apk_build(toolchain: ToolchainCL):
    pass

def before_apk_build(toolchain: ToolchainCL):
    # Находим сгенерированный AndroidManifest.xml перед компиляцией APK
    manifest_path = Path(toolchain._dist.dist_dir) / "src" / "main" / "AndroidManifest.xml"
    if manifest_path.exists():
        content = manifest_path.read_text(encoding="utf-8")
        
        # Если сервис еще не прописан, внедряем его внутрь тега <application>
        service_tag = '''
        <service
            android:name="org.twinklehub.LocalVpnService"
            android:permission="android.permission.BIND_VPN_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.net.VpnService" />
            </intent-filter>
        </service>
        </application>
        '''
        
        if "org.twinklehub.LocalVpnService" not in content:
            content = content.replace("</application>", service_tag)
            manifest_path.write_text(content, encoding="utf-8")
            print("[Hook] LocalVpnService успешно добавлен в AndroidManifest.xml!")
          
