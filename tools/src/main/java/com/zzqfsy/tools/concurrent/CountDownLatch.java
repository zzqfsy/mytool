package com.zzqfsy.tools.concurrent;

import java.util.concurrent.locks.AbstractQueuedSynchronizer;

public class CountDownLatch {

    /**
     * 同步控制
     * 使用AQS状态计数
     */
    private static final class Sync extends AbstractQueuedSynchronizer {
        private static final long seriaalVersionUID = 1L;

        Sync(int count){
            setState(count);
        }

        int getCount(){
            return getState();
        }

    }
}
