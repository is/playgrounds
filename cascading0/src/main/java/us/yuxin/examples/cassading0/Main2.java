package us.yuxin.examples.cassading0;


import java.util.Properties;

import cascading.flow.Flow;
import cascading.flow.FlowDef;
import cascading.flow.local.LocalFlowConnector;
import cascading.operation.Identity;
import cascading.operation.aggregator.Count;
import cascading.operation.regex.RegexSplitGenerator;
import cascading.pipe.Each;
import cascading.pipe.Every;
import cascading.pipe.GroupBy;
import cascading.pipe.Pipe;
import cascading.property.AppProps;
import cascading.scheme.local.TextLine;
import cascading.tap.Tap;
import cascading.tap.local.FileTap;
import cascading.tuple.Fields;

public class Main2 {
  public static void main(String[] args) throws InterruptedException {
    Properties properties = new Properties();
    AppProps.setApplicationJarClass(properties, Main2.class);
    LocalFlowConnector flowConnector = new LocalFlowConnector();

    String inPath = "data/piece";
    String outPath = "data/res2";

    Pipe docPipe;

    Fields text = new Fields("text");
    Fields token = new Fields("token");

    Fields fieldSelector = new Fields("doc_id", "token");
    Fields scrubArgument = new Fields("doc_id", "token");

    docPipe = new Pipe("doc");
    docPipe = new Each(docPipe, new Fields("num", "line"),
      new Identity(new Fields("doc_id", "text")));

    RegexSplitGenerator splitter = new RegexSplitGenerator(token, "[ \\[\\]\\(\\),.:=|\"]");
    docPipe = new Each(docPipe, text, splitter, fieldSelector);
    docPipe = new Each(docPipe, scrubArgument, new ScrubFunction(fieldSelector), Fields.RESULTS);

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
    flow.writeDOT("data/main2.dot");
    flow.complete();

  }


}
