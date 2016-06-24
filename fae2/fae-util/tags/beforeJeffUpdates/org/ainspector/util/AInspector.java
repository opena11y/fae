package org.ainspector.util;

import java.io.*;
import java.net.URL;
import java.util.*;

import com.gargoylesoftware.htmlunit.*;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import org.apache.commons.logging.LogFactory;

import org.ainspector.util.Controller;
import org.ainspector.util.FileUtil;

/**
 * AInspector
 *
 * Initialize and store the following:
 *   1. Either a single URL or a list of URLs (a list takes precedence)
 *   2. Concatenated scripts
 *   3. Name of directory to store results
 *   4. Reference to WebClient object
 *
 * Provide the following functionality:
 *   1. Iteratively call getPage for each URL to get its DOM object
 *   2. Execute JavaScript on each DOM object and get ScriptResult object
 *   3. Save the results From each ScriptResult object in specified directory
 */

class AInspector {

  public static void main (String args[]) {
    long startTime, endTime;
    startTime = System.currentTimeMillis();

    // Consume the command line arguments
    Controller ctrl = new Controller("java org.ainspector.util.AInspector <options>", args);
    debug                    = ctrl.DEBUG;
    verbose                  = ctrl.VERBOSE;
    final String scriptsFile = ctrl.SCRIPTS_FILE;
    final String outputDir   = ctrl.OUTPUT_DIRECTORY;
    final String inputFile   = ctrl.INPUT_FILE;
    final String singleUrl   = ctrl.SINGLE_URL;

    // Check that outputDirectory does not already exist and can be created.
    // If both conditions are not met, exit with error message.
    try {
      if (!initOutputDirectory(outputDir)) {
        System.err.println(configError);
        System.err.println("Error: Directory " + outputDir + " already exists or could not be created!");
        System.err.println(exiting);
        System.exit(1);
      }
    }
    catch (Exception e) {
      displayException(e);
      System.err.println(exiting);
      System.exit(1);
    }

    // Turn off all logging unless verbose option specified
    if (!verbose)
      LogFactory.getFactory().setAttribute("org.apache.commons.logging.Log",
                                           "org.apache.commons.logging.impl.NoOpLog");
    initWebClient();

    if (debug) {
      System.out.println("scriptsFile: " + scriptsFile);
      System.out.println("outputDirectory: " + outputDirectory);
      if (inputFile != null)
        System.out.println("inputFile: " + inputFile);
      else
        System.out.println("singleUrl: " + singleUrl);
      System.out.println("browser: " + webClient.getBrowserVersion().getNickname());
    }

    try {
      // Get the JavaScript to execute
      script = FileUtil.concatenateFiles(scriptsFile, debug);
      if (debug) System.out.println(script);

      // Process one or more URLs
      if (inputFile != null) {
        urls = FileUtil.getUrlList(inputFile);

        for (URL url : urls) {
          processUrl(url);
        }
      }
      else {
        processUrl(new URL(singleUrl));
      }
    }
    catch(Exception e) {
      displayException(e);
      System.err.println(exiting);
    }
    finally {
      webClient.closeAllWindows();
      endTime = System.currentTimeMillis();
      displaySummary(inputFile, singleUrl, endTime - startTime);
    }
  }

  private static boolean initOutputDirectory(String dirName) throws IOException {
    File dir = new File(dirName);
    if (dir.exists()) return false;

    // Create the output directory only when NOT in debug mode
    if (debug) return true;
    if (!dir.mkdir()) return false;
    outputDirectory = dir.getAbsolutePath();
    return true;
  }

  private static void initWebClient() {
    // Set the default browser version
    BrowserVersion.setDefault(BrowserVersion.FIREFOX_3_6);

    // Instantiate a WebClient object with default browser version
    webClient = new WebClient();

    // Suppress CSS, HTML Parser and Incorrectness warnings and errors
    if (!verbose) {
      webClient.setCssErrorHandler(new SilentCssErrorHandler());
      webClient.setHTMLParserListener(null);
      webClient.setIncorrectnessListener(new NoOpIncListener());
    }

    // Disallow exceptions of these types when getPage() is called
    webClient.setThrowExceptionOnFailingStatusCode(false);
    webClient.setRefreshHandler(new RefreshHandler() {
      public void handleRefresh(Page page, URL url, int arg) throws IOException {}
    });
  }

