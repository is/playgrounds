package us.yuxin.examples.cassading0;


import java.util.Properties;

import cascading.flow.Flow;
import cascading.flow.FlowDef;
import cascading.flow.local.LocalFlowConnector;
import cascading.pipe.Pipe;
import cascading.property.AppProps;
import cascading.scheme.local.TextLine;
import cascading.tap.Tap;
import cascading.tap.local.FileTap;
import cascading.tuple.Fields;

public class Main0 {
  public static void main(String[] args) throws InterruptedException {
    Properties properties = new Properties();
    AppProps.setApplicationJarClass(properties, Main0.class);
    LocalFlowConnector flowConnector = new LocalFlowConnector();

    Tap inTap = new FileTap(new TextLine(new Fields("num", "line")), "data/piece");
    Tap outTap = new FileTap(new TextLine(new Fields("line")), "data/res");
    Pipe copyPipe = new Pipe("copy");

    FlowDef flowDef = FlowDef.flowDef()
      .addSource(copyPipe, inTap)
      .addTailSink(copyPipe, outTap);

    Flow flow = flowConnector.connect(flowDef);
    flow.complete();
  }
}
