# XMeme Backend
This is the backend for the XMeme Project built as part of the CWoD. Build using Flask (Flask Restplus) and SQLalchemy. Sqlite is used for local testing purposes and postgrsql for production build.
 ## Setting up a development environment
* It is assumed that `git`, `python` and `pip` are installed.
* Clone the repo:
`git clone https://github.com/iamsdas/xmeme-backend && cd xmeme-backend`
* Install requirements:
`pip install -r requirements_dev.txt`
* Run using:
`python -u app.py`
### Alternate Docker method:
* It is assumed that `docker` is installed.
* It is assumed that `$user` is a part of the `docker group` (if not, use `sudo` before the commands).
* Build docker image:
`docker build -t xmeme .`
* Run using:
`docker run --net="host" --volume $PWD/db:/app/db xmeme`
* Note: it is neccessary to use this volume as otherwise database will be lost after stopping server.
## Usage
* By default server should start at `http://localhost:8081`
* Test by executing:
`curl --location --request GET 'http://localhost:8081/memes'`
* This should result in an empty array
