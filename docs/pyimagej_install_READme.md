 # README for Installing PyImageJ and Required Dependencies for Macintosh Operating System (MacOS) 
  
This document will help you install the four requirements for running PyImageJ: 

1. Python (Visual studio code + Anaconda[^1]) 
2. PyImageJ 
3. Maven 3.8.8 
4. Java Development Kit 11.0.x 

 
## Prerequisites:  

1. Setting up an Integrated Development Environment (IDE): Visual Studio Code 

a. Navigagte to https://code.visualstudio.com/

b. Select “Download for MacOS”

c. Open the installer and follow the instructions 
 


2. Setting up a Python:  Interpreter (Anaconda) + IDE Extension  

a. Navigate to https://www.anaconda.com/download/success  

b. Verify and select the “Download for Mac” button  


c. Open the Installer and follow the provided installation instructions  

d. Activate Conda  computer system for Conda Location
```text
finder > Applications > Anaconda (right-click) > Show Orginial > File > Get info > Where
```

```bash
source /path/to/anaconda3/bin/activate/
```

e. Verify installation by running the following command in the terminal:  

```bash 
conda –V 
```

e. Navigate to https://marketplace.visualstudio.com/items?itemName=ms-python.python 

f. Click “Install” and follow and instructions  
 


## Installations 

1. Setting up PyimageJ via a projet virtual environment using Conda: 

a. Open the system Terminal, 

b. Create a virtual environment using python 3.9 from the project's `environment.yml` file [here](/env/environment_setup.md).
 

2. Setting up Maven version 3.8.8:

a. Use this hyperlink, https://maven.apache.org/download.cgi , and scroll down to section labeled Previous Stable 3.8.x Release 

b. Download Apache Maven 3.8.8 in the tar.gz format  

c. Open the Installer and follow the installation directions 

d. To verify, open terminal and run the following command to check Maven version: 
```bash 
mvn –v
```
e. Add the Maven directory to the operating system variable (PATH) that stores a list of directories where executable programs paths, using the following commands in terminal.  
- i. Open the Shell Configuration File, and enter user password when prompted 

```bash  
sudo nano ~/.zshrc
```
- ii. At the bottom, insert the following line to add Maven to PATH 
```bash 
export PATH="/usr/local/apache-maven/bin:$PATH" 
 ``` 

- iii. Exit file and save changes to File with commands:
```
control + x, y 
```

- iv. Apply the changes to .zshrc file 

```bash  
source ~/.zshrc
```

 

3. Setting up JDK 11.0.x 

a. Navigate to Oracle Java Downloads,  https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html, and scroll down to Java SE Development. 

b. Download any version of Java 11.0 for MacOS x64 DMG 
Installer and start the installation instructions 

c. Finish installation in the terminal 

d. Updated shell profile configuration file 
- i. Open the Shell Configuration File and enter user password when prompted 

```bash 
sudo nano ~/.zshrc 
``` 

- ii. At the bottom,  set the Java environment variables with the following commands  
```bash  
export JAVA_HOME=`/usr/libexec/java_home -v 11’ 
export PATH =$PATH:$JAVA_HOME/bin 
``` 

- iii. Exit file and save changes to File with commands: 
```text
control + x, y 
```

- iv. Apply the changes 
```bash 
source ~/.zshrc
```

e. To verify JDK Installation, run 
```bash  
java -version
```
Output:

```bash 
(base) Daniel@MDMC02DMAXBML7H Java % java --version 
java 11.0.23 2024-04-16 LTS    
Java(TM) SE Runtime Environment 18.9 (build 11.0.23+7-LTS-222)    
Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.23+7-LTS-222, mixed mode)
```


 
## Testing your Installation in terminal:  

Terminal command:
```bash 
python -c 'import imagej; ij = imagej.init("2.14.0"); print(ij.getVersion())' 
```

Output:
```bash
2.14.0  
```



## Footnotes
[^1] : Find more information about Anaconda [here](https://freelearning.anaconda.cloud/get-started-with-anaconda)