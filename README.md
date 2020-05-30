# 3DUNET-NeuronPreprocessing
Use 3DUNET on fMOST neuron imaging data to remove background noise.

## Step 1:
Use split2cubes.py to first split the input image stack into cubes of fixed size.
```bash
python3 split2cubes.py $input_image_stack_directory $output_cubes_directory
```

Required to install python 3.7.x.
Used packages:
numpy
h5py
pillow

## Step 2:

Acknowledgement: We directly used the code from https://github.com/wolny/pytorch-3dunet for processing 3D data. Here we only adjusted some parameters (hyper-parameters).

Some important directories:
1). "resources/", you can adjust training/testing hyperparameters in those two .yaml files.
2). "pytorch3dunet/3dunet/", trained model is there named "fMOST_neuron1_trained.pytorch".

More details please refer to the ReadMe text in the original repository.