  public static void processUrl(URL url) throws Exception {
    long startTime, endTime;

    // Get the page to analyze
    webClient.setThrowExceptionOnScriptError(false);
    System.out.println(newline + "Processing URL: " + url);
    System.out.print("Retrieving DOM... ");
    startTime = System.currentTimeMillis();
    HtmlPage page = webClient.getPage(url);
    endTime = System.currentTimeMillis();
    displayTiming(startTime, endTime);

    // Run the concatenated JavaScript scripts against the page
    webClient.setThrowExceptionOnScriptError(true);
    System.out.print("Running evaluation scripts... ");
    startTime = System.currentTimeMillis();
    ScriptResult result = page.executeJavaScript(script);
    endTime = System.currentTimeMillis();
    displayTiming(startTime, endTime);

    // Increment number of URLs processed
    urlCount++;

    // Display or save the JavaScript result
    if (debug)
      displayResult(result, debug);
    else
      saveResult(result);
  }

  public static void saveResult(ScriptResult result) throws IOException {
    String num = urlCount < 10 ? "00" + urlCount : urlCount < 100 ? "0" + urlCount : "" + urlCount;
    String basename = filePrefix + num + fileSuffix;
    System.out.println("Saving results file: " + basename);
    String filename = outputDirectory + fileSep + basename;
    FileUtil.writeStringToFile(result.getJavaScriptResult().toString(), filename);
  }

  public static void displayResult(ScriptResult result, boolean delimiterFlag) {
    if (delimiterFlag) System.out.println(newline + beginResults);
    System.out.println(result.getJavaScriptResult());
    if (delimiterFlag) System.out.println(endResults);
  }

  public static void displaySummary(String inputFile, String singleUrl, long elapsedTime) {
    String fdesc = urlCount == 1 ? "file" : "files";

    System.out.println();
    if (inputFile != null) {
      System.out.print("Summary: Processed " + urlCount + " of " + urls.size()
                       + " URLs from " + inputFile);
    }
    else {
      System.out.print("Summary: Processed single URL " + singleUrl);
    }
    System.out.println(" in " + elapsedTime + " msec.");

    if (!debug)
      System.out.println("and saved results " + fdesc + " in " + outputDirectory);
  }

  public static void displayTiming(long startTime, long endTime) {
    long elapsedTime = endTime - startTime;
    System.out.println(elapsedTime + " msec.");
  }

  public static void displayException(Exception e) {
    System.err.println(exceptionCaught);
    System.err.println(e);
  }

  public static class NoOpIncListener implements IncorrectnessListener
  {
    public void notify(String message, Object origin) {}
  }

  // class variables needed for iterating through list of URLs
  static WebClient webClient;
  static ArrayList<URL> urls;
  static String script;

  static boolean debug;
  static boolean verbose;
  static String outputDirectory;
  static int urlCount = 0;

  // miscellaneous class constants
  static final String beginResults    = "************ BEGIN JAVASCRIPT RESULTS ************";
  static final String endResults      = "************ END JAVASCRIPT RESULTS ************";
  static final String exceptionCaught = "************ EXCEPTION CAUGHT IN AINSPECTOR-UTIL MAIN ************";
  static final String configError     = "************ CONFIGURATION ERROR IN AINSPECTOR-UTIL MAIN ************";
  static final String exiting         = "************ AINSPECTOR-UTIL IS EXITING ************";
  static final String filePrefix      = "aiutil-";
  static final String fileSuffix      = ".txt";
  static final String fileSep         = System.getProperty("file.separator");
  static final String newline         = System.getProperty("line.separator");
}
