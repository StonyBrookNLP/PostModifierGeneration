# Post Modifier Generation Baseline

This is a baseline system for TTIC 2018 [Post-modifier Generation](https://sites.google.com/view/tticlanggen-2018/hackathon/post-modifier-generation) task.
This system is developed using [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py), an open-source neural machine translation system.

## Prerequisite

You will need [Post-modifier dataset](https://github.com/StonyBrookNLP/PostModifier) and [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py) to run the system.

## Quickstart

### Step 1: Set OpenNMT path

You have to set up OpenNMT location in `util.py`
```python
OpenNMT_dir = "OpenNMT_location"
```

### Step 2: Preprocess the data

```bash
python pm_generation.py prepare -data_dir dataset_location -data_out prepared_data_location_and_prefix
```

This is using `preprocess.py` in OpenNMT system, and will genereate three following files:

* `(prefix).train.pt`: Pytorch file containing training data
* `(prefix).valid.pt`: Pytorch file containing validation data
* `(prefix).vocab.pt`: Pytorch file containing vocabulary data

As a seq2seq model, the model takes source sequences and target sequences. In our task, the source sequences will be setences with wikipedia entities and the target sequences will be post-modifiers.

```
Example:

-Source(input)
Haitham al-Haddad is one preacher under scrutiny according to Whitehall officials . <rel> instance of \
</rel> <value> human </value> <rel> sex or gender </rel> <value> male </value> <rel> educated at </rel> \ 
<value> SOAS, University of London </value> <rel> occupation </rel> <value> Islamic studies scholar </value>

-Target(output)
an Islamic scholar
```

### Step 3: Train the model

```bash
python pm_generation.py train -data data_prefix -model model_dir
```

This is using `train.py` in OpenNMT system. The model consists of a 2-layer biLSTM with 500 hidden units on the encoder and a 2-layer LSTM with 500 hidden units on the decoder.
Attention is used the *general* scheme, which is a multipicative global attention. 

### Step 4: Generate Post-modifier
```bash
python pm_generation.py generate -data_dir dataset_location -dataset dataset_prefix  -model model_dir -out output_file
```

This is using `translate.py` in OpenNMT system. The setting remains the same as the default (beam size = 5).

For further information, pleaes refer [OpenNMT-py repository](https://github.com/OpenNMT/OpenNMT-py#quickstart) or [OpenNMT-py document](http://opennmt.net/OpenNMT-py).

### Pretrained model

You can download pretrained model form [here](https://drive.google.com/file/d/1FvbA7L9T2CfhaRWv1_9hCDsKW8Jq_1ci/view?usp=sharing)
