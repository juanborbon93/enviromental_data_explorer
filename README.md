# L2 Enviro Dataset Explorer
A web app designed to make it easier to navigate large environmental sample datasets. letting the user filet results based on calculated haversine distance. 

## Installation

### 1. Install Miniconda:
- [click here](https://docs.conda.io/en/latest/miniconda.html) to download the miniconda software. Miniconda is a python package manager that we will use to set up the software dependencies that our software needs to run. 

### 2. Download this repository:
- There are multiple ways to do this. The simplest way can be found under "Method 1" in [this guide](https://www.wikihow.com/Download-a-GitHub-Folder)
- Unzip the contents of the repository

### 3. Open the directory in a comand line interface (CLI)
- Open the command line interface of your system
- Find the location of the folder where the code resides
    - This folder should contain a folder called "dash_app"
- type the following command:
```
cd <THE PATH TO THE PROJECT FOLDER>
```
- To check that you are now in the right directory, type "ls" into the CLI and you should see "dash_app" as one of the listed outputs.

### 4. Set up the application environment:
- type the following command to create a new environment containing all the needed dependencies
```
conda env create -f environment.yml
```
- The installation process may take a few minutes. After completed, type the following command to switch into your new environment.
```
conda activate l2
```
### 5. Run the app:
- start the app by typing the following command
```
python dash_app/index.py
```
- navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to use the app
