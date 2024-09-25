# axpo_challenge

## Develop

Clone the repo.

We use `pyenv` and `poetry` to manage python versions and project depencies and environments, but a _flat_ `requirements.txt` is provided as well. You should create a virtual environment for this project to isolate dependencies, activate the virutal environment and the run `pip install -r requirements.txt` or `poetry install` depending on your tastes.

## Run

Clone this repo.

Create the docker image by typing `docker buildx build -t <image_tag> .`.

Run the image as `docker run -p 8501:8501 <image_tag>`.



