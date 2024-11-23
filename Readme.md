# Doc2Pdf

The is the main service which utilizes the `unoserver` to convert the doc files to pdf files.

There is 1 route:

- /encrypt - which takes a pdf file, encrypts it and sends it back to the Converter-Service

Additionally, **password** can be passed to this endpoint to encrypt the pdf file.

## Running the app

#### Steps to run the app:

- run `./encryption_script.sh`

## Running the stack

To run the whole stack, use this [Dockerfile](https://github.com/Rapid-Converter/Deployments/blob/master/docker-compose.yml).
`docker compose up -d --build`

## Technologies/Libraries Used

- Python
- FastAPI
- unoconv
