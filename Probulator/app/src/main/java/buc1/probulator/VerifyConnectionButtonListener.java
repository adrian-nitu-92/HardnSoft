package buc1.probulator;

import android.app.Activity;
import android.content.Intent;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import buc1.probulator.buc1.communication.CommunicationInfo;

public class VerifyConnectionButtonListener implements View.OnClickListener {
	Activity activity;
    CommunicationInfo communicationInfo;
	
	public VerifyConnectionButtonListener(Activity activity) {
		this.activity = activity;
	}
	
	@Override
	public void onClick(View v) {
		if (v.getId() == R.id.verify_request_button) {
			getConnectionInfo();
			return;
		}
        getUrlConnection();
	}

    private void getUrlConnection() {
        String url = ((TextView) activity.findViewById(R.id.url_input))
                .getText().toString().trim();
        if (!checkmptyFieldErrorMessage(url, "Url cannot be an empty string")) {
            return;
        }

        communicationInfo = CommunicationInfo.getCommunicationInfo(url);

        Intent intent = new Intent(activity, MainActivity.class);
        intent.putExtra("PROTOCOL", "http");
        activity.startActivity(intent);
    }

	private void getConnectionInfo() {
		String protocol = ((TextView) activity.findViewById(R.id.protocol_input))
				.getText().toString().trim();
		if (!checkmptyFieldErrorMessage(protocol, "Protocol cannot be an empty string")) {
			return;
		}
		
		String ip = ((TextView) activity.findViewById(R.id.ip_input))
				.getText().toString().trim();
		if (!checkmptyFieldErrorMessage(ip, "Ip cannot be an empty string")) {
			return;
		}
		
		String port = ((TextView) activity.findViewById(R.id.port_input))
				.getText().toString().trim();
		if (!checkmptyFieldErrorMessage(port, "Ip cannot be an empty string")) {
			return;
		}
		
		communicationInfo = CommunicationInfo.getCommunicationInfo(protocol, ip, port);
		
		Intent intent = new Intent(activity, MainActivity.class);
		intent.putExtra("PROTOCOL", protocol);
		intent.putExtra("IP", ip);
		intent.putExtra("PORT", port);
		activity.startActivity(intent);
	}
	
	private boolean checkmptyFieldErrorMessage(String field, String errorMessage) {
		if (field == null || field.isEmpty()) {
			Toast.makeText(activity.getApplicationContext(),
                    errorMessage, Toast.LENGTH_LONG).show();
			return false;
		}
		System.out.println(field);
		return true;
	}
}
