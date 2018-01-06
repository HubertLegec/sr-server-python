# FILE SERVER

Project for Distributed Systems course 
at the Faculty of Electronics and Information Technology of Warsaw University of Technology.

## Project description

## How to run
### Requirements
There are two possible options to run the project:
* Standalone mode
  
  To run project this way following requirements needs to be fulfilled:
  * Python 3.6 installed
  * Packages from ```requirements.txt``` installed
* Docker mode

  The only required thing is Docker installed on your system.

### Standalone mode
* Go to ```server``` directory
* Run ```python run.py```
Server should be available under ```localhost:4200``` by default. 
If uou want to change default port or run more than one instance you can modify ```config.json``` file or add start params:
* ```-c``` custom path to config file
* ```-s``` number that represents server config index in ```config.json``` file
* ```-d``` run in debug mode

### Docker mode
* Go to root project directory
* Run ```docker-compose up``` command
Server should be available under ```localhost:4200```