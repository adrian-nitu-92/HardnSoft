package buc1.probulator.buc1.communication;

import android.os.SystemClock;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Updater extends Thread {
    Storage storage;
	private static int nrExec = 0;
	
	public Updater(Storage storage) {
		System.out.println("Update created");
		this.storage = storage;
	}
	
	@Override
	public void run() {
        //pt debug
		++nrExec;
		if (nrExec > 1) {
			System.out.println("here!!!!!!!!!!!!!");
			return;
		}
		ExecutorService svc = Executors.newFixedThreadPool(1);
		svc.submit( new Runnable() {

			@Override
			public void run() {
				System.out.println("Update.run a fost apelat");
				while (true) {
                    CommunicationThread t =
                            new CommunicationThread(
                                    storage,
                                    "/getChartsData");
                    t.start();
                    try {
                        t.join();
                    }
                    catch (Exception e) {
                    }
					SystemClock.sleep(10000);
				}
			}
			
		});
		/*svc.shutdown();
		try {
			svc.awaitTermination(30000, TimeUnit.SECONDS);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}*/
		
	}
}
