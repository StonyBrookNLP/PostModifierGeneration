# Post Modifier Generation Baseline

This is a baseline system for TTIC 2018 [Post-modifier Generation](https://sites.google.com/view/tticlanggen-2018/hackathon/post-modifier-generation) task.
This system is developed using [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py), an open-source neural machine translation system.

## Quickstart

## Step 1: Set OpenNMT path

You have to set up OpenNMT location in `util.py`
```python
OpenNMT_dir = "OpenNMT_location"
```

## Step 2: Preprocess the data

```bash
python pm_generation.py prepare -data_dir dataset_location -data_out prepared_data_location_and_prefix
```

This is using `preprocess.py` in OpenNMT system, and will genereate three following files:

* `(prefix).train.pt`: Pytorch file containing training data
* `(prefix).valid.pt`: Pytorch file containing validation data
* `(prefix).vocab.pt`: Pytorch file containing vocabulary data

## Step 3: Train the model

```bash
python pm_generation.py train -data data_prefix -model model_dir
```

This is using `train.py` in OpenNMT system

## Step 4: Generate Post-modifier
```bash
python pm_generation.py generate -data_dir dataset_location -dataset dataset_prefix  -model model_dir -out output_file
```

This is using `translate.py` in OpenNMT system

For more detailed information, pleaes refer [OpenNMT-py repository](https://github.com/OpenNMT/OpenNMT-py#quickstart) or [OpenNMT-py document](http://opennmt.net/OpenNMT-py).
