package buc1.probulator.buc1.communication;

import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class CommunicationThread extends Thread {
	private final CommunicationInfo communicationInfo;
	private String path;
	private int responseCode;
    private Storage storage;
	
	public CommunicationThread(Storage storage, String path) {
		this.communicationInfo = CommunicationInfo.getCommunicationInfo();
		this.path = path;
        this.storage = storage;
	}
	
	@Override
	public void run() {
        if (communicationInfo.url != null) {
            try {
                String url = communicationInfo.protocol + "://" +communicationInfo.url + path;
                System.err.println(url);
                URL obj = new URL(url);
                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                con.setRequestMethod("GET");
                con.setRequestProperty("User-Agent", communicationInfo.USER_AGENT);
                responseCode = con.getResponseCode();
                InputStream in = con.getInputStream();
                String encoding = con.getContentEncoding();
                encoding = encoding == null ? "UTF-8" : encoding;

                StringWriter writer = new StringWriter();
                IOUtils.copy(in, writer, encoding);
                final String theString = writer.toString();

                System.out.println("\nSending 'GET' request to URL : " + url);
                System.out.println("Response Code : " + responseCode);


                storage.update(theString);
            } catch (MalformedURLException e) {
                System.out.println("MalformedURLException");
                e.printStackTrace();
                //responseEvent.responseReady(responseCode);
            } catch (IOException e) {
                System.out.println("IOException");
                e.printStackTrace();
                //responseEvent.responseReady(responseCode);
            }
            return ;
        }
		try {
			String url = communicationInfo.protocol + "://" +communicationInfo.ip +
					":" + communicationInfo.port + path;
			System.err.println(url);
			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();
			con.setRequestMethod("GET");
			con.setRequestProperty("User-Agent", communicationInfo.USER_AGENT);
			responseCode = con.getResponseCode();
            InputStream in = con.getInputStream();
            String encoding = con.getContentEncoding();
            encoding = encoding == null ? "UTF-8" : encoding;

            StringWriter writer = new StringWriter();
            IOUtils.copy(in, writer, encoding);
            final String theString = writer.toString();

			System.out.println("\nSending 'GET' request to URL : " + url);
			System.out.println("Response Code : " + responseCode);


            storage.update(theString);
		} catch (MalformedURLException e) {
			System.out.println("MalformedURLException");
			e.printStackTrace();
			//responseEvent.responseReady(responseCode);
		} catch (IOException e) {
			System.out.println("IOException");
			e.printStackTrace();
			//responseEvent.responseReady(responseCode);
		}
	}
	
	public synchronized int getResponseCode() {
		return responseCode;
	}

}
