# Folder synchronizator

## installation

```bash
pip3 install requirements.txt
```
## usage

```bash
python3 app.py
```
application have to be run with parameters:
* -si or --synchronization-interval  -> Synchronization interval in HH:MM:SS format
* -sf --source-folder -> Source folder path for one-way synchronization 
* -rf --replica-folder -> Replica folder path for one-way synchronization
* -lf --log-file -> Log file path. 