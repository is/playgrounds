package us.yuxin.examples.cassading0;


import java.util.Properties;

import cascading.flow.Flow;
import cascading.flow.FlowDef;
import cascading.flow.local.LocalFlowConnector;
import cascading.operation.aggregator.Count;
import cascading.operation.regex.RegexSplitGenerator;
import cascading.pipe.Each;
import cascading.pipe.Every;
import cascading.pipe.GroupBy;
import cascading.pipe.Pipe;
import cascading.property.AppProps;
import cascading.scheme.local.TextDelimited;
import cascading.scheme.local.TextLine;
import cascading.tap.Tap;
import cascading.tap.local.FileTap;
import cascading.tuple.Fields;

public class Main1 {
  public static void main(String[] args) throws InterruptedException {
    Properties properties = new Properties();
    AppProps.setApplicationJarClass(properties, Main1.class);
    LocalFlowConnector flowConnector = new LocalFlowConnector();

    String inPath = "data/piece";
    String outPath = "data/res1";

    Fields token = new Fields("token");
    Fields text = new Fields("line");

    RegexSplitGenerator splitter = new RegexSplitGenerator(token, "[ \\[\\]\\(\\),.:=|\"]");
    Pipe docPipe = new Each("token", text, splitter, Fields.RESULTS);
    Pipe wcPipe = new Pipe("wc", docPipe);

    wcPipe = new GroupBy(wcPipe, token);
    wcPipe = new Every(wcPipe, Fields.ALL, new Count(), Fields.ALL);

    Tap inTap = new FileTap(new TextLine(), inPath);
    Tap outTap = new FileTap(new TextLine(), outPath);

    FlowDef flowDef = FlowDef.flowDef()
      .setName("wc")
      .addSource(docPipe, inTap)
      .addTailSink(wcPipe, outTap);

    Flow flow = flowConnector.connect(flowDef);
    flow.complete();
    flow.writeDOT("main1.dot");
  }
}
