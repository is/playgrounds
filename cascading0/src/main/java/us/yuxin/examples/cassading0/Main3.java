package us.yuxin.examples.cassading0;

import cascading.flow.Flow;
import cascading.flow.FlowDef;
import cascading.flow.local.LocalFlowConnector;
import cascading.operation.aggregator.Count;
import cascading.operation.regex.RegexSplitGenerator;
import cascading.pipe.Each;
import cascading.pipe.Every;
import cascading.pipe.GroupBy;
import cascading.pipe.HashJoin;
import cascading.pipe.Pipe;
import cascading.pipe.assembly.Retain;
import cascading.pipe.joiner.LeftJoin;
import cascading.scheme.local.TextDelimited;
import cascading.tap.Tap;
import cascading.tap.local.FileTap;
import cascading.tuple.Fields;

public class Main3 {
  public static void main(String[] args) {
    LocalFlowConnector flowConnector = new LocalFlowConnector();

    String docPath = "data/i4/rain.txt";
    String wcPath = "data/i4/wc";
    String stopPath = "data/i4/en.stop";

    Tap docTap = new FileTap(new TextDelimited(true, "\t"), docPath);
    Tap wcTap = new FileTap(new TextDelimited(true, "\t"), wcPath);

    Fields stop = new Fields("stop");
    Tap stopTap = new FileTap(new TextDelimited(stop, true, "\t"), stopPath);


    Fields token = new Fields("token");
    Fields text = new Fields("text");

    RegexSplitGenerator splitter = new RegexSplitGenerator(token, "[ \\[\\]\\(\\),.]" );
    Fields fieldSelector = new Fields("doc_id", "token");
    Pipe docPipe = new Each("token", text, splitter, fieldSelector);

    Fields scrubArguments = new Fields( "doc_id", "token" );
    docPipe = new Each(docPipe, scrubArguments, new ScrubFunction(scrubArguments), Fields.RESULTS);


    Pipe stopPipe = new Pipe("stop");
    Pipe tokenPipe = new HashJoin(docPipe, token, stopPipe, stop, new LeftJoin());

    Pipe wcPipe = new Pipe("wc", tokenPipe);
    wcPipe = new Retain(wcPipe, token);
    wcPipe = new GroupBy(wcPipe, token);
    wcPipe = new Every(wcPipe, Fields.ALL, new Count(), Fields.ALL);

    FlowDef flowDef = FlowDef.flowDef()
      .setName( "wc" )
      .addSource( docPipe, docTap )
      .addSource( stopPipe, stopTap )
      .addTailSink( wcPipe, wcTap );

    // write a DOT file and run the flow
    Flow wcFlow = flowConnector.connect( flowDef );
    wcFlow.writeDOT( "data/main3.dot" );
    wcFlow.complete();

  }
}
