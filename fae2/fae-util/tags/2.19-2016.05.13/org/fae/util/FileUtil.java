package org.fae.util;

import java.io.*;
import java.net.*;
import java.util.*;

class FileUtil {

  /**
   * getNormalFile
   *
   * Create File object f from filename and check whether it exists,
   * is a normal, readable file and not a directory. If any of these
   * conditions are not met, throw an appropriate exception.
   *
   * @param filename Name of file to check
   * @return File object
   */
  public static File getNormalFile(String filename)
    throws IOException {
    File f = new File(filename);
    if (!f.exists())
      throw new FileNotFoundException(filename);
    if (!f.isFile())
      throw new IOException(filename + "is not a normal file.");
    if (!f.canRead())
      throw new IOException(filename + "is not readable.");
    return f;
  }

  /**
   * getFileList
   *
   * If inputFilename is a normal file, and if each of its non-empty lines
   * corresponds to a normal file, convert each to a File object and store
   * in list. Otherwise, throw an appropriate exception.
   *
   * @param inputFilename Name of file containing filenames
   * @return ArrayList<File>
   */
  public static ArrayList<File> getFileList(String inputFilename)
    throws IOException {
    // Check that the input file exists, etc.
    File inputFile = getNormalFile(inputFilename);

    // Check that each filename in inputFile is a normal file
    // and store in fileList unless exception is encountered.
    ArrayList<File> fileList = new ArrayList<File>();

    FileReader fr = new FileReader(inputFile);
    BufferedReader br = new BufferedReader(fr);
    String filename;

    try {
      while ((filename = br.readLine()) != null) {
        // Ignore lines that are empty or only contain whitespace.
        filename = filename.trim();
        if (filename.length() == 0)
          continue;

        // Add file object to fileList if it passes the tests.
        fileList.add(getNormalFile(filename));
      }
    }
    finally {
      fr.close();
    }
    return fileList;
  }

  /**
   * getFileContents
   *
   * Build a string by concatenating all lines in File object.
   *
   * @param f File object
   * @return String
   */
  public static String getFileContents(File f)
    throws Exception {
    FileReader fr = new FileReader(f);
    BufferedReader br = new BufferedReader(fr);
    StringBuilder contents = new StringBuilder();
    String line;

    while ((line = br.readLine()) != null) {
      contents.append(line + lineSep);
    }

    br.close();
    return contents.toString();
  }

  /**
   * getContentsAllFiles
   *
   * Iterate through the fileList and build a string by concatenating
   * the contents of each file in the list in the order of appearance.
   * If the commentsFlag is set, prefix each concatenation with a line
   * containing the filename as a C language style comment.
   *
   * @param fileList ArrayList of File objects
   * @param commentsFlag A boolean indicating whether to insert comments
   * @return String
   */
  public static String getContentsAllFiles(ArrayList<File> fileList, boolean commentsFlag)
    throws Exception {
    StringBuilder contents = new StringBuilder();

    for (File f : fileList) {
      if (debug)
        System.out.println(f.getAbsolutePath());
      if (commentsFlag) {
        contents.append("/* " + f.getAbsolutePath() + " */" + lineSep);
      }
      contents.append(getFileContents(f));
    }
    return contents.toString();
  }

  /**
   * concatenateFiles
   *
   * Convenience method: Build file list, concatenate all files and return result.
   *
   * @param inputFilename Name of file containing filenames
   * @param commentsFlag A boolean indicating whether to insert comments
   * @return String
   */
  public static String concatenateFiles(String inputFilename, boolean commentsFlag)
    throws Exception {
    ArrayList<File> fileList = getFileList(inputFilename);
    return getContentsAllFiles(fileList, commentsFlag);
  }

  /**
   * getUrlList
   *
   * If inputFilename is a normal file, and if each of its non-empty lines
   * corresponds to a URL, store each URL object in list. Otherwise, throw
   * an appropriate exception.
   *
   * @param inputFilename Name of file containing URLs
   * @return ArrayList of String objects
   */
  public static ArrayList<String> getUrlList(String inputFilename)
    throws Exception {
    // Check that the input file exists, etc.
    File inputFile = getNormalFile(inputFilename);

    // Check that each filename in inputFile is a well-formed URL
    // and store in urlList unless exception is encountered.
    ArrayList<String> urlList = new ArrayList<String>();

    FileReader fr = new FileReader(inputFile);
    BufferedReader br = new BufferedReader(fr);
    String line;

    try {
      while ((line = br.readLine()) != null) {
        line = line.trim();

        // Ignore lines that are empty or only contain whitespace.
        if (line.length() == 0)
          continue;

        // Ignore comment lines.
        if (line.startsWith("#"))
          continue;

        // Add URL object to urlList if no exceptions.
        URL url = new URL(line);
        urlList.add(line);
      }
    }
    finally {
      br.close();
    }
    return urlList;
  }

  /**
   * writeStringToFile
   *
   * Write a string, which may include newline characters, line by line
   * to the file specified by filename.
   */
  public static void writeStringToFile(String s, String filename)
    throws IOException {
    String inputStr = s.trim();
    if (inputStr.length() == 0)
      throw new IOException("Input string contains no printable characters.");

    BufferedReader br = new BufferedReader(new StringReader(inputStr));
    BufferedWriter bw = new BufferedWriter(new FileWriter(filename));

    // Read the string line by line and write each to the output file.
    try {
      String line;

      while ((line = br.readLine()) != null) {
        // Ignore lines that are empty or only contain whitespace.
        line = line.trim();
        if (line.length() == 0)
          continue;

        // Write line to output file
        bw.write(line);
        bw.newLine();
      }
    }
    finally {
      br.close();
      bw.close();
    }
  }

  public static void delete(File f)
    throws IOException {
    if (f.isDirectory()) {
      for (File c : f.listFiles())
        delete(c);
    }
    if (!f.delete())
      throw new FileNotFoundException("Failed to delete file: " + f);
  }

  public static void main(String args[]) {
    String scriptsFile = args[0];
    String urlsFile = args[1];
    String outputFile = args[2];

    try {
      // test concatenation of text files
      String s = concatenateFiles(scriptsFile, true);
      System.out.println(s);

      // test reading URLs
      ArrayList<String> urls = getUrlList(urlsFile);
      for (String url : urls) {
        System.out.println(url);
      }

      // test writing string to file
      writeStringToFile(s, outputFile);
    }
    catch (Exception e) {
      System.err.println(e);
    }
  }

  // class variables
  static final boolean debug = false;
  static final String lineSep = System.getProperty("line.separator");
}
