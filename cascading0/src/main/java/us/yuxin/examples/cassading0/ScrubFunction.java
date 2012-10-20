package us.yuxin.examples.cassading0;

import cascading.flow.FlowProcess;
import cascading.operation.BaseOperation;
import cascading.operation.Function;
import cascading.operation.FunctionCall;
import cascading.tuple.Fields;
import cascading.tuple.Tuple;
import cascading.tuple.TupleEntry;

/**
* Created with IntelliJ IDEA.
* User: is
* Date: 10/20/12
* Time: 7:15 PM
* To change this template use File | Settings | File Templates.
*/
public class ScrubFunction extends BaseOperation implements Function {
  public ScrubFunction(Fields fieldDeclaration) {
    super (2, fieldDeclaration);
  }

  public void operate(FlowProcess flowProcess, FunctionCall functionCall) {
    TupleEntry argument = functionCall.getArguments();
    String doc_id = argument.getString(0);
    String token = scrubText(argument.getString(1));

    if (token.length() > 0) {
      Tuple result = new Tuple();
      result.add(doc_id);
      result.add(token);
      functionCall.getOutputCollector().add(result);
    }
  }

  public String scrubText(String text) {
    return text.trim().toLowerCase();
  }
}
