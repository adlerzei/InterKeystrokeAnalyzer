# InterKeystrokeAnalyzer

This program serves to analyze the keystroke latencies, that are recorded by a Bluetooth sniffer. In this repository, methods can be found to generate the transition array, the observation array and the observation sequence from the recorded data. Furthermore, three different implementations of the n-Viterbi algorithm can be found. Finally, some methods to plot interesting data features are included. 

## Requirements

1. A Python interpreter (recommended version 3 or higher)

## Dependencies

To run this program, you need to install the following Python libraries:

  * [numpy](https://pypi.org/project/numpy/)
  * [scipy](https://pypi.org/project/scipy/)
  * [matplotlib](https://pypi.org/project/matplotlib/)
  * [tikzplotlib](https://pypi.org/project/tikzplotlib/)
  
### Installation

These packages can be installed by using your favorite packet manager. For instance, if you use [pip](https://pip.pypa.io/en/stable/), just run the following command:

```shell
pip install numpy scipy matplotlib tikzplotlib
```

## Usage

In the following, sample instructions are given to execute the relevant parts of the program. Sample code, how the program can be used, can be found in the file 
 
 * **analyzer.py**
  
where the complete training and classification process is illustrated. This file contains two debug functions, to verify the correctness of the implementations of the Viterbi algorithm. Furthermore, a function for executing the complete training and classification process is included. Additionally, it contains several sample calls to plot the data.

To execute the complete process, execute the following line:

```python
run(user_id="9963", password_task_id="5", password_to_classify="s4ci", password_id=1, n=5, parallel=False, with_dict=True)
```

As it can be seen, the function expects several parameters:
  * **user_id**: The id of the user, whose data shall be classified
  * **password_task_id**: The task id, from which the data is recorded. Type ```"4"``` for pseudo-randomly generated passwords and ```"5"``` for passwords that are generated completly random.
  * **password_to_classify**: The password of which the recorded data is to be used as the observation sequence.
  * **password_id**: The input number of the recording. Choose a value between 1 and 5.
  * **n**: The number of outputs, that should be generated.
  * **parallel** (optional): Indicates, whether the parallelized implementation should be used or not. Default is ```parallel=False```.
  * **with_dict** (optional): Indicates, whether the numpy implementation or the standard dictionary implementation should be used. Default is ```with_dict=True```.

### Configuration

Before the process can be started, a few configurations can be adjusted. This can be done in the file config.py. The most important thing is to change the value of

  * **data_base_folder**
  
to your local data base folder.

### Hidden Markov Model

All methods that organize the recorded data as a HMM, including the computations of the transition and observation arrays can be found in the following two classes:

  * **KeyPairAnalyer (key_pair_analyzer.py)**: Generates the observation array and the transition array from the training data.
  * **PasswordAnalyzer (password_analyzer.py)**: Generates the observation sequence from the test data.
  * **utils.py**: Contains several helper functions.
  
A sample usage of this classes and methods can be taken from the file analyzer.py.

### n-Viterbi Algorithm

To execute the classification process, the follwing files can be used:

  * **viterbi.py**: Contains methods for all three implementations of the n-Viterbi algorithm as well as implementations of a normal Viterbi algorithm.
  * **MaxTransitionList (max_transition_list.py)**: Stores the best n transitions.

A sample usage of this classes and methods can be taken from the file analyzer.py.

### Plots

The repository contains several methods for plotting the data. These methods are contained in the following files:

  * **key_interval_analyzer.py**
  * **keystroke_analyzer.py**
  * **results_plotter.py**

A sample usage of this methods can be taken from the file analyzer.py.

### Misc

In addition to the files names above, the repository includes the following files:

  * **FileHandler (file_handler.py)**: Provides methods for the file handling, which includes the reading and writing of files.
  * **key_pair_generator.py**: Generates a list of all key pairs that include upper-case characters and are recorded during the data study.
 
 A sample usage of this classes and methods can be taken from the file analyzer.py.

