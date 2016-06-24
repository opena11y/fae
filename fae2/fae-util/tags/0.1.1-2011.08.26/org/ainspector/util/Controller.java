package org.ainspector.util;

import org.apache.commons.cli.*;

/**
 * Read command-line arguments and store values as constants. These values
 * are used to control the execution of methods in the collaborative class.
 */
public class Controller {

  // Exported constants
  public final String SCRIPTS_FILE;
  public final String URLS_FILE;
  public final String OUTPUT_DIRECTORY;
  public final boolean DEBUG;
  public final boolean VERBOSE;

  /**
   * Constructor
   * @param syntax (command invocation syntax not including options and arguments)
   * @param args (command-line arguments passed in from main method)
   */
  public Controller(String syntax, String[] args) {
    SYNTAX = syntax;

    initOptions();
    initCmdLine(args);

    // Check for mandatory args
    if (!cmdLine.hasOption(scriptsFile.getOpt())) {
      printUsage();
      System.exit(1);
    }
    SCRIPTS_FILE = cmdLine.getOptionValue(scriptsFile.getOpt());

    if (!cmdLine.hasOption(urlsFile.getOpt())) {
      printUsage();
      System.exit(1);
    }
    URLS_FILE = cmdLine.getOptionValue(urlsFile.getOpt());

    if (!cmdLine.hasOption(outputDirectory.getOpt())) {
      printUsage();
      System.exit(1);
    }
    OUTPUT_DIRECTORY = cmdLine.getOptionValue(outputDirectory.getOpt());

    // Initialize optional args
    DEBUG = cmdLine.hasOption(debug.getOpt());
    VERBOSE = cmdLine.hasOption(verbose.getOpt());
  }

  /**
   * Initialize and populate the Options container
   */
  private void initOptions() {
    options = new Options();

    options.addOption(scriptsFile);
    options.addOption(urlsFile);
    options.addOption(outputDirectory);
    options.addOption(debug);
    options.addOption(verbose);
  }

  /**
   * Initialize the cmdLine variable by parsing command-line arguments.
   * If any exceptions occur, print error and usage messages, and exit.
   * @param args (command-line arguments)
   */
  private void initCmdLine(String[] args){
    CommandLineParser parser = new PosixParser();

    try {
      cmdLine = parser.parse(options, args);
    }
    catch (ParseException e) {
      printException(PARSE_ERROR, e);
      printUsage();
      System.exit(1);
    }
  }

  /**
   * Print the help text.
   */
  private void printUsage() {
    HelpFormatter formatter = new HelpFormatter();
    formatter.printHelp(SYNTAX, options);
  }

  /**
   * Print an exception message.
   * @param prefix (set the context of the message)
   * @param e (the exception whose message will be printed)
   */
  private void printException(String prefix, Exception e) {
    String sep = System.getProperty("line.separator");
    System.err.println(sep + ">>> " + prefix + ": " + e.getMessage() + sep);
  }

  // Test driver
  public static void main(String[] args) {
    Controller ctrl = new Controller("java org.ainspector.util.AInspector <options>", args);

    Option[] list = ctrl.cmdLine.getOptions();
    for (Option o : list) {
      System.out.println(o.getLongOpt() + ": " + o.getValue());
    }
  }

  // CommandLine instance
  private CommandLine cmdLine = null;

  // Options container
  private Options options = null;

  // Option instances
  private Option scriptsFile = new Option("s", "scripts", true, "Required: text file with names of script files");
  private Option urlsFile = new Option("u", "urls", true, "Required: text file with URLs to inspect");
  private Option outputDirectory = new Option("o", "output", true, "Required: directory for results files");
  private Option debug = new Option("D", "debug", false, "Optional: turn on debugging output");
  private Option verbose = new Option("V", "verbose", false, "Optional: turn on HtmlUnit logging output");

  // Error message constants
  private final String PARSE_ERROR = "Error parsing arguments";

  // Help text constants
  private final String SYNTAX;
}
