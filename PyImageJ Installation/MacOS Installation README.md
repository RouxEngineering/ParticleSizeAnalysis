## MacOS README for Installing PyImageJ


PyImageJ Requirements
- Java/OpenJDK 11.0 
- ImageJ 
- Maven 3.8.8 
- Homebrew


Downloading ImageJ
1.	Refer to ImageJ download [website](https://imagej.net/ij/download.html)
2.	Download ImageJ based on MacOS operating system and follow the installation instructions


Downloading Maven 3.8.8
1.	Refer to Maven download [website](https://maven.apache.org/download.cgi) and download Stable 3.8x Release
2.	Download source tar.gz formatted file and follow installation instructions
3.	Verify Maven version 3.8.8 by running the command: <ins>mvn -v</ins> your terminal


Download PyImageJ
1.	Go to your terminal and type in the command: <ins>pip install pyimagej</ins>


Downloading and setting up Java/OpenJDK 11.0 
1.	Refer to Oracle Java download [website](https://www.oracle.com/java/technologies/downloads/)
2.	Download JDK based on MacOS operating system and follow installation instructions
3.	Open terminal to install Java 11.0 
4.	Ensure you have Homebrew installed onto your operating system 
5.	In terminal run the command: <ins>brew install openjdk@11</ins> to install Java 11.0
6.	Set up environment to use new Java version by updating shell profile configuration file (ie. `~/.bash_profile`, `~./zshrc`)
7.	Update shell profile configuration file with the line: <ins>export JAVA_HOME=`/usr/libexec/java_home -v 11`</ins> which sets the default Java version to be used as 11.0
8.	Save the changes made to the shell profile file 
9.	Verify the Java version using the command: <ins>java -version in your terminal</ins>


Testing your installation of PyImageJ 
1.	Run the following command in your console: <ins>python -c 'import imagej; ij = imagej.init("2.14.0"); print(ij.getVersion())'</ins>
2.	The console should return 2.14.0 
