# Dask Tutorial 

## ✏️ Note
This repository contains Jupyter notebooks from the [dask-tutorial](https://github.com/dask/dask-tutorial/tree/main). The Dockerfile has been updated to a modern version for compatibility.

The original repository is licensed under the **BSD 3-Clause License**, which allows modification, distribution, and commercial use while requiring attribution and prohibiting endorsement without permission. This repository retains the same license.

---

## ⚙️ Set-Up

Got to the `02_hands_on` folder and run:
```bash
docker build -t <your_image_name> .
```

After the docker image has been built run:
```bash
docker run -it \
  -p 8888:8888 \
  -p 8787:8787 \
  -v <your/local/path/to>/cic-le4-hands-on:/home/jovyan/cic-le4-hands-on \
  my-dask-image

```

Jupyter lab will start and provide and URL where you will find your Lab. 

If you create a new file in your Lab make sure to use the `Python (Dask Tutorial)` Kernel.