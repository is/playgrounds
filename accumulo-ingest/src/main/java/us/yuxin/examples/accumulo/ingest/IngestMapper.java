package us.yuxin.examples.accumulo.ingest;


import java.io.IOException;
import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

import com.google.common.base.Splitter;
import org.apache.accumulo.core.client.AccumuloException;
import org.apache.accumulo.core.client.AccumuloSecurityException;
import org.apache.accumulo.core.client.BatchWriter;
import org.apache.accumulo.core.client.Connector;
import org.apache.accumulo.core.client.MutationsRejectedException;
import org.apache.accumulo.core.client.TableNotFoundException;
import org.apache.accumulo.core.client.ZooKeeperInstance;
import org.apache.accumulo.core.data.Mutation;
import org.apache.accumulo.core.data.Value;
import org.apache.accumulo.core.security.ColumnVisibility;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;
import org.codehaus.jackson.map.ObjectMapper;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

public class IngestMapper implements Mapper<LongWritable, Text, NullWritable, NullWritable> {
  ObjectMapper mapper;
  protected DateTimeFormatter timeFmt;
  AtomicInteger serial;
  AtomicInteger oidSerial;

  ColumnVisibility columnVisbility;

  ZooKeeperInstance instance;
  Connector connector;
  BatchWriter writer;

  JobConf job;

  protected Text createRowId(Map<String, Object> data) {
    Long ots = null;
    Object ov;

    ov = data.get("logTimestamp");
    if (ov == null) {
      //return new Text("9999");
      return null;
    }

    if (ov instanceof Long) {
      ots = (Long)ov;
    } else if (ov instanceof Integer) {
      // logger.warn("Invalid logTimestamp(int) - raw-log:" + new String(event.getBody()));
      ots = ((Integer)ov).longValue();
    } else if (ov instanceof String) {
      // logger.warn("Invalid logTimestamp(string) - raw-log:" + new String(event.getBody()));
      ots = Long.parseLong((String)ov);
    }

    if (ots == null) {
      // logger.warn("Invalid logTimestamp(empty) - raw-log:" + new String(event.getBody()));
      // return new Text("9999");
      return null;
    }

    Integer oid = (Integer)data.get("oid");
    if (oid == null)
      oid = oidSerial.incrementAndGet();

    Integer ser = serial.incrementAndGet();
    return  new Text(String.format("%s.%04d%04d",
      timeFmt.print(ots), oid % 10000, ser % 10000));
  }


  protected void createConnection()
    throws AccumuloSecurityException, AccumuloException, TableNotFoundException {

    String connectionToken = job.get(Ingest.CONF_ACCULUMO_CONNECTION_TOKEN);

    Iterator<String> tokens = Splitter.on(':').split(connectionToken).iterator();

    String instanceName = tokens.next();
    String zooKeepers = tokens.next();
    String user = tokens.next();
    String password = tokens.next();
    String visibility = tokens.next();
    String tableName = tokens.next();

    instance = new ZooKeeperInstance(instanceName, zooKeepers);
    connector = instance.getConnector(user, password.getBytes());
    writer = connector.createBatchWriter(tableName,
      job.getInt(Ingest.CONF_ACCULUMO_MAX_MEMORY, Ingest.ACCUMULO_MAX_MEMORY),
      job.getInt(Ingest.CONF_ACCUMULO_MAX_LATENCY, Ingest.ACCUMULO_MAX_LATENCY),
      job.getInt(Ingest.CONF_ACCUMULO_MAX_WRITE_THREADS, Ingest.ACCUMULO_MAX_WRITE_THREADS));
    columnVisbility = new ColumnVisibility(visibility);
  }


  protected void closeConnection() {
    if (writer != null) {
      try {
        writer.close();
      } catch (MutationsRejectedException e) {
        // TODO: logger.warn("Unable to shutdown Accumulo Batch Writer", e);
      }
      writer = null;
    }

    connector = null;
    instance = null;
  }


  @Override
  public void configure(JobConf conf) {
    this.job = conf;
    mapper = new ObjectMapper();
    timeFmt = DateTimeFormat.forPattern("YYYYMMddHHmmssSSS");
    oidSerial = new AtomicInteger(0);
    serial = new AtomicInteger(0);
  }


  @Override
  public void map(LongWritable key, Text value, OutputCollector<NullWritable, NullWritable> nullWritableNullWritableOutputCollector, Reporter reporter) throws IOException {
    // skip blank line.
    if (value.getLength() == 0)
      return;

    byte[] raw = value.getBytes();
    try {
      Map<String, Object> msg = mapper.readValue(raw, Map.class);
      Text rowId = createRowId(msg);
      if (rowId == null) {
        // TODO ... Error Handler
        return;
      }

      Mutation mutation = new Mutation(rowId);
      mutation.put(new Text("raw"), value, columnVisbility, new Value(new byte[0]));

      for (String k: msg.keySet()) {
        if (k.startsWith("__"))
          continue;

        Object v = msg.get(k);

        if (v == null)
          continue;

        if (v.equals(""))
          continue;

        mutation.put(new Text("a"), new Text(k.toLowerCase()),
          columnVisbility, new Value(v.toString().getBytes()));
      }

      if (writer == null) {
        createConnection();
      }

      writer.addMutation(mutation);
    } catch (Exception e) {
      // TODO ... Error Handler
    }
  }



  @Override
  public void close() throws IOException {
    closeConnection();
  }
}
