package us.yuxin.examples.accumulo0;

import org.apache.accumulo.core.client.AccumuloException;
import org.apache.accumulo.core.client.AccumuloSecurityException;
import org.apache.accumulo.core.client.BatchWriter;
import org.apache.accumulo.core.client.Connector;
import org.apache.accumulo.core.client.TableNotFoundException;
import org.apache.accumulo.core.client.ZooKeeperInstance;
import org.apache.accumulo.core.data.Mutation;
import org.apache.accumulo.core.data.Value;
import org.apache.accumulo.core.security.ColumnVisibility;
import org.apache.hadoop.io.Text;

public class Cli0 {
  public static void main(String p[]) throws AccumuloSecurityException, AccumuloException, TableNotFoundException {
    String instanceName = "is";
    String zooKeepers = "h4a0";
    String tableName = "exam0";
    ColumnVisibility colVis = new ColumnVisibility("public");

    String user = "is";
    byte[] pass = "ispass_12_".getBytes();

    ZooKeeperInstance instance = new ZooKeeperInstance(instanceName, zooKeepers);
    Connector connector = instance.getConnector(user, pass);

    BatchWriter bw = connector.createBatchWriter(tableName, 204800, 10000, 2);
    long baseid = System.currentTimeMillis();

    for (int i = 0; i < 100; ++i) {
      baseid += 1;
      Text rowid = new Text(String.format("row_%016x", baseid));
      // System.out.println(rowid);

      Mutation mutation = new Mutation(rowid);
      mutation.put(new Text("foo"),
        new Text("1"), colVis,
        new Value(rowid.toString().getBytes()));
      mutation.put(new Text("foo"),
        new Text("2"), colVis,
        new Value("Hello World".getBytes()));
      bw.addMutation(mutation);
    }
    bw.close();
  }
}
