package buc1.probulator.buc1.communication;

import java.util.List;

// SINGLETON
public class CommunicationInfo {
	public final String USER_AGENT = "Mozilla/5.0";
	public String protocol;
	public String ip;
	public String port;
	private static CommunicationInfo ci_ = null;
    public String url = null;
	
	private CommunicationInfo(String protocol, String ip, String port) {
		this.protocol = protocol;
		this.ip = ip;
		this.port = port;
	}
    private CommunicationInfo( String url) {
        this.protocol = "http";
        this.url = url;
    }

    public static CommunicationInfo getCommunicationInfo(String url) {
        if (ci_ == null) {
            ci_ = new CommunicationInfo(url);
        }

        if (!ci_.url.equals(url)) {
            ci_.url = url;
        }

        return ci_;
    }
	
	public static CommunicationInfo getCommunicationInfo(String protocol, String ip, String port) {
		if (ci_ == null) {
			ci_ = new CommunicationInfo(protocol, ip, port);
		}
		
		if (!ci_.protocol.equals(protocol)) {
			ci_.protocol = protocol;
		}
		
		if (!ci_.ip.equals(ip)) {
			ci_.ip = ip;
		}
		
		if (!ci_.port.equals(port)) {
			ci_.port = port;
		}
		
		return ci_;
	}

	public static CommunicationInfo getCommunicationInfo() {
		if (ci_ == null) {
			//TODO
		}
		
		return ci_;
	}


}
