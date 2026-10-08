package org.twinklehub;

import android.content.Intent;
import android.net.VpnService;
import android.os.ParcelFileDescriptor;
import java.io.IOException;

public class LocalVpnService extends VpnService {
    private ParcelFileDescriptor mInterface;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (mInterface == null) {
            try {
                Builder builder = new Builder();
                builder.addAddress("10.0.0.2", 24);
                builder.addRoute("0.0.0.0", 0);
                builder.setSession("TwinkleHub Server Selector");
                mInterface = builder.establish();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return START_STICKY;
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
