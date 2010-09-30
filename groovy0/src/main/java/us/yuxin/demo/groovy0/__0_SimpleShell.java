package us.yuxin.demo.groovy0;

import java.io.IOException;

import groovy.lang.Binding;
import groovy.lang.GroovyShell;

public class __0_SimpleShell {
	public static void main(String[] args) throws IOException {
		Binding binding = new Binding();
		binding.setVariable("msg", "Hello World");
		binding.setVariable("id", new Integer(10));
		GroovyShell gs = new GroovyShell(binding);
		gs.evaluate("print msg + ':' + id");
	}
}
