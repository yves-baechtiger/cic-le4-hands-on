FROM jupyter/datascience-notebook:latest

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y graphviz git

# Switch back to Jupyter user
USER jovyan

# Use Mamba for package management (installed by default in jupyter/datascience-notebook)
RUN mamba install -y \
    python=3.11 \
    jupyterlab=4 \
    numpy \
    scipy \
    bokeh \
    dask \
    dask-labextension \
    dask-ml \
    distributed \
    matplotlib \
    pandas \
    python-graphviz \
    ipycytoscape \
    pyarrow \
    s3fs \
    zarr \
    pooch \
    xarray

# Register the Conda environment as a Jupyter kernel
RUN python -m ipykernel install --user --name dask-tutorial --display-name "Python (Dask Tutorial)"

# Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
