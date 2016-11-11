package Communication;

import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class ServerCommunicator {
	Socket sock;
	// Queue
	
	public ServerCommunicator(String ipAddress, int port) {
		try {
			sock = new Socket(ipAddress, port);
		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void sendMessage(PacketMsg msgToSend) {
		if (!msgToSend.isValid())
			return;

		byte[] msg = msgToSend.toString().getBytes();
		try {
			sock.getOutputStream().write(msg);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
