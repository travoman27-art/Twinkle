import os
from pathlib import Path

def patch_manifest():
    # Автоматически ищем все файлы AndroidManifest.xml в рабочей директории сборки
    for root, dirs, files in os.walk("."):
        if "AndroidManifest.xml" in files:
            manifest_path = Path(root) / "AndroidManifest.xml"
            try:
                content = manifest_path.read_text(encoding="utf-8", errors="ignore")
                
                # Проверяем, что наш сервис еще не добавлен и файл содержит тег приложения
                if "org.twinklehub.LocalVpnService" not in content and "</application>" in content:
                    service_tag = '''
        <service
            android:name="org.twinklehub.LocalVpnService"
            android:permission="android.permission.BIND_VPN_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.net.VpnService" />
            </intent-filter>
        </service>
    </application>'''
                    
                    content = content.replace("</application>", service_tag)
                    manifest_path.write_text(content, encoding="utf-8")
                    print(f"[Hook Success] Успешно добавлен VPN-сервис в: {manifest_path}")
            except Exception as e:
                pass

# Запускаем патч при импорте хука сборщиком
patch_manifest()
