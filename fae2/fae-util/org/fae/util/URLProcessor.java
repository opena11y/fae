package org.fae.util;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.StringTokenizer;
import java.util.Vector;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;

import org.eclipse.jetty.http.HttpStatus;
import org.w3c.dom.Document;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.ScriptResult;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.DomElement;
import com.gargoylesoftware.htmlunit.html.HtmlAnchor;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlForm;
import com.gargoylesoftware.htmlunit.html.HtmlImage;
import com.gargoylesoftware.htmlunit.html.HtmlPage;


// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
/**
 * This is the main class for processing/traversing a URL.
 * 
 * @author jheckel
 */
public class URLProcessor {

	public static boolean FIND_EVENTS = true;
	public static boolean EVAL_SCRIPT = true;
	public static boolean FIND_LINKS = true;

	static boolean m_processingURL = false;

	private Processor m_processor;
	private int pageCount = 0;

	// need a static WebClient so don't have to keep logging into a page
	static BrowserVersion BROWSER_VERSION = FaeUtil.BROWSER_VERSION;
	static WebClient webClient = new WebClient(BROWSER_VERSION);
	private String m_loggedInURL = null;
	private Vector<String> m_alreadyProcessedAuthorizationUrls = new Vector<String>();
	private Vector<String> maxPageUrls = new Vector<String>();
	public static Vector<String> m_loginSuccessURLs = new Vector<String>();
	public static Vector<String> m_loginFailURLs = new Vector<String>();
	public static String excludedURLParent;
	public static boolean more_urls;

	// ==========================================================================
	// ==========================================================================
	/**
	 * Will process/read the given URL. DOES TRAVERSE HERE! Creates an instance
	 * of URLProcessor class and then calls the 'process' method. When complete
	 * will look at links (HREF) found and normalize the link into a true URL
	 * and then traverse it, increasing 'depth'.
	 * 
	 * @throws MalformedURLException
	 */
	public void traverseURL(FaeUtil faeUtil, String urlFrom, String url,
			int depth, String baseURL) throws MalformedURLException, Exception {
		// check if should process/traverse given url
		// if (!traverseIt(depth, FaeUtil.m_urlCount, 0, url))
		// return;
		// // already read this URL?
		// if (FaeUtil.m_urlsRead.contains(url))
		// return;
		//
		// // past depth to search?
		// if (depth > FaeUtil.MAX_DEPTH)
		// return;
		//
		// // still on the proper domain or host?
		// if (FaeUtil.m_host != null && FaeUtil.m_host.length() > 0) {
		// if (FaeUtil.m_traverseSubDomains) {
		// if (!url.contains(FaeUtil.m_host)) {
		// return;
		// }
		// }
		// else {
		// if (!url.startsWith(FaeUtil.m_host)) {
		// return;
		// }
		// }
		// }
		int maxPage = 0;
		if (faeUtil.m_ctrl.MAX_PAGES.length() > 0) {
			maxPage = Integer.parseInt(faeUtil.m_ctrl.MAX_PAGES);
		}
		if (pageCount < maxPage && !maxPageUrls.contains(url)) {
			if (faeUtil.m_ctrl.PATH != null
					&& !faeUtil.m_ctrl.PATH.toString().isEmpty()) {
				if (pageCount > 0
						&& url.length() > urlFrom.length()
						&& urlFrom.substring(0, urlFrom.length() - 1).equals(
								url.substring(0, urlFrom.length() - 1))) {
					subTraverseURL(faeUtil, urlFrom, url, depth, baseURL);
				} else {
					if (pageCount == 0) {
						subTraverseURL(faeUtil, urlFrom, url, depth, baseURL);
					}
				}
			} else {
				subTraverseURL(faeUtil, urlFrom, url, depth, baseURL);
			}
		} else if (maxPage == 0) {
			subTraverseURL(faeUtil, urlFrom, url, depth, baseURL);
		} else if (pageCount == maxPage) {
			more_urls = true;
		}
	}

