# path2path


## fresh installation

1) install miniconda3 from

2) create conda environment and install library.
    This command assumes you are on macos - replace the tensorflow
    wheel path on different environments

``` bash
conda create -n path2path-env python=3.6
source activate path2path-env
pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.6.0-py3-none-any.whl
pip install --upgrade flask flask_restful rdp scipy matplotlib requests
```

3) acquire wheel from github releases

```bash
pip install path/to/wheel
```

## upgrade installation

```bash
pip uninstall path2path
pip install path/to/wheel
```

## usage

1) acquire a trained model

2) Start a crserver

```bash
source activate path2path-env
crserver /path/to/trained/model
```

3) curl in JSON calls from the command line

```bash
curl --data-binary "@Gesture-20180203-115827.json" http://localhost:5000/tfgen > ~/response.json
```

4) or post from another program

```python
TBD
```