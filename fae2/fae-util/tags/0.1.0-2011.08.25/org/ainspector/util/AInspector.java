package org.ainspector.util;

import java.io.IOException;
import java.net.URL;

import com.gargoylesoftware.htmlunit.*;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import org.apache.commons.logging.LogFactory;

import org.ainspector.util.Controller;
import org.ainspector.util.MultiFileConcatenator;

class AInspector {

  public static void main (String args[]) {

    // Consume the command line arguments
    Controller ctrl = new Controller("java org.ainspector.util.AInspector <options>", args);
    final boolean debug    = ctrl.DEBUG;
    final String  filename = ctrl.FILENAME;
    final String  url      = ctrl.URL;
    final boolean verbose  = ctrl.VERBOSE;

    // Turn off all logging unless verbose option specified
    if (!verbose)
      LogFactory.getFactory().setAttribute("org.apache.commons.logging.Log",
                                           "org.apache.commons.logging.impl.NoOpLog");
    // Set the default browser version
    BrowserVersion.setDefault(BrowserVersion.FIREFOX_3_6);

    // Instantiate a WebClient object with default browser version
    final WebClient webClient = new WebClient();

    // Suppress CSS, HTML Parser and Incorrectness warnings and errors
    if (!verbose) {
      webClient.setCssErrorHandler(new SilentCssErrorHandler());
      webClient.setHTMLParserListener(null);
      webClient.setIncorrectnessListener(new NoOpIncListener());
    }

    // Disallow exceptions of these types when getPage() is called
    webClient.setThrowExceptionOnFailingStatusCode(false);
    webClient.setThrowExceptionOnScriptError(false);
    webClient.setRefreshHandler(new RefreshHandler() {
      public void handleRefresh(Page page, URL url, int arg) throws IOException {}
    });

    if (debug) {
      System.out.println("filename: " + filename);
      System.out.println("url: " + url);
      System.out.println("browser: " + webClient.getBrowserVersion().getNickname());
    }

    try {
      // Get the JavaScript to execute
      MultiFileConcatenator mfc = new MultiFileConcatenator(filename, debug);
      mfc.processInputFile();
      String script = mfc.getContentsAllFiles();

      if (debug) System.out.println(script);

      // Get the page to analyze
      HtmlPage page = webClient.getPage(url);

      // Run the concatenated JavaScript scripts against the page
      webClient.setThrowExceptionOnScriptError(true);
      ScriptResult result = page.executeJavaScript(script);

      // Display the JavaScript result
      displayResult(result, debug);
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

  static final String beginResults    = "************ BEGIN JAVASCRIPT RESULTS ************";
  static final String endResults      = "************ END JAVASCRIPT RESULTS ************";
  static final String exceptionCaught = "************ EXCEPTION CAUGHT IN AINSPECTOR-UTIL MAIN ************";
  static final String exiting         = "************ AINSPECTOR-UTIL IS EXITING ************";
  static final String sep             = System.getProperty("line.separator");
}
