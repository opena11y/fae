package org.fae.util;

import com.gargoylesoftware.htmlunit.ScriptPreProcessor;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

/**
 * Class that is called by HtmlUnit before downloading/evaluating a Javascript file.
 * This was added to make it possible to ignore certain files that would cause HtmlUnit to crash.
 */
public class ScriptPreprocessor implements ScriptPreProcessor {

  private FaeUtil m_faeUtil;

  public ScriptPreprocessor(FaeUtil faeUtil) {
    m_faeUtil = faeUtil;
  }

  @Override
  public String preProcess(HtmlPage htmlPage, String sourceCode, String sourceName, int lineNumber, HtmlElement htmlElement) {
    //System.out.println("in my ScriptPreprocessor, sourceName=>" + sourceName);
    for (String url : m_faeUtil.m_javascriptUrlsToNotProcess) {
      if (url.equals(sourceName)) {
        System.err.println(" ***** SKIPPING JAVASCRIPT FROM: " + sourceName);
        return new String();
      }
    }
    //    if (sourceName.equals("http://www.edb.utexas.edu/education/assets/js/coe_tpl11/jquery.tools.min.js")) {
    //      System.err.println(" ***** SKIPPING JAVASCRIPT FROM: " + sourceName);
    //      return new String();
    //    }
    return sourceCode;
  }
}
