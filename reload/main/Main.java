import java.io.File;
import java.net.URLClassLoader;
import java.net.URL;

import com.google.common.io.Files;

public class Main {
	public static void main(String args[]) throws Exception {
		File cp = new File("o/s");
		String classname = "Processor";
		
		Runtime runtime = Runtime.getRuntime();

		BaseProcessor proc = null;
		fileCopy(new File("o/0/Processor.class"), new File("o/s/Processor.class"));
		proc = getProcessor(cp, classname);
		proc.print();


		fileCopy(new File("o/1/Processor.class"), new File("o/s/Processor.class"));
		proc = getProcessor(cp, classname);
		proc.print();

		fileCopy(new File("o/0/Processor.class"), new File("o/s/Processor.class"));
		proc = getProcessor(cp, classname);
		proc.print();
	}

	public static BaseProcessor getProcessor(
		File basePath, String classname) throws Exception { 
		URL classPath[] = new URL[] {basePath.toURI().toURL()};
		URLClassLoader classLoader = new URLClassLoader(
			classPath, Main.class.getClassLoader());
		return (BaseProcessor)classLoader.loadClass(classname).newInstance();
	}

	public static void fileCopy(File from, File to) throws Exception {
		if (to.exists()) {
			to.delete();
		}

		Files.copy(from, to);
	}
}