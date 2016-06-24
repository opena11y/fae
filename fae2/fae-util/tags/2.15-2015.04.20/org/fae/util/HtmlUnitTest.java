package org.fae.util;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

import org.apache.log4j.Category;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Level;
import org.apache.log4j.PatternLayout;

import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class HtmlUnitTest {

  /**
   * @param args
   */
  public static void main(String[] args) {
    try {
      Category logger = Category.getRoot();
      logger.setLevel(Level.DEBUG);
      //logger.addAppender(new ConsoleAppender(new SimpleLayout()));
      logger.addAppender(new ConsoleAppender(new PatternLayout("|%c|%5p| %m%n")));
      //logger = Category.getInstance(WebClient.class);
      //logger.setLevel(Level.DEBUG);
      //logger = Category.getInstance("com.gargoylesoftware.htmlunit");
      //logger.setLevel(Level.DEBUG);
      //logger = Category.getInstance("com.gargoylesoftware.htmlunit.javascript.configuration.JavaScriptConfiguration");
      //logger.setLevel(Level.DEBUG);

      FaeUtil faeUtil = new FaeUtil();
      faeUtil.DEBUG = true;

      WebClient webClient = new WebClient(faeUtil.BROWSER_VERSION);
      faeUtil.initWebClient(webClient);

      webClient.getOptions().setPrintContentOnFailingStatusCode(false);
      webClient.getOptions().setThrowExceptionOnScriptError(false);
      webClient.getOptions().setUseInsecureSSL(true); // JSH added
      //URL requestUrl = new URL("http://msn.com/");
      URL requestUrl = new URL("https://nessie.uihr.uillinois.edu/cf/sitelogin.cfm");
      HtmlPage page = webClient.getPage(requestUrl);
      faeUtil.debug(" &&&&& " + page.getWebResponse());
      faeUtil.debug(" &&&&& " + page.getWebResponse().getStatusCode());
      faeUtil.debug(" &&&&& " + page.getWebResponse().getStatusMessage());
      faeUtil.debug(" &&&&& " + page.getWebResponse().getWebRequest().getUrl());
    }
    catch (MalformedURLException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    catch (FailingHttpStatusCodeException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

}
