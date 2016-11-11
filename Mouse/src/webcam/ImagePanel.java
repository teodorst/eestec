package webcam;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

import javax.swing.JPanel;

public class ImagePanel extends JPanel {
	
	private BufferedImage image;
	
	public ImagePanel() {
		super();
	}

	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		g.drawImage(this.image, 10, 10, this.image.getWidth(), this.image.getHeight(), null);
		g.setColor(Color.WHITE);
		
	}
	
}
