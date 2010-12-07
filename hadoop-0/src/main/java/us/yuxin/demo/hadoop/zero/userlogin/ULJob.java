package us.yuxin.demo.hadoop.zero.userlogin;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;


import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.partition.HashPartitioner;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class ULJob extends Configured implements Tool {
	@Override
	public int run(String[] args) throws Exception {
		Configuration conf = getConf();

		Job job0 = new Job(conf, "UserLogin");
		job0.setJarByClass(ULJob.class);

		FileInputFormat.setInputPaths(job0, args[0]);
		FileOutputFormat.setOutputPath(job0, new Path(args[1]));
		
		job0.setMapperClass(ULMapper.class);
		job0.setReducerClass(ULUserReducer.class);

		job0.setMapOutputKeyClass(Text.class);
		job0.setMapOutputValueClass(IntWritable.class);

		job0.setOutputKeyClass(IntWritable.class);
		job0.setOutputValueClass(ULDistribution.class);
		
		job0.setInputFormatClass(TextInputFormat.class);
		job0.setOutputFormatClass(SequenceFileOutputFormat.class);

		job0.setNumReduceTasks(13);
		job0.setPartitionerClass(HashPartitioner.class);
		
		if (!job0.waitForCompletion(true))
			return 1;
		
		Job job1 = new Job(conf, "UserLoginGroup");
		job1.setJarByClass(ULJob.class);
		
		FileInputFormat.setInputPaths(job1, args[1]);
		FileOutputFormat.setOutputPath(job1, new Path(args[2]));
		
		job1.setReducerClass(ULMonthReducer.class);
		job1.setMapOutputKeyClass(IntWritable.class);
		job1.setMapOutputValueClass(ULDistribution.class);
		job1.setOutputKeyClass(IntWritable.class);
		job1.setOutputValueClass(ULDistribution.class);

		job1.setPartitionerClass(HashPartitioner.class);
		job1.setNumReduceTasks(13);

		job1.setInputFormatClass(SequenceFileInputFormat.class);
		job1.setOutputFormatClass(TextOutputFormat.class);
		
		if (!job1.waitForCompletion(true))
			return 1;
		
		return 0;
	}
	
	public static void main(String args[]) throws Exception {
		ToolRunner.run(new Configuration(), new ULJob(), args);
	}
}
