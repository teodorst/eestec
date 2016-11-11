package Communication;

import java.sql.Timestamp;
import java.util.LinkedList;
import java.util.Queue;

/*will not contain more than 200 messages in one second interval*/
public class QueueFreqLimited {
	private class Pair<L,R> {

		  private final L left;
		  private final R right;

		  public Pair(L left, R right) {
		    this.left = left;
		    this.right = right;
		  }

		  public L getLeft() { return left; }
		  public R getRight() { return right; }

		  @Override
		  public int hashCode() { return left.hashCode() ^ right.hashCode(); }

		  @Override
		  public boolean equals(Object o) {
		    if (!(o instanceof Pair)) return false;
		    Pair pairo = (Pair) o;
		    return this.left.equals(pairo.getLeft()) &&
		           this.right.equals(pairo.getRight());
		  }

		}
	
	private static final short MESSAGE_CNT_LIMIT = 200;
	Queue<Pair<Object, Timestamp> > queue;
	
	public QueueFreqLimited() {
		queue = new LinkedList<Pair<Object, Timestamp>>();
	}
	
	// adds the object in the queue if the oldest message is newer than 1 second from current timestamp
	public boolean addObject(Object o) {
		boolean r = false;
		java.util.Date date = new java.util.Date();
		Timestamp currentTime = new Timestamp(date.getTime());
		
		if (queue.peek().getRight().getTime() - currentTime.getTime() <= 1000 
				&& queue.size() < MESSAGE_CNT_LIMIT) {
			queue.add(new Pair<Object, Timestamp>(o, currentTime));
			r = true;
		}
		
		return r;
	}
	
	public Object getObject() {
		return queue.poll();
	}
	
	public int getSize() {
		return queue.size();
	}
	
}
