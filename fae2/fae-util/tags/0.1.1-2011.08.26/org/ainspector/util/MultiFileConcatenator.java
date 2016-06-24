package org.ainspector.util;

import java.io.*;
import java.util.*;

class MultiFileConcatenator {

  /**
   * MultiFileConcatenator
   *
   * Store the value of inputFile and initialize the fileList array. Throw
   * an exception if filename does not correspond to a normal readable file.
   *
   * @param filename Name of a text file containing one or more filenames
   * @param commentsFlag Controls output of filename comments in concatenation
   */
  public MultiFileConcatenator(String filename, boolean commentsFlag) throws FileNotFoundException {
    File f = getNormalFile(filename);
    if (f == null)
      throw new FileNotFoundException(filename);

    this.inputFile = f;
    fileList = new ArrayList<File>();
    this.commentsFlag = commentsFlag;
  }

  /**
   * processInputFile
   *
   * Read each line of inputFile and check that it is a filename that
   * corresponds to a normal readable file. If not throw an exception;
   * otherwise store all files in fileList.
   */
  public void processInputFile() throws Exception {
    FileReader fr = new FileReader(inputFile);
    BufferedReader br = new BufferedReader(fr);
    String filename;

    while ((filename = br.readLine()) != null) {
      // Ignore lines that are empty or only contain whitespace.
      filename = filename.trim();
      if (filename.length() == 0) continue;

      // Add file object to fileList if readable.
      File f = getNormalFile(filename);
      if (f == null) {
        fr.close();
        throw new FileNotFoundException(filename);
      }
      fileList.add(f);
    }

    fr.close();
  }

  /**
   * getFileContents
   *
   * Return a string built by concatenating all lines in File object f.
   *
   * @param f File object
   */
  public static String getFileContents(File f) throws Exception {
    FileReader fr = new FileReader(f);
    BufferedReader br = new BufferedReader(fr);
    StringBuilder contents = new StringBuilder();
    String line;

    while ((line = br.readLine()) != null) {
      contents.append(line + sep);
    }

    fr.close();
    return contents.toString();
  }

  /**
   * getContentsAllFiles
   *
   * Iterate through the fileList and build a string by concatenating
   * the contents of each file in the list in the order of appearance.
   * If the commentsFlag is set, prefix each concatenation with a line
   * containing the filename as a C language style comment.
   */
  public String getContentsAllFiles() throws Exception {
    StringBuilder contents = new StringBuilder();

    for (File f : fileList) {
      if (debug) System.out.println(f.getAbsolutePath());
      if (commentsFlag) {
        contents.append("/* " + f.getName() + " */" + sep);
      }
      contents.append(getFileContents(f));
    }
    return contents.toString();
  }

  /**
   * getNormalFile
   *
   * Create a File object from filename and if it corresponds to
   * a normal readable file, return it; otherwise return null.
   *
   * @param filename Name of a normal readable text file
   */
  public static File getNormalFile(String filename) {
    File f = new File(filename);
    if (f.isFile() && f.canRead()) return f;
    return null;
  }

  public static void main (String args[]) {
    String filename = args[0];

    try {
      MultiFileConcatenator mfc = new MultiFileConcatenator(filename, true);
      mfc.processInputFile();
      System.out.print(mfc.getContentsAllFiles());
    }
    catch (Exception e) {
      System.err.println(e);
    }
  }

  // instance variables
  File inputFile;
  ArrayList<File> fileList;
  boolean commentsFlag;

  // class variables
  static final String sep = System.getProperty("line.separator");
  static final boolean debug = false;
}
