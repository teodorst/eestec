package Communication;


public class PacketMsg {
	private static final short MAX_X = 640;
	private static final short MAX_Y = 480;
	
	private short X;
	private short Y;
	private boolean isPressed;
	
	public PacketMsg(short x, short y, boolean pressed) {
		X = x;
		Y = y;
		isPressed = pressed;
	}
	
	public boolean isValid() {
		return (X >= 0 && X <= MAX_X) && (Y >= 0 && Y <= MAX_Y); 
	}
	
	public String toString() {
		return X + "" + Y + "" + (isPressed ? 1 : 0); 
	}
}
