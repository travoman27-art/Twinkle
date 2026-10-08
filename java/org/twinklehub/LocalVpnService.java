package org.twinklehub;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.net.VpnService;
import android.os.Build;
import android.os.ParcelFileDescriptor;
import androidx.core.app.NotificationCompat;
import java.io.IOException;

public class LocalVpnService extends VpnService {
    private ParcelFileDescriptor mInterface;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        createNotificationChannel();
        Notification notification = new NotificationCompat.Builder(this, "vpn_channel")
                .setContentTitle("TwinkleHub VPN")
                .setContentText("Фильтрация серверов активна")
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .build();

        startForeground(1, notification);

        if (mInterface == null) {
            try {
                Builder builder = new Builder();
                builder.addAddress("10.0.0.2", 24);
                builder.addRoute("0.0.0.0", 0);
                builder.setSession("TwinkleHub Server Selector");
                
                // Исключаем само приложение из туннеля, чтобы сокеты пинга работали напрямую
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.L) {
                    builder.addDisallowedApplication(getPackageName());
                }

                mInterface = builder.establish();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return START_STICKY;
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    "vpn_channel",
                    "TwinkleHub VPN Service",
                    NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                manager.createNotificationChannel(channel);
            }
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (mInterface != null) {
            try {
                mInterface.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            mInterface = null;
        }
    }
}
