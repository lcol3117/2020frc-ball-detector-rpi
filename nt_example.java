import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;

public static double[] getRaspberryValues() {
  double[] values = new double[4];
  NetworkTable table = NetworkTableInstance.getDefault().getTable("FRCVisionpc");
  NetworkTableEntry tx = table.getEntry("pi_tx");
  NetworkTableEntry ty = table.getEntry("pi_ty");
  NetworkTableEntry ta = table.getEntry("pi_ta");

  //read values periodically
  values[1] = tx.getDouble(0.0);
  values[2] = ty.getDouble(0.0);
  values[3] = ta.getDouble(0.0);
  values[0] = ((values[1]==-1)&&(values[2]==-1))?0:1;
  return values;
}
