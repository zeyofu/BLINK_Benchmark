# Evaluation Guidelines
We provide detailed instructions for evaluation. 
To execute our evaluation script, please ensure that the structure of your model outputs is the same as ours.

Specifically, we provide 
- An example model inference file including data loading and subtask-specific output saving.
- The evaluation code.

## Saved Baseline Predictions
For fostering future research, **we release the full suite of [model predictions](saved_outputs) on both validation and test sets for the baselines tested in our paper.** 

Notice that for the data entry in model predictions such as [this](eval/saved_outputs/GPT4V/Counting.json), ```full_prediction``` means the raw model output before answer extraction, and ```prediction``` means the extracted answer choice that is used for final evaluation.


## Data Loading, Model Inference, and Output Saving
We provide one example file `test_benchmark.py` to test the benchmark for your reference. 
Basically, it
- loads the dataset
- conducts model inference (supported in `query_model.py`)
- extracts the answer choices from model outputs (supported in `multiple_choice.py`)
- saves subtask-specific outputs to an output folder.

`test_benchmark.py` only supports the model GPT4V(ision). Feel free to replace [`model_generate_funcs`](https://github.com/zeyofu/BLINK_Benchmark/blob/main/eval/test_benchmark.py#L167) for any new model that you'd like to test on. 

Example call:
```
python test_benchmark.py --model_name GPT4V --task_name all
```
where `task_name` is either `all` (evaluates on all subtasks), or one of the subtasks in: `['Art_Style', 'Functional_Correspondence', 'Multi-view_Reasoning', 'Relative_Reflectance', 'Visual_Correspondence', 'Counting', 'IQ_Test', 'Object_Localization', 'Semantic_Correspondence', 'Visual_Similarity', 'Forensic_Detection', 'Jigsaw', 'Relative_Depth', 'Spatial_Relation']`.

### Output folder structure
Saved model output folder includes task-specific json files, as in the following structure:

```
└── model_name (e.g. GPT4V)
    ├── sub-task_name.json (e.g. Counting.json)
    └── sub-task_name.json (e.g. Art_Style.json)
    ...
```

where each `sub-task_name.json` file follows the format:
```
{
    "val": [
        {
            "idx": "val_Art_Style_1",
            "answer": "(A)",
            "full_prediction": "The first image is painted in a style that is characterized by visible brushstrokes, a vibrant use of color, and a focus on capturing the essence or impression of the subject rather than detailed realism...\n\nTherefore, the second image shares the same style as the reference image, which is Impressionism.",
            "prediction": "(A)"
        },
        ...
    ],
    "test": [
        {
            "idx": "test_Art_Style_1",
            "answer": "hidden",
            "full_prediction": "The first image is representative of Cubism, an art movement where objects are broken up, analyzed, and re-assembled in an abstracted form...\n\nTherefore, the image that shares the same style as the reference image (Cubism) is:\n\n(A) the second image.",
            "prediction": "(A)"
        },
        ...
    ]
}
```

*Notice that we release the model predictions in [saved_outputs](saved_outputs) for the baselines tested in our paper.*

## Evaluation

We use `evaluate.py` to turn the task-specific outputs into *one single final prediction file*, and evaluate the file for task-specific and total accuracies. 

The final prediction file is in the following format:
```
{
    "val_Art_Style_1": "(A)",
    "val_Spatial_Relation_29": "(B)",
    ...
}
```

*Notice that the final prediction files for the baselines tested in our paper are released at [saved_val_predictions](saved_val_predictions) and [saved_test_predictions](saved_test_predictions).*

### Validation Set Evaluation
Example call:
```
python evaluate.py
```
Feel free to change `model_name` to your custom model name.

### Test Set Evaluation
You can submit your model's final prediction file for the **test set** to **[EvalAI](https://eval.ai/web/challenges/challenge-page/2287/overview)**.
