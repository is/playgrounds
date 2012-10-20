package us.yuxin.examples.accumulo.ingest;


public class Ingest {
  public final static String CONF_ACCULUMO_CONNECTION_TOKEN = "ingest.accumulo.token";
  public final static String CONF_ACCULUMO_MAX_MEMORY = "ingest.accumulo.max.memory";
  public final static String CONF_ACCUMULO_MAX_LATENCY = "ingest.accumulo.max.latency";
  public final static String CONF_ACCUMULO_MAX_WRITE_THREADS = "ingest.accumulo.max.write.threads";

  protected final static int ACCUMULO_MAX_MEMORY = 1024000;
  protected final static int ACCUMULO_MAX_LATENCY = 1000;
  protected final static int ACCUMULO_MAX_WRITE_THREADS = 2;
}