	public void subTraverseURL(FaeUtil faeUtil, String urlFrom, String url,
			int depth, String baseURL) throws MalformedURLException, Exception {
		faeUtil.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
		faeUtil.debug(faeUtil.m_urlCount + ": TRAVERSING " + url + " (" + depth
				+ ":" + baseURL + ")");

		for (int x = 1; x < depth; ++x)
			faeUtil.m_treeRepresentation.append("\t");
		faeUtil.m_treeRepresentation.append(url + "\n");
		// FaeUtil.m_treeRepresentation.append(url + " (" + FaeUtil.m_urlCount +
		// ")\n");

		if (authorizationUrlMatch(faeUtil, 0, 0, url))
			traverseURL(faeUtil, urlFrom, url, depth, baseURL);

		// if (pageCount > 0 && baseURL.length() > urlFrom.length() &&
		// urlFrom.substring(0, urlFrom.length() -
		// 1).equals(baseURL.substring(0, urlFrom.length() - 1))){

		URLProcessor processor = new URLProcessor();
		// process the URL - read page, find events, evaluate script, find links
		processor.process(faeUtil, urlFrom, url);
		pageCount++;
		maxPageUrls.add(url);
		int urlNum = processor.getProcessor().getUrlNum();

		// if going to go past DEPTH then don't bother wasting cpu cycles
		if ((depth + 1) <= faeUtil.DEPTH) {
			// get list of links found
			Vector<String> links = processor.getProcessor().getLinksFound();
			faeUtil.debug(urlNum + ": depth:" + depth + ": number links => "
					+ links.size());
			int cnt = 1;
			for (String link : links) {

				// transform the found link into a true URL and get newBase for
				// URL
				String newBase = baseURL;
				if (faeUtil.m_ctrl.PATH != null
						&& !faeUtil.m_ctrl.PATH.toString().isEmpty()) {
					String path = faeUtil.m_ctrl.PATH;
					if (path.startsWith("/")) {
						path = path.substring(1);
					}
					if (path.endsWith("/")) {
						path = path.substring(0, path.length() - 1);
					}
					if (link.startsWith("/")) {
						link = link.substring(1);
					}
					if (link.endsWith("/")) {
						link = link.substring(0, link.length() - 1);
					}
					//TODO need to add starts with path logic, need to discuss with Jon first
					
					if (link.startsWith(baseURL + path)) {
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found " + link);
						newBase = link;
					} else if (!link.startsWith("http") && !link.contains("www")) {
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found1 " + link);
						//if (link.startsWith("/")) {
						if(!link.equals(path)){
							if (baseURL.endsWith("/")){
								if (link.contains(path)) {
									link = baseURL.toString() + link;
								}else {
									link = baseURL.toString() + path + "/" + link;
								}
							} else {
								if (link.contains(path)) {
									link = baseURL.toString() + link;
								}else {
									link = baseURL.toString() + "/" + path + "/" + link;
								}								
							}
						}
//						} else {
//							if (baseURL.endsWith("/")) {
//								if (link.contains(faeUtil.m_ctrl.PATH)) {
//									link = baseURL.toString() + link;
//								}else {
//									link = baseURL.toString() + faeUtil.m_ctrl.PATH + "/" + link;
//								}
//							} else {								
//								if (link.contains(faeUtil.m_ctrl.PATH)) {
//									link = baseURL.toString() + "/" + link;
//								}else {
//									link = baseURL.toString() + "/" + faeUtil.m_ctrl.PATH + "/" + link;
//								}
//							}
//						}
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found2 " + link);
					}
				} else {
					if (link.startsWith("http")) {
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found " + link);
						newBase = link;
					} else {
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found1 " + link);
						if (link.startsWith("/")) {
							if (baseURL.endsWith("/"))
								link = baseURL.toString() + link.substring(1);
							else
								link = baseURL.toString() + link;
						} else {
							if (baseURL.endsWith("/"))
								link = baseURL.toString() + link;
							else
								link = baseURL.toString() + "/" + link;
						}
						faeUtil.debug(urlNum + ":" + cnt + ": depth:" + depth
								+ ": found2 " + link);
					}
				}

				// match URL and traverse
				if (authorizationUrlMatch(faeUtil, urlNum, cnt, link)) {
					if (traverseIt(faeUtil, url, depth, urlNum, cnt,
							m_loggedInURL))
						traverseURL(faeUtil, url, m_loggedInURL, depth + 1,
								newBase);
					// processor.process(faeUtil, link, url1);
				}
				// should we traverse this new URL?
				else if (traverseIt(faeUtil, url, depth, urlNum, cnt, link))
					traverseURL(faeUtil, url, link, depth + 1, newBase);

				cnt++;
			}
		}
	}

	// =========================================================================
	// =========================================================================
	/**
	 * Return true if URL found matches with url in the authorization xml file.
	 * 
	 * @throws Exception
	 */
	private boolean authorizationUrlMatch(FaeUtil faeUtil, int urlNum, int cnt,
			String url) throws Exception {
		boolean urlMatch = false;

		String matcher = url;

		Document doc = faeUtil.getAuthorizationDoc();
		XPath xpath = faeUtil.getAuthorizationXpath();
		for (String tmp : faeUtil.getAuthorizationURLs()) {

			String matchType = (String) (xpath.compile("//authorization[url='"
					+ tmp + "']/url-match/@type")).evaluate(doc,
					XPathConstants.STRING);

			if (matchType.equals("endsWith")) {
				if (url.endsWith(tmp)
						&& !m_alreadyProcessedAuthorizationUrls.contains(tmp)) {
					urlMatch = true;
					matcher = tmp;
					m_alreadyProcessedAuthorizationUrls.add(tmp);
					break;
				}
			}

			else if (matchType.equals("startsWith")) {
				if (url.startsWith(tmp)
						&& !m_alreadyProcessedAuthorizationUrls.contains(tmp)) {
					urlMatch = true;
					matcher = tmp;
					m_alreadyProcessedAuthorizationUrls.add(tmp);
					break;
				}
			}

			else if (matchType.equals("contains")) {
				if (url.contains(tmp)
						&& !m_alreadyProcessedAuthorizationUrls.contains(tmp)) {
					urlMatch = true;
					matcher = tmp;
					m_alreadyProcessedAuthorizationUrls.add(tmp);
					break;
				}
			}
			// check for full string match
			else if (faeUtil.getAuthorizationURLs().contains(url)
					&& !m_alreadyProcessedAuthorizationUrls.contains(url)) {
				urlMatch = true;
				m_alreadyProcessedAuthorizationUrls.add(url);
				break;
			}
		}
		// check for starts with match
		/*
		 * else { for (String tmp : faeUtil.getAuthorizationURLs()) { if
		 * (url.startsWith(tmp) &&
		 * !m_alreadyProcessedAuthorizationUrls.contains(tmp)) { urlMatch =
		 * true; matcher = tmp; m_alreadyProcessedAuthorizationUrls.add(tmp);
		 * break; } } }
		 */

		// If url match, perform login checks
		if (urlMatch) {
			// System.out.println("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
			System.out.println(urlNum + ":" + cnt
					+ ": AUTHORIZATION URL MATCH: " + url);
			processLogin(faeUtil, urlNum, cnt, url, matcher);
		}
		return urlMatch;
	}

