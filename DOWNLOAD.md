Dataset **Human Parts** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMzUyOV9IdW1hbiBQYXJ0cy9odW1hbi1wYXJ0cy1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJYU2Y2Rm9leWJWM05iSXNNQWFQcGlQSUJ3c2duTlFzeTZhdVdzL2gwOWdBPSJ9?response-content-disposition=attachment%3B%20filename%3D%22human-parts-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Human Parts', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://drive.google.com/file/d/1L7oxFqRi63APVi-ffeK3L7dF_qTkZmbW/view?usp=sharing).