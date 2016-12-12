package org.fae.util;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;

/**
 * Read command-line arguments and store values as constants. These values
 * are used to control the execution of methods in the collaborative class.
 */
public class Controller {

  // Exported constants
  public boolean DEBUG = false;
  //public boolean SEARCH_SUBDOMAINS = false;
  public boolean TEST_MODE = false;
  public boolean VERBOSE = false;
  public String JAVA_SCRIPT = "true";
  public String EXPORT_OPTION = "false";
  public String BROWSER_VERSION = "firefox";
  public String CONFIG_FILE;
  public String DEPTH = "1";
  public String MAX_PAGES = "0";
  public String PATH;
  public String INPUT_FILE;
  public String OUTPUT_DIRECTORY;
  public String SCRIPTS_FILE;
  public String SINGLE_URL;
  public String WAIT;
  public String GROUPS = "7";

  public String EXCLUDE_DOMAINS;
  public String INCLUDE_DOMAINS;
  public String SPAN_DOMAINS;

  //public String EVALUATION_LEVELS;
  public String RULESET;

  public String AUTHORIZATION;
 
  public Controller(String syntax) {
    SYNTAX = syntax;

    initOptions();
  }

  public void dump(String msg) {
    System.out.println(" ----------------------------------------------------- ");
    System.out.println(msg);
    System.out.println("\t" + browserVersion.getLongOpt() + "=> " + BROWSER_VERSION);
    System.out.println("\t" + configFile.getLongOpt() + "=> " + CONFIG_FILE);
    System.out.println("\t" + debug.getLongOpt() + "=> " + DEBUG);
    System.out.println("\t" + depth.getLongOpt() + "=> " + DEPTH);
    System.out.println("\t" + maxPages.getLongOpt() + "=> " + MAX_PAGES);
    System.out.println("\t" + path.getLongOpt() + "=> " + PATH);
    System.out.println("\t" + groups.getLongOpt() + "=> " + GROUPS);
    System.out.println("\t" + inputFile.getLongOpt() + "=> " + INPUT_FILE);
    System.out.println("\t" + outputDirectory.getLongOpt() + "=> " + OUTPUT_DIRECTORY);
    System.out.println("\t" + scripts.getLongOpt() + "=> " + SCRIPTS_FILE);
    //System.out.println("\tSEARCH_SUBDOMAINS=>" + SEARCH_SUBDOMAINS);
    System.out.println("\t" + singleUrl.getLongOpt() + "=> " + SINGLE_URL);
    System.out.println("\t" + testMode.getLongOpt() + "=> " + TEST_MODE);
    System.out.println("\t" + verbose.getLongOpt() + "=> " + VERBOSE);
    System.out.println("\t" + wait.getLongOpt() + "=> " + WAIT);

    System.out.println("\t" + excludeDomains.getLongOpt() + "=> " + EXCLUDE_DOMAINS);
    System.out.println("\t" + includeDomains.getLongOpt() + "=> " + INCLUDE_DOMAINS);
    System.out.println("\t" + spanDomains.getLongOpt() + "=> " + SPAN_DOMAINS);

    //System.out.println("\t" + evaluationLevels.getLongOpt() + "=> " + EVALUATION_LEVELS);
    System.out.println("\t" + ruleset.getLongOpt() + "=> " + RULESET);

    System.out.println("\t" + authorization.getLongOpt() + "=> " + AUTHORIZATION);
    System.out.println("\t" + javaScript.getLongOpt() + "=> " + JAVA_SCRIPT);
    System.out.println("\t" + exportOption.getLongOpt() + "=> " + EXPORT_OPTION);
    System.out.println(" ----------------------------------------------------- ");
  }

  public void readArgs(String[] args) {
    CommandLineParser parser = new PosixParser();
    try {
      m_cmdLine = parser.parse(m_options, args);
    }
    catch (ParseException e) {
      //e.printStackTrace();
      printException(PARSE_ERROR, e);
      printUsage();
      System.exit(1);
    }

    // look for config file
    if (m_cmdLine.hasOption(configFile.getOpt()))
      CONFIG_FILE = m_cmdLine.getOptionValue(configFile.getOpt());

    // Check for mandatory args
    if (m_cmdLine.hasOption(inputFile.getOpt()))
      INPUT_FILE = m_cmdLine.getOptionValue(inputFile.getOpt());
    if (m_cmdLine.hasOption(singleUrl.getOpt()))
      SINGLE_URL = m_cmdLine.getOptionValue(singleUrl.getOpt());
    //if (SINGLE_URL == null && m_cmdLine.getArgs().length > 0)
    //SINGLE_URL = m_cmdLine.getArgs()[0];
    if (m_cmdLine.hasOption(outputDirectory.getOpt()))
      OUTPUT_DIRECTORY = m_cmdLine.getOptionValue(outputDirectory.getOpt());
    if (m_cmdLine.hasOption(scripts.getOpt()))
      SCRIPTS_FILE = m_cmdLine.getOptionValue(scripts.getOpt());

    // Initialize optional args
    DEBUG = m_cmdLine.hasOption(debug.getOpt());
    TEST_MODE = m_cmdLine.hasOption(testMode.getOpt());
    VERBOSE = m_cmdLine.hasOption(verbose.getOpt());
    
    if (m_cmdLine.hasOption(javaScript.getOpt()))
    	JAVA_SCRIPT = m_cmdLine.getOptionValue(javaScript.getOpt());   
    if (m_cmdLine.hasOption(exportOption.getOpt()))
    	EXPORT_OPTION = m_cmdLine.getOptionValue(exportOption.getOpt());
    if (m_cmdLine.hasOption(browserVersion.getOpt()))
      BROWSER_VERSION = m_cmdLine.getOptionValue(browserVersion.getOpt());
    if (m_cmdLine.hasOption(depth.getOpt()))
      DEPTH = m_cmdLine.getOptionValue(depth.getOpt());
    if (m_cmdLine.hasOption(maxPages.getOpt()))
        MAX_PAGES = m_cmdLine.getOptionValue(maxPages.getOpt());
    if (m_cmdLine.hasOption(path.getOpt()))
        PATH = m_cmdLine.getOptionValue(path.getOpt());
    if (m_cmdLine.hasOption(groups.getOpt()))
      GROUPS = m_cmdLine.getOptionValue(groups.getOpt());
    if (m_cmdLine.hasOption(wait.getOpt()))
      WAIT = m_cmdLine.getOptionValue(wait.getOpt());

    //if (m_cmdLine.hasOption(searchSubDomains.getOpt()))
    //SEARCH_SUBDOMAINS = m_cmdLine.hasOption(searchSubDomains.getOpt());

    if (m_cmdLine.hasOption(excludeDomains.getOpt()))
      EXCLUDE_DOMAINS = m_cmdLine.getOptionValue(excludeDomains.getOpt());
    if (m_cmdLine.hasOption(includeDomains.getOpt()))
      INCLUDE_DOMAINS = m_cmdLine.getOptionValue(includeDomains.getOpt());
    if (m_cmdLine.hasOption(spanDomains.getOpt())) {
      SPAN_DOMAINS = m_cmdLine.getOptionValue(spanDomains.getOpt());
      /*if (SPAN_DOMAINS.equals("star"))
        SPAN_DOMAINS = "*";*/
    }

    /*if (m_cmdLine.hasOption(evaluationLevels.getOpt()))
      EVALUATION_LEVELS = m_cmdLine.getOptionValue(evaluationLevels.getOpt());*/
    if (m_cmdLine.hasOption(ruleset.getOpt()))
      RULESET = m_cmdLine.getOptionValue(ruleset.getOpt());

    if (m_cmdLine.hasOption(authorization.getOpt()))
      AUTHORIZATION = m_cmdLine.getOptionValue(authorization.getOpt());
           
  }

  public void validateInput() {
    dump("settings");

    boolean error = false;

    if (SCRIPTS_FILE == null || SCRIPTS_FILE.length() == 0) {
      System.err.println("missing " + scripts.getLongOpt() + " argument");
      error = true;
    }

    if (OUTPUT_DIRECTORY == null || OUTPUT_DIRECTORY.length() == 0) {
      System.err.println("missing " + outputDirectory.getLongOpt() + " argument");
      error = true;
    }

    // Must have specified one or the other...
    if ((INPUT_FILE == null || INPUT_FILE.length() == 0) && (SINGLE_URL == null || SINGLE_URL.length() == 0)) {
      System.err.println("missing " + singleUrl.getLongOpt() + " or " + inputFile.getLongOpt() + " argument");
      error = true;
    }

    // Can't have both
    if (INPUT_FILE != null && SINGLE_URL != null) {
      System.err.println("Cannot specify both starting URL and multiple URLs file.");
      error = true;
    }

    if (INPUT_FILE != null && (!DEPTH.equals("1") || EXCLUDE_DOMAINS != null || INCLUDE_DOMAINS != null || SPAN_DOMAINS != null)) {
      System.err.println("Cannot specify <" + depth.getLongOpt() + " " + excludeDomains.getLongOpt() + " " + includeDomains.getLongOpt() + " " + spanDomains.getLongOpt() + "> with " + inputFile.getLongOpt() + ".");
      error = true;
    }
    
    if (MAX_PAGES.length() != 0 && Integer.parseInt(MAX_PAGES) < 0) {
        System.err.println("Invalid " + maxPages.getLongOpt() + ": " + MAX_PAGES);
        error = true;
    }

    if (!BROWSER_VERSION.equalsIgnoreCase("chrome") && !BROWSER_VERSION.equalsIgnoreCase("firefox") && !BROWSER_VERSION.equalsIgnoreCase("ie")) {
      System.err.println("Unknown " + browserVersion.getLongOpt() + ": " + BROWSER_VERSION);
      error = true;
    }
    
    if (!JAVA_SCRIPT.equalsIgnoreCase("true") && !JAVA_SCRIPT.equalsIgnoreCase("false")) {
      System.err.println("Unknown " + javaScript.getLongOpt() + ": " + JAVA_SCRIPT);
      error = true;
    }
    
    if (!EXPORT_OPTION.equalsIgnoreCase("true") && !EXPORT_OPTION.equalsIgnoreCase("false")) {
        System.err.println("Unknown " + exportOption.getLongOpt() + ": " + EXPORT_OPTION);
        error = true;
    }
    
    if (error) {
      printUsage();
      System.exit(1);
    }
  }

  /**
   * Initialize and populate the Options container
   */
  private void initOptions() {
    m_options = new Options();

    m_options.addOption(browserVersion);
    m_options.addOption(configFile);
    m_options.addOption(debug);
    m_options.addOption(depth);
    m_options.addOption(maxPages);
    m_options.addOption(path);
    m_options.addOption(groups);
    m_options.addOption(inputFile);
    m_options.addOption(outputDirectory);
    m_options.addOption(scripts);
    //m_options.addOption(searchSubDomains);
    m_options.addOption(singleUrl);
    m_options.addOption(testMode);
    m_options.addOption(verbose);
    m_options.addOption(wait);

    m_options.addOption(excludeDomains);
    m_options.addOption(includeDomains);
    m_options.addOption(spanDomains);

    //m_options.addOption(evaluationLevels);
    m_options.addOption(ruleset);

    m_options.addOption(authorization);
    m_options.addOption(javaScript);
    m_options.addOption(exportOption);
  }

  /**
   * Print the help text.
   */
  public void printUsage() {
    HelpFormatter formatter = new HelpFormatter();
    formatter.setWidth(250);
    formatter.printHelp(SYNTAX, m_options);
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
    Controller ctrl = new Controller("java org.ainspector.util.FaeUtil <options> <url - Required (unless -u, --urls is specified): starting URL>");
    ctrl.readArgs(args);
    ctrl.printUsage();

    System.out.println("------------------------------------");
    for (String arg : args)
      System.out.println(arg);

    System.out.println("------------------------------------");
    Option[] list = ctrl.m_cmdLine.getOptions();
    for (Option o : list) {
      System.out.println(o.getLongOpt() + ": " + o.getValue());
    }

    ctrl.validateInput();

    ctrl.dump("main");
  }

  // CommandLine instance
  public CommandLine m_cmdLine = null;

  // Options container
  private Options m_options = null;

  // Option instances
  public Option browserVersion = new Option("browserVersion", "browserVersion", true, "Optional: browserVersion to use; chrome, firefox (default), ie");
  public Option configFile = new Option("c", "config", true, "Optional: filename of configuration parameters");
  public Option debug = new Option("D", "debug", false, "Optional: turn on debugging output");
  public Option depth = new Option("d", "depth", true, "Optional: maximium depth to traverse (number: 1 | 2 | 3, default = 1, which means no traversing)");
  public Option maxPages = new Option("p", "maxPages", true, "Optional: maximium number of pages to process (number, greater than or equal to 1: default = all pages)");
  public Option path = new Option("h", "path", true, "Optional: url path (string, url path: default = empty)");
  public Option groups = new Option("g", "groups", true, "Optional: number indicating which rules will be evaluated based on rule group information (default = 7)");
  public Option inputFile = new Option("m", "multipleUrls", true, "Required (unless -u, --url is specified): filename containing URLs to evaluate");
  public Option outputDirectory = new Option("o", "outputDirectory", true, "Required: directory for results files");
  public Option scripts = new Option("scripts", "scripts", true, "Required: file with names of script files");
  //public Option searchSubDomains = new Option("searchSubDomains", "searchSubDomains", false, "Optional: search subDomains");
  public Option singleUrl = new Option("u", "url", true, "Required (unless -m, --multipleUrls is specified): starting URL");
  public Option testMode = new Option("testMode", "testMode", false, "Optional: testmode; will not find events or evaluate scripts");
  public Option verbose = new Option("V", "verbose", false, "Optional: turn on HtmlUnit logging output");
  public Option wait = new Option("w", "wait", true, "Optional: maximium time in milliseconds to wait when processing a page, default = 30000 msec. (30 seconds)");

  public Option excludeDomains = new Option("e", "excludeDomains", true, "Optional: do not traverse these domains (comma-separated list; valid only if -s is specified; each domain must be a subdomain of an entry in spanDomains)");
  public Option includeDomains = new Option("i", "includeDomains", true, "Optional: traverse these domains (comma-separated list) in addition to the domain specified by the URL");
  public Option spanDomains = new Option("s", "spanDomains", true, "Optional: traverse the subdomains of these domains (comma-separated list), in addition to the domain specified by the URL");

  //public Option evaluationLevels = new Option("l", "evaluationLevels", true, "Optional: Rule levels to include in the evaluation ('A' | 'A_AA', default='A_AA')");
  public Option ruleset = new Option("r", "ruleset", true, "Optional: OAA ruleset ID ('ARIA_TRANS' | 'ARIA_STRICT', default = 'ARIA_TRANS')");

  public Option authorization = new Option("a", "authorization", true, "Optional: filename of authorization information");
  public Option javaScript = new Option("j", "javaScript", true, "Optional: boolean value to enable (true, default) or disable (false) HtmlUnit java script");
  public Option exportOption = new Option("xo", "exportOption", true, "Optional: boolean value to enable (true) or disable (false, default) export option");
  
  // Error message constants
  private final String PARSE_ERROR = "Error parsing arguments";

  // Help text constants
  private final String SYNTAX;
}
