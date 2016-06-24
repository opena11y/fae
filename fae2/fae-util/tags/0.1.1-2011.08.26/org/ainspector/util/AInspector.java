package org.ainspector.util;

import java.io.IOException;
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
 *   1. List of URL objects
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

    // Consume the command line arguments
    Controller ctrl = new Controller("java org.ainspector.util.AInspector <options>", args);
    debug                     = ctrl.DEBUG;
    verbose                   = ctrl.VERBOSE;
    outputDirectory           = ctrl.OUTPUT_DIRECTORY;
    final String  urlsFile    = ctrl.URLS_FILE;
    final String  scriptsFile = ctrl.SCRIPTS_FILE;

    // Turn off all logging unless verbose option specified
    if (!verbose)
      LogFactory.getFactory().setAttribute("org.apache.commons.logging.Log",
                                           "org.apache.commons.logging.impl.NoOpLog");
    initWebClient();

    if (debug) {
      System.out.println("urlsFile: " + urlsFile);
      System.out.println("scriptsFile: " + scriptsFile);
      System.out.println("outputDirectory: " + outputDirectory);
      System.out.println("browser: " + webClient.getBrowserVersion().getNickname());
    }

    try {
      // Get the list of URLs
      urls = FileUtil.getUrlList(urlsFile);

      // Get the JavaScript to execute
      script = FileUtil.concatenateFiles(scriptsFile, debug);
      if (debug) System.out.println(script);

      // Process each URL with HTMLUnit
      for (URL url : urls) {
        processUrl(url);
      }
    }
    catch(Exception e) {
      displayException(e);
      System.err.println(exiting);
      System.exit(1);
    }
    finally {
      webClient.closeAllWindows();
    }
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
    // Get the page to analyze
    webClient.setThrowExceptionOnScriptError(false);
    HtmlPage page = webClient.getPage(url);

    // Run the concatenated JavaScript scripts against the page
    webClient.setThrowExceptionOnScriptError(true);
    ScriptResult result = page.executeJavaScript(script);

    // Display the JavaScript result
    displayResult(result, debug);
  }

  public static void displayResult(ScriptResult result, boolean delimiterFlag) {
    if (delimiterFlag) System.out.println(beginResults);
    System.out.println(result.getJavaScriptResult());
    if (delimiterFlag) System.out.println(endResults);
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

  // miscellaneous class constants
  static final String beginResults    = "************ BEGIN JAVASCRIPT RESULTS ************";
  static final String endResults      = "************ END JAVASCRIPT RESULTS ************";
  static final String exceptionCaught = "************ EXCEPTION CAUGHT IN AINSPECTOR-UTIL MAIN ************";
  static final String exiting         = "************ AINSPECTOR-UTIL IS EXITING ************";
  static final String sep             = System.getProperty("line.separator");
}