	// =========================================================================
	// =========================================================================
	/**
	 * Login to given url and set 'next' page to m_loggedInURL.
	 * 
	 * @throws Exception
	 */
	public void processLogin(FaeUtil faeUtil, int urlNum, int cnt, String url,
			String matcher) throws Exception {
		Document doc = faeUtil.getAuthorizationDoc();
		XPath xpath = faeUtil.getAuthorizationXpath();

		// Extract xml data based on url
		String submitName = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/submit/@name")).evaluate(doc,
				XPathConstants.STRING);
		String submitValue = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/submit/@value")).evaluate(doc,
				XPathConstants.STRING);
		String submitTag = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/submit/@tag")).evaluate(doc,
				XPathConstants.STRING);
		String submitType = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/submit/@type")).evaluate(doc,
				XPathConstants.STRING);
		Double formIndex = (Double) (xpath.compile("//authorization[url='"
				+ matcher + "']/form/@index")).evaluate(doc,
				XPathConstants.NUMBER);
		String formName = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/form/@name")).evaluate(doc,
				XPathConstants.STRING);
		String formId = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/form/@id"))
				.evaluate(doc, XPathConstants.STRING);
		String formuser = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/control/@name")).evaluate(doc,
				XPathConstants.STRING);
		String formpass = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/control[2]/@name")).evaluate(doc,
				XPathConstants.STRING);
		String user = (String) (xpath.compile("//authorization[url='" + matcher
				+ "']/control/@value")).evaluate(doc, XPathConstants.STRING);
		String pass = (String) (xpath.compile("//authorization[url='" + matcher
				+ "']/control[2]/@value")).evaluate(doc, XPathConstants.STRING);
		String anchorText = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/anchor/@text")).evaluate(doc,
				XPathConstants.STRING);
		String verification = (String) (xpath.compile("//authorization[url='"
				+ matcher + "']/verification/@enabled")).evaluate(doc,
				XPathConstants.STRING);
		String verificationText = (String) (xpath
				.compile("//authorization[url='" + matcher
						+ "']/verification/@text")).evaluate(doc,
				XPathConstants.STRING);
		Double controlCount = (Double) (xpath.compile("//authorization[url='"
				+ matcher + "']/control/@count")).evaluate(doc,
				XPathConstants.NUMBER);

		// Disable htmlunit warnings
		webClient.close();
		webClient.getCookieManager().clearCookies();
		webClient.getOptions().setUseInsecureSSL(true);
		webClient.getOptions().setThrowExceptionOnScriptError(false);
		if (faeUtil.m_ctrl.JAVA_SCRIPT.equals("false"))
			webClient.getOptions().setJavaScriptEnabled(false);
		else
			webClient.getOptions().setJavaScriptEnabled(true);
		webClient
				.setCssErrorHandler(new com.gargoylesoftware.htmlunit.SilentCssErrorHandler());

		// Get the first page
		HtmlPage page1 = webClient.getPage(url);
		if (!anchorText.isEmpty()) {
			HtmlAnchor anchor = (HtmlAnchor) page1.getAnchorByText(anchorText);
			page1 = (HtmlPage) anchor.click();
		}

		// Set the form
		HtmlForm form = null;
		// form with name
		if (!formName.isEmpty())
			form = page1.getFormByName(formName);
		// form with id
		else if (!formId.isEmpty())
			form = (HtmlForm) page1.getElementById(formId);
		else if (!formIndex.toString().equals("NaN"))
			form = (HtmlForm) page1.getForms().get(formIndex.intValue());
		// HtmlForm form1 = (HtmlForm) page1.getElementById(form);
		System.out.println(urlNum + ":" + cnt + ": PERFORMING LOGIN");

		// Set login details for a page with more than two fields
		if (!controlCount.toString().equals("NaN")) {

			for (int i = 1; i <= controlCount.intValue(); i++) {
				String controlName = (String) (String) (xpath
						.compile("//authorization[url='" + matcher
								+ "']/control[@id='" + i + "']/@name"))
						.evaluate(doc, XPathConstants.STRING);
				String controlValue = (String) (xpath
						.compile("//authorization[url='" + matcher
								+ "']/control[@id='" + i + "']/@value"))
						.evaluate(doc, XPathConstants.STRING);
				form.getInputByName(controlName)
						.setValueAttribute(controlValue);
			}
		} else {
			// set login details for regular page
			form.getInputByName(formuser).setValueAttribute(user);
			form.getInputByName(formpass).setValueAttribute(pass);
		}

		// Submit the form by clicking the button and get back the second page
		/*
		 * HtmlPage page2; if(!submit.isEmpty()) page2 = (HtmlPage)
		 * form1.getInputByValue(submit).click(); else
		 */
		HtmlPage page2 = null;
		if (!submitName.isEmpty())
			page2 = (HtmlPage) form.getInputByName(submitName).click();
		else if (!submitValue.isEmpty())
			page2 = (HtmlPage) form.getInputByValue(submitValue).click();
		else if (!submitTag.isEmpty() && !submitType.isEmpty())
			page2 = (HtmlPage) form
					.getElementsByAttribute(submitTag, "type", submitType)
					.get(0).click();

		m_loggedInURL = page2.getUrl().toString();

		if (!verification.isEmpty() && verification.equals("true")) {
			if (!verificationText.isEmpty()
					&& page2.asText().contains(verificationText)
					&& !user.isEmpty() && !pass.isEmpty()) {
				System.out.println(urlNum + ":" + cnt + ": LOGIN SUCCESSFUL");
				m_loginSuccessURLs.add(url);
			} else if (!verificationText.isEmpty()
					&& page2.asXml().contains(verificationText)
					&& !user.isEmpty() && !pass.isEmpty()) {
				System.out.println(urlNum + ":" + cnt + ": LOGIN SUCCESSFUL");
				m_loginSuccessURLs.add(url);
			} else {
				System.err
						.println(urlNum
								+ ":"
								+ cnt
								+ ": LOGIN FAILED WITH SUPPLIED CREDENTIALS IN authorization.xml!");
				m_loginFailURLs.add(url);
			}
		} else if (verification.equals("false") || verification.isEmpty()) {
			if (!user.isEmpty() && !pass.isEmpty()) {
				System.out.println(urlNum + ":" + cnt + ": LOGIN SUCCESSFUL");
				m_loginSuccessURLs.add(url);
			} else {
				System.err
						.println(urlNum
								+ ":"
								+ cnt
								+ ": LOGIN FAILED WITH SUPPLIED CREDENTIALS IN authorization.xml!");
				m_loginFailURLs.add(url);
			}
		}

	}

	// =========================================================================
	// =========================================================================
	/**
	 * Process each page and retrieve image urls.
	 * 
	 * @throws Exception
	 */
	public static void imageLinks(HtmlPage page) throws Exception {
		FaeUtil faeUtil = new FaeUtil();

		System.out.println(" ----- Retrieving Image Links:");

		// Extract image links from the final page
		List<DomElement> it = page.getElementsByTagName("img");
		Iterator<DomElement> it1 = it.iterator();

		int i = 0;
		while (it1.hasNext()) {
			HtmlElement element1 = null;
			DomElement element = it1.next();
			if (element instanceof HtmlImage) {
				HtmlImage input = (HtmlImage) element;
				element1 = input;
				HtmlPage page3 = element1.click();
				faeUtil.dumpNode(page3);
				i++;
			}
		}

		if (i == 0) {
			System.out.println("0 image link(s) retrieved.\n");
		} else
			System.out.println(i + " image link(s) retrieved.\n");
	}

	// ==========================================================================
	// ==========================================================================
	/**
	 * Return true if should traverse given url.
	 * 
	 * @throws MalformedURLException
	 */
	public boolean traverseIt(FaeUtil faeUtil, String urlFrom, int depth,
			int urlNum, int cnt, String url) throws MalformedURLException {
		boolean traverseIt = true;
		String msg = null;

		// check depth
		if (depth > faeUtil.DEPTH) {
			traverseIt = false;
		}

		// check already read
		if (faeUtil.m_urlsRead.contains(url)) {
			traverseIt = false;
			msg = urlNum + ":" + cnt + ": depth:" + depth + ": " + url
					+ " ALREADY READ, NOT PROCESSING";
		}

		// check do not read list
		for (String doNotRead : faeUtil.m_urlsToNotTraverse) {
			if (url.startsWith(doNotRead)) {
				traverseIt = false;
				msg = urlNum + ":" + cnt + ": depth:" + depth + ": " + url
						+ " MATCHES DO NOT READ LIST, NOT PROCESSING";
			}
		}

		if (traverseIt) {

			// check spanDomains
			if (faeUtil.m_ctrl.SPAN_DOMAINS != null) {
				boolean match = false;
				StringTokenizer st = new StringTokenizer(
						faeUtil.m_ctrl.SPAN_DOMAINS, ",");
				while (st.hasMoreTokens()) {
					String tok = st.nextToken();
					// System.out.println("---------------------------");
					// System.out.println(tok);
					if (tok.equals("*")) {
						match = true;
						break;
					}
					if (url.contains("http") && url.indexOf(tok + "/") != -1) {
						URL t = new URL(url);
						if (t.getHost().indexOf(tok) != -1){
							String prefix = t.getHost().substring(0,
									t.getHost().indexOf(tok));
							// System.out.println(prefix);
							// count number of periods
							int num = countOccurrences(prefix, '.');
							// System.out.println(num);
							if (num == 0 || num == 1) {
								match = true;
								break;
							}
						} else {
							match = false;
							break;
						}
					}
				}
				// System.out.println(url + ": match => " + match);
				if (!match) {
					traverseIt = false;
					faeUtil.m_filteredURLs.add(url);
					String timing = "\"" + url + "\",\"" + urlFrom + "\"";
					faeUtil.m_filteredURLsCSV.add(timing);
					msg = urlNum + ":" + cnt + ": depth:" + depth + ": " + url
							+ " DOES NOT MATCH ANY SPAN DOMAIN, NOT PROCESSING";
				}
			} else {
				traverseIt = false;
				faeUtil.m_filteredURLs.add(url);
				String timing = "\"" + url + "\",\"" + urlFrom + "\"";
				faeUtil.m_filteredURLsCSV.add(timing);
				msg = urlNum + ":" + cnt + ": depth:" + depth + ": " + url
						+ ": NO SPAN DOMAINS GIVEN, NOT PROCESSING";
			}

			// // check domain or host match
			// if (FaeUtil.m_host != null && FaeUtil.m_host.length() > 0) {
			// if (FaeUtil.m_traverseSubDomains) {
			// if (!url.contains(FaeUtil.m_host)) {
			// traverseIt = false;
			// FaeUtil.m_filteredURLs.add(url);
			// FaeUtil.verbose(urlNum + ":" + cnt + ": depth:" + depth + ": " +
			// url + " DOES NOT MATCH DOMAIN, NOT PROCESSING");
			// }
			// }
			// else {
			// if (!url.startsWith(FaeUtil.m_host)) {
			// traverseIt = false;
			// FaeUtil.m_filteredURLs.add(url);
			// FaeUtil.verbose(urlNum + ":" + cnt + ": depth:" + depth + ": " +
			// url + " DOES NOT MATCH HOST, NOT PROCESSING");
			// }
			// }
			// }

			// check includeDomains
			// System.out.println(Controller.INCLUDE_DOMAINS);
			if (faeUtil.m_ctrl.INCLUDE_DOMAINS != null) {
				if(count(url,"http") == 1) {
					StringTokenizer st = new StringTokenizer(
							faeUtil.m_ctrl.INCLUDE_DOMAINS, ",");
					while (st.hasMoreTokens()) {
						String tok = st.nextToken();
						// System.out.println(tok);
						if (url.indexOf("/" + tok + "/") != -1) {
							traverseIt = true;
							faeUtil.m_filteredURLs.remove(url);
							String timing = "\"" + url + "\",\"" + urlFrom + "\"";
							faeUtil.m_filteredURLsCSV.remove(timing);
							msg = urlNum + ":" + cnt + ": depth:" + depth + ": "
									+ url + " MATCHES INCLUDE DOMAIN " + tok
									+ ", PROCESSING";
						}
					}
				}
			}

			// check excludeDomains
			// System.out.println(Controller.EXCLUDE_DOMAINS);
			if (faeUtil.m_ctrl.EXCLUDE_DOMAINS != null) {
				StringTokenizer st = new StringTokenizer(
						faeUtil.m_ctrl.EXCLUDE_DOMAINS, ",");
				while (st.hasMoreTokens()) {
					String tok = st.nextToken();
					// System.out.println(tok);
					if (url.indexOf("/" + tok + "/") != -1) {
						traverseIt = false;
						faeUtil.m_filteredURLs.add(url);
						String timing = "\"" + url + "\",\"" + urlFrom + "\"";
						faeUtil.m_filteredURLsCSV.add(timing);
						msg = urlNum + ":" + cnt + ": depth:" + depth + ": "
								+ url + " MATCHES EXCLUDE DOMAIN " + tok
								+ ", NOT PROCESSING";
					}
				}
			}

		}

		if (msg != null)
			faeUtil.verbose(msg);
		return traverseIt;
	}

	// ==========================================================================
	// ==========================================================================
	/**
	 * Will process/read the given URL. DOES NOT TRAVERSE HERE! Creates an
	 * instance of Processor class to run on a thread and then 'monitors' how
	 * long it takes to process. If takes longer than MAX_WAIT it will kill the
	 * thread.
	 */
	public void process(FaeUtil faeUtil, String urlFrom, String url) {
		faeUtil.m_urlsRead.add(url);
		int urlNum = faeUtil.m_urlCount;
		faeUtil.m_urlCount++;

		try {
			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// make a WebClient for each URL - DON"T DO THIS NOW SINCE LOGGING
			// IN LOGIC ADDED!
			// WebClient webClient = new WebClient(faeUtil.BROWSER_VERSION);
			faeUtil.initWebClient(webClient);
			// webClient.getOptions().setThrowExceptionOnScriptError(false);
			// webClient.getOptions().setUseInsecureSSL(true); // JSH added

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// timing variables
			long diff = 0;
			java.util.Date start = new java.util.Date();
			java.util.Date end;

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// make the Thread to process with
			m_processor = new Processor(faeUtil, webClient, urlNum, url,
					urlFrom);
			Thread th = new Thread(m_processor);

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// set to processing = true
			m_processingURL = true;

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// start processing...check how long it takes and break if too long
			try {
				th.start();
				while (m_processingURL) {
					Thread.sleep(1000);
					end = new java.util.Date();
					diff = end.getTime() - start.getTime();
					// System.out.println(m_processingURL + " " + diff);
					if (diff > faeUtil.WAIT) {
						// System.out.println("*** breaking " + diff);
						faeUtil.m_unprocessedURLs.add(new URL(url));
						String timing = "\"" + url + "\",\"" + urlFrom + "\",";
						timing += m_processor.m_loadTime + ",";
						timing += m_processor.m_findEventsTime + ",";
						timing += m_processor.m_findEventsTime + ",";
						timing += m_processor.m_scriptProcessingTime + ",";
						timing += (m_processor.m_loadTime
								+ m_processor.m_findEventsTime
								+ m_processor.m_findEventsTime + m_processor.m_scriptProcessingTime);
						faeUtil.m_unprocessedURLsCSV.add(timing);
						System.err.println("COULD NOT PROCESS URL: " + url
								+ ". WAITED " + diff + "ms.");
						th.interrupt();
						Thread.sleep(3000); // give some time for resources to
											// clean up
						break;
					}
				}
			} catch (Exception e) {
				e.printStackTrace();
			} finally {
				 if (webClient != null)
					 webClient.close();
			}

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// webClient = null;

			// ------------------------------------------------------------------------
			// ------------------------------------------------------------------------
			// record timings
			String timing = urlNum + ",\"" + url + "\",\""
					+ m_processor.m_urlRead + "\",\"" + urlFrom + "\",";
			timing += m_processor.m_statusCode + ",";
			timing += m_processor.m_loadTime + ",";
			timing += m_processor.m_findEventsTime + ",";
			timing += m_processor.m_findEventsTime + ",";
			timing += m_processor.m_scriptProcessingTime + ",";
			timing += (m_processor.m_loadTime + m_processor.m_findEventsTime
					+ m_processor.m_findEventsTime + m_processor.m_scriptProcessingTime);
			faeUtil.m_processedURLsCSV.add(timing);
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	// ==========================================================================
	// ==========================================================================
	/** Will return the Processor instance used in reading/evaluating the URL. */
	public Processor getProcessor() {
		return m_processor;
	}

	// ==========================================================================
	// ==========================================================================
	public static int countOccurrences(String haystack, char needle) {
		int count = 0;
		for (int i = 0; i < haystack.length(); i++) {
			if (haystack.charAt(i) == needle) {
				count++;
			}
		}
		return count;
	}

	// ==========================================================================
	// ==========================================================================
	public static void main(String[] args) {
		try {
			// ======================================================================
			// SETUP FaeUtil
			// ======================================================================
			FaeUtil faeUtil = new FaeUtil();

			faeUtil.VERBOSE = true;

			faeUtil.m_ctrl.EXCLUDE_DOMAINS = "";
			System.out.println("EXCLUDE_DOMAINS => "
					+ faeUtil.m_ctrl.EXCLUDE_DOMAINS);

			faeUtil.m_ctrl.INCLUDE_DOMAINS = "illinois.edu";
			System.out.println("INCLUDE_DOMAINS => "
					+ faeUtil.m_ctrl.INCLUDE_DOMAINS);

			faeUtil.m_ctrl.SPAN_DOMAINS = "";
			// Controller.SPAN_DOMAINS = "illinois.edu,junk.com";
			System.out
					.println("SPAN_DOMAINS => " + faeUtil.m_ctrl.SPAN_DOMAINS);

			Vector<String> testURLs = new Vector<String>();
			testURLs.add("http://illinois.edu/");
			testURLs.add("http://www.illinois.edu/");
			testURLs.add("http://www.cites.illinois.edu/email/logins.html");
			testURLs.add("http://odos.illinois.edu/newstudent/Programs/WelcomeDays.html");
			testURLs.add("http://illinois.edu/arts/arts.html");
			testURLs.add("http://go.illinois.edu/visioningoutcomesreport");
			testURLs.add("http://www.library.illinois.edu/cmservices");
			testURLs.add("http://www.business.illinois.edu/");
			testURLs.add("http://news.illinois.edu/news/13/0806music_theory_app_HeinrichTaube.html");
			testURLs.add("http://www.uiaa.org/urbana/");
			testURLs.add("http://www.uic.edu/");
			testURLs.add("http://uiedev.extension.uiuc.edu/100yrs/");
			testURLs.add("http://www.online.uillinois.edu/");
			// testURLs.add("xxx");

			// ======================================================================
			// SETUP URLProcessor
			// ======================================================================
			URLProcessor processor = new URLProcessor();

			// ======================================================================
			// TEST
			// ======================================================================
			for (String url : testURLs) {
				System.out
						.println("=============================================");

				boolean match = false;
				StringTokenizer st = new StringTokenizer(
						faeUtil.m_ctrl.SPAN_DOMAINS, ",");
				while (st.hasMoreTokens()) {
					String tok = st.nextToken();
					// System.out.println("---------------------------");
					// System.out.println(tok);
					if (url.indexOf(tok + "/") != -1) {
						URL t = new URL(url);
						String prefix = t.getHost().substring(0,
								t.getHost().indexOf(tok));
						// System.out.println(prefix);
						// count number of periods
						int num = countOccurrences(prefix, '.');
						// System.out.println(num);
						if (num == 0 || num == 1) {
							match = true;
							break;
						}
					}
				}
				System.out.println(url + ": match => " + match);

				boolean traverseIt = processor.traverseIt(faeUtil, "BASE", 0,
						0, 0, url);
				System.out.println(url + ": traverseIt => " + traverseIt);
			}

			if (true)
				System.exit(0);

			// String url_str = "http://illinois.edu/";
			// String url_str = "http://www.illinois.edu/";
			// String url_str = "http://business.nd.edu/accountancy/";
			String url_str = "http://bc.edu/";
			// String url_str = "http://ls.wisc.edu/";
			System.out.println("url_str: " + url_str);

			URL url = new URL(url_str);
			System.out.println("url: " + url);

			String baseUrl = url.getProtocol() + "://" + url.getHost() + "/";
			System.out.println("baseUrl: " + baseUrl);

			String domain = url.getHost();
			if (domain.startsWith("www."))
				domain = domain.substring(4);
			System.out.println("domain: " + domain);

			// URI uri = new URI(url_str);
			// FaeUtil.m_host = baseUrl;
			// FaeUtil.m_host = url.getHost();
			// System.out.println("FaeUtil.m_host: " + FaeUtil.m_host);

			// if going to traverse subDomains then set host to domain
			// if not traversing subDomains then do a startsWith check
			// if traversing subDomains then do a contains check
			// FaeUtil.m_traverseSubDomains = true;
			// System.out.println("FaeUtil.m_traverseSubDomains: " +
			// FaeUtil.m_traverseSubDomains);
			// if (FaeUtil.m_traverseSubDomains)
			// FaeUtil.m_host = domain;
			// else
			// FaeUtil.m_host = baseUrl;
			// System.out.println("FaeUtil.m_host: " + FaeUtil.m_host);

			faeUtil.DEBUG = true;
			System.out.println("FaeUtil.m_debug: " + faeUtil.DEBUG);
			faeUtil.VERBOSE = true;
			System.out.println("FaeUtil.m_verbose: " + faeUtil.VERBOSE);

			FIND_EVENTS = false;
			System.out.println("FIND_EVENTS: " + FIND_EVENTS);
			EVAL_SCRIPT = false;
			System.out.println("EVAL_SCRIPT: " + EVAL_SCRIPT);
			FIND_LINKS = true;
			System.out.println("FIND_LINKS: " + FIND_LINKS);

			faeUtil.DEPTH = 2;
			System.out.println("FaeUtil.DEPTH: " + faeUtil.DEPTH);

			faeUtil.m_urlsToNotTraverse.add("http://msn.com/");
			faeUtil.m_urlsToNotTraverse.add("http://www.bc.edu/offices/pubaf/");
			System.out.println("faeUtil.m_doNotRead: "
					+ faeUtil.m_urlsToNotTraverse);

			faeUtil.m_extensionsToNotProcess.add("pdf");
			faeUtil.m_extensionsToNotProcess.add("xml");
			System.out.println("faeUtil.m_extensionsToNotProcess: "
					+ faeUtil.m_extensionsToNotProcess);

			try {
				faeUtil.m_evaluationScript = FileUtil
						.concatenateFiles(
								"/home/jheckel/DRESWork/ainspector-util-read-only/test/scripts.txt",
								true);
			} catch (Exception e) {
				e.printStackTrace();
			}
			System.out.println("faeUtil.m_evaluationScript: "
					+ faeUtil.m_evaluationScript);

			URLProcessor tmp = new URLProcessor();

			// ======================================================================
			// ======================================================================
			// IF NOT TRAVERSING
			faeUtil.m_urlCount = 0;
			faeUtil.m_urlsRead.clear(); // need to clear after previous run
			System.out.println("\n\n");
			tmp.process(faeUtil, "BASE", url_str);
			Vector<String> linksFound = tmp.getProcessor().getLinksFound();
			if (linksFound.size() == 0)
				System.out.println("no URLs found");
			int cnt = 0;
			Collections.sort(linksFound);
			for (String found : linksFound) {
				System.out.println(cnt++ + ": " + "found " + found);
			}

			// ======================================================================
			// ======================================================================
			// IF TRAVERSING
			faeUtil.m_urlCount = 0;
			faeUtil.m_urlsRead.clear(); // need to clear after previous run
			System.out.println("\n\n");
			tmp.traverseURL(faeUtil, "BASE", url_str, 1, baseUrl);
			if (faeUtil.m_urlsRead.size() > 1) {
				System.out.println(faeUtil.m_urlsRead.size()
						+ " total URLs traversed. All URLs traversed:");
				System.out.println("IN READ ORDER");
				cnt = 0;
				for (String t : faeUtil.m_urlsRead) {
					System.out.println("\t" + cnt++ + ": " + t);
				}
				System.out.println("IN ALPHABETICAL ORDER");
				cnt = 0;
				Collections.sort(faeUtil.m_urlsRead);
				for (String t : faeUtil.m_urlsRead) {
					System.out.println("\t" + cnt++ + ": " + t);
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	/**
	 * Class that reads the page, find events, evaluate script, and finds links.
	 */
	public static class Processor implements Runnable {

		private FaeUtil m_faeUtil;
		private WebClient m_webClient;
		private int m_urlNum;
		private String m_url;
		private String m_urlFrom;
		public String m_urlRead;
		public int m_statusCode;

		private Vector<String> m_linksFound = new Vector<String>();

		// ==========================================================================
		// ==========================================================================
		public Processor(FaeUtil faeUtil, WebClient webClient, int urlNum,
				String url, String urlFrom) throws MalformedURLException {
			m_faeUtil = faeUtil;
			m_webClient = webClient;
			m_urlNum = urlNum;
			m_url = url;
			m_urlFrom = urlFrom;
		}

		// ==========================================================================
		// ==========================================================================
		/** Get URL number - mainly used in output display. */
		public int getUrlNum() {
			return m_urlNum;
		}

		// ==========================================================================
		// ==========================================================================
		/** Get URL to process. */
		public String getUrl() {
			return m_url;
		}

		// ==========================================================================
		// ==========================================================================
		/** Gets links found during processing. */
		public Vector<String> getLinksFound() {
			return m_linksFound;
		}

		public long m_loadTime;
		public long m_findLinksTime;
		public long m_findEventsTime;
		public long m_scriptProcessingTime;

		// ==========================================================================
		// ==========================================================================
		@Override
		public void run() {
			m_faeUtil
					.verbose("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
			System.out.println(m_urlNum + ": PROCESSING " + m_url);
			m_faeUtil
					.verbose("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");

			// FOR REAL WORK
			try {
				long startTime, endTime;

				// ------------------------------------------------------------------------
				// ------------------------------------------------------------------------
				m_faeUtil.updateStatus("processing", m_url);

				// ------------------------------------------------------------------------
				// ------------------------------------------------------------------------
				// Get the page to analyze
				m_faeUtil.verbose(" ----- READING PAGE");
				// FaeUtil.verbose("----------------------------------------");
				m_faeUtil.verbose("\t" + m_urlNum + ": Retrieving DOM... ");
				startTime = System.currentTimeMillis();
				
				URL requestUrl = new URL(m_url);
				HtmlPage page = m_webClient.getPage(requestUrl);

				// List<FrameWindow> window = page.getFrames();
				m_faeUtil.debug(" &&&&& " + page.getWebResponse());
				m_faeUtil.debug(" &&&&& "
						+ page.getWebResponse().getStatusCode());
				m_faeUtil.debug(" &&&&& "
						+ page.getWebResponse().getStatusMessage());
				m_faeUtil.debug(" &&&&& "
						+ page.getWebResponse().getWebRequest().getUrl());
				this.m_urlRead = page.getWebResponse().getWebRequest().getUrl()
						.toString();
				this.m_statusCode = page.getWebResponse().getStatusCode();
				// m_faeUtil.dumpNode(page);
				// for (int i = 0; i < window.size(); i++) {// page within the
				// frames
				// HtmlPage page2 = (HtmlPage) window.get(i).getEnclosedPage();
				// m_faeUtil.dumpNode(page2);
				// }
				// imageLinks(page);// retrieve image urls
				endTime = System.currentTimeMillis();
				m_loadTime = endTime - startTime;
				m_faeUtil.verbose("\t" + m_loadTime + " msec.");

				if (!requestUrl.equals(page.getWebResponse().getWebRequest()
						.getUrl())) {
					m_faeUtil.debug(" &&&&& REDIRECTION");
				}

				if (page.getWebResponse().getStatusCode() == HttpStatus.FORBIDDEN_403
						|| page.getWebResponse().getStatusCode() == HttpStatus.NOT_FOUND_404) {
					try {
						m_faeUtil.m_unprocessedURLs.add(new URL(m_url));
						String timing = "\"" + m_url + "\",\"" + m_urlFrom
								+ "\",";
						timing += m_loadTime + ",";
						timing += m_findEventsTime + ",";
						timing += m_findEventsTime + ",";
						timing += m_scriptProcessingTime + ",";
						timing += (m_loadTime + m_findEventsTime
								+ m_findEventsTime + m_scriptProcessingTime);
						m_faeUtil.m_unprocessedURLsCSV.add(timing);
					} catch (MalformedURLException e1) {
						e1.printStackTrace();
					}
				} else {
					// ------------------------------------------------------------------------
					// ------------------------------------------------------------------------
					// Find URLs on page
					if (FIND_LINKS) {
						m_faeUtil.verbose(" ----- FINDING LINKS");
						// FaeUtil.verbose("----------------------------------------");
						m_faeUtil.verbose("\t" + m_urlNum
								+ ": Looking for links... ");
						startTime = System.currentTimeMillis();
						excludedURLParent = m_url;
						m_faeUtil.findLinks(page, "", m_linksFound);
						endTime = System.currentTimeMillis();
						// for (String link : m_linksFound) {
						// FaeUtil.debug("link=> " + link);
						// }
						m_faeUtil.verbose("\t" + m_linksFound.size()
								+ " links found");
						m_findLinksTime = endTime - startTime;
						m_faeUtil.verbose("\t" + m_findLinksTime + " msec.");
					}

					// ------------------------------------------------------------------------
					// ------------------------------------------------------------------------
					// Look for events
					if (FIND_EVENTS) {
						m_faeUtil.verbose(" ----- FINDING EVENTS");
						// FaeUtil.verbose("----------------------------------------");
						m_faeUtil.verbose("\t" + m_urlNum
								+ ": Looking for events... ");
						startTime = System.currentTimeMillis();
						m_faeUtil.findEvents(page, "");
						endTime = System.currentTimeMillis();
						m_findEventsTime = endTime - startTime;
						m_faeUtil.verbose("\t" + m_findEventsTime + " msec.");
					}
					
					//TODO: Wait some time before executing evaluation script.

					// ------------------------------------------------------------------------
					// ------------------------------------------------------------------------
					// Run the concatenated JavaScript scripts against the page
					if (EVAL_SCRIPT) {
						if (m_faeUtil.m_evaluationScript != null
								&& m_faeUtil.m_evaluationScript.length() > 0) {
							m_faeUtil.verbose(" ----- EVALUATING SCRIPT");
							// FaeUtil.verbose("----------------------------------------");
							m_webClient.getOptions().setThrowExceptionOnScriptError(false);
							m_faeUtil.verbose("\t" + m_urlNum
									+ ": Running evaluation scripts... ");
							startTime = System.currentTimeMillis();

							ScriptResult result = page.executeJavaScript(m_faeUtil.m_evaluationScript);

							// System.out.println("result=>" + result);
							// System.out.println("result.getJavaScriptResult()=>"
							// + result.getJavaScriptResult());
							m_faeUtil
									.verbose(result.getJavaScriptResult() == null ? "null"
											: result.getJavaScriptResult()
													.toString());
							endTime = System.currentTimeMillis();
							m_scriptProcessingTime = endTime - startTime;
							m_faeUtil.verbose("\t" + m_scriptProcessingTime
									+ " msec.");

							// ------------------------------------------------------------------------
							// ------------------------------------------------------------------------
							// Process the JavaScript result
							long total = m_loadTime + m_findLinksTime
									+ m_findEventsTime + m_scriptProcessingTime;
							m_faeUtil.processResult(m_urlNum, result, total);
						}
					}
				}
			} catch (Exception e) {
				e.printStackTrace();
				try {
					m_faeUtil.m_unprocessedURLs.add(new URL(m_url));
					String timing = "\"" + m_url + "\",\"" + m_urlFrom + "\",";
					timing += m_loadTime + ",";
					timing += m_findEventsTime + ",";
					timing += m_findEventsTime + ",";
					timing += m_scriptProcessingTime + ",";
					timing += (m_loadTime + m_findEventsTime + m_findEventsTime + m_scriptProcessingTime);
					m_faeUtil.m_unprocessedURLsCSV.add(timing);
				} catch (MalformedURLException e1) {
					e1.printStackTrace();
				}
			}

			// FOR TESTING PURPOSES
			// try {
			// System.out.println("hey: " + m_url);
			// for (int i = 0; i < 10; ++i) {
			// Thread.sleep(1000);
			// System.out.println("\t... " + m_url);
			// }
			// }
			// catch (InterruptedException e) {
			// e.printStackTrace();
			// }

			m_processingURL = false;

			m_faeUtil.debug(m_urlNum + ": leaving Processor:run");
		}
	}
	
	/**
	   * Count the number of instances of substring within a string.
	   *
	   * @param string     String to look for substring in.
	   * @param substring  Sub-string to look for.
	   * @return           Count of substrings in string.
	   */
	  public static int count(final String string, final String substring)
	  {
	     int count = 0;
	     int idx = 0;

	     while ((idx = string.indexOf(substring, idx)) != -1)
	     {
	        idx++;
	        count++;
	     }

	     return count;
	  }

}
