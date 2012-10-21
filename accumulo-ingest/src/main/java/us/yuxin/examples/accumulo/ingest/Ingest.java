package us.yuxin.examples.accumulo.ingest;


import java.net.URL;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class Ingest extends Configured implements Tool {
  public final static String CONF_ACCULUMO_CONNECTION_TOKEN = "ingest.accumulo.token";
  public final static String CONF_ACCULUMO_MAX_MEMORY = "ingest.accumulo.max.memory";
  public final static String CONF_ACCUMULO_MAX_LATENCY = "ingest.accumulo.max.latency";
  public final static String CONF_ACCUMULO_MAX_WRITE_THREADS = "ingest.accumulo.max.write.threads";

  protected final static int ACCUMULO_MAX_MEMORY = 1024000;
  protected final static int ACCUMULO_MAX_LATENCY = 1000;
  protected final static int ACCUMULO_MAX_WRITE_THREADS = 2;


  @Override
  public int run(String[] args) throws Exception {
    Configuration conf = getConf();

    JobConf job = new JobConf(conf);
    job.setJobName(String.format("accumulo-ingest--%d", System.currentTimeMillis()));
    job.setInputFormat(TextInputFormat.class);
    job.setMapperClass(IngestMapper.class);

    FileInputFormat.setInputPaths(job, new Path(args[0]));
    JobClient.runJob(job);
    return 0;
  }


  protected static Configuration prepareConfiguration() {
    Configuration conf = new Configuration();
    ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
    if (classLoader == null) {
      classLoader = Ingest.class.getClassLoader();
    }

    URL defaultURL = classLoader.getResource("ingest-default.xml");
    if (defaultURL != null)
      conf.addResource(defaultURL);

    URL siteURL = classLoader.getResource("ingest-site.xml");
    if (siteURL != null)
      conf.addResource(siteURL);

    return conf;
  }


  public static void main(String[] args) throws Exception {
    Configuration conf = prepareConfiguration();
    int res = ToolRunner.run(conf, new Ingest(), args);
    System.exit(res);
  }
}
