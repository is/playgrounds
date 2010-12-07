package us.yuxin.demo.hadoop.zero.userlogin;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;

public class ULMonthReducer extends
		Reducer<IntWritable, ULDistribution, IntWritable, ULDistribution> {

	@Override
	protected void reduce(IntWritable key, Iterable<ULDistribution> values,
			Context context) throws IOException, InterruptedException {
		ULDistribution uld = new ULDistribution();
		for (ULDistribution value : values) {
			uld.add(value);
		}
		context.write(key, uld);
	}
}
