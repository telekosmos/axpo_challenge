# axpo_challenge

Develop a tool that will help us visualize and analyze our time series.

## Develop

Clone the repo.

We use `pyenv` and `poetry` to manage python versions and project depencies and environments, but a _flat_ `requirements.txt` is provided as well. You should create a virtual environment (whatever way you like more) for this project to isolate dependencies, activate the virutal environment and the run `pip install -r requirements.txt` or `poetry install` depending on your tastes.

## Run

Clone this repo.

Create the docker image by typing `docker buildx build -t <image_tag> .`.

Run the image as `docker run -p 8501:8501 --name <container-name> <image_tag>`.

Access to the UI by typing in your browser `http://localhost:8501/`.

## Considerations

Use [streamlit](http://streamlit.io) as UI framework of choice. Suitable for prototyping and showcasing, not for full production or highly interactive applications. Allows to use python and take advantage of python data tools (pandas, numpy, polars, ...)

_Time series_ (_measurements_) data contained different series for different signals. Data points size for the signals were largely different, ranging from few thousands to tens of thousands, which raises a challenge to _plot_ two or more series (as requested) in the same chart with large different data points size for the same time range. To _mitigate_ this one, a _dynamic downsampling_ function was put in place to downsample to a max of 5000 data points the series (if needed) without losing significant details.

Also, downsampling is needed as plotting a huge number of data points in a chart can get the visualization to become slower or unable depending on your system capabilities.

Data series also have _gaps_. This one wasn't addressed and techniques to mitigate those gaps (fi needed) is noted to be investigated.

The _dispersion_ of the data around the mean is quite similar for all signals but the mean of the distance between consecutive points is very different given the amount of data points for each serie.
