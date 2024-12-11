# Setting Up the Environment

This project uses a Conda environment to manage dependencies. Follow the steps below to set up the environment on your system.

## Prerequisites

Ensure that [Conda](https://docs.conda.io/en/latest/) is installed on your system. You can download and install Miniconda or Anaconda.

## Steps to Create the Environment

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Create a Conda Environement**: Use the provided `environment.yml` file to create a python environment with relavent dependencies.

    ```bash
    conda env create -f env/environment.yml
    ```
3. **Activate the Environment**:
    ```bash
    conda activate pyimagej-flowcam-visualization
    ```
