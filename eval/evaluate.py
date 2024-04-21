import json
import os


def get_prediction_file(split, model_name):
    """
    Combine the task-specific prediction files for a model on split into one single final-prediction json file.

    Parameters:
    - split: String, the split to evaluate on.
    - model_name: String, the name of the model.

    Returns:
    - save_path, the path to the saved final prediction json file.
    """
    save_path = f'{split}_predictions/{model_name}.json'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    saved = {}
    for task_name in subtasks:
        output_path = f'{output_save_folder}/{model_name}/{task_name.replace("_", " ")}.json'
        outputs = json.load(open(output_path, 'r'))[split]
        for d in outputs:
            saved[d['idx']] = d['prediction']
    json.dump(saved, open(save_path, 'w'), indent=4)
    return save_path


def eval_prediction(split, model_name):
    """
    Evaluate the model on the split and return the accuracy for all tasks and also total accuracy.

    Parameters:
    - split: String, the split to evaluate on.
    - model_name: String, the name of the model.

    Returns:
    - accu_by_task, the accuracy for all tasks and also total accuracy (averaged over all subtasks).
    """
    accu_by_task = {}
    task_numbers = {}
    errors = {}
    for task_name in subtasks:
        accu_by_task[task_name] = 0
        task_numbers[task_name] = 0
        errors[task_name] = []
    answer_file_path = f'{split}_answers.json'
    prediction_file_path = f'{split}_predictions/{model_name}.json'
    answers = json.load(open(answer_file_path, 'r'))
    predictions = json.load(open(prediction_file_path, 'r'))
    for idx, gold_answer in answers.items():
        task = '_'.join(idx.split(split)[1][1:].split('_')[:-1])
        task_numbers[task] += 1
        if idx in predictions and predictions[idx] == gold_answer:
            accu_by_task[task] += 1
        else:
            errors[task].append(idx)

    average_accu = 0
    for task in subtasks:
        accu_by_task[task] = accu_by_task[task] / task_numbers[task]
        average_accu += accu_by_task[task]
    average_accu = average_accu / len(subtasks)
    accu_by_task["Total"] = average_accu 
    print(f'Average Accuracy of model {model_name} on BLINK split {split} over all tasks is {round(100 * average_accu, 2)}%')
    return accu_by_task

if __name__ == '__main__':  
    dataset_name = 'BLINK-Benchmark/BLINK'
    output_save_folder = 'outputs'

    # models that we experimented on
    model_names = [
                    'MiniGPT-4-v2', 'flamingov2', 'instructblip_7b', 'instructblip_13b',
                    'llava-internlm2-7b', 'Yi_VL_6B', 'Yi_VL_34B',
                    'llava-v1.5-7b-xtuner', 'llava-v1.5-13b-xtuner', 'cogvlm-chat', 
                    'llava_v1.5_7b', 'llava_v1.5_13b', 'llava-v1.6-34b',
                    'QwenVLMax', 'GeminiProVision', 'GPT4V', 'OPUS'
                    ]
    # save to a output path with model_name.json, replace with custom model name
    model_name = model_names[-2]
    subtasks = [
        'Visual_Similarity', 'Counting', 'Relative_Depth', 'Jigsaw', 'Art_Style', 'Functional_Correspondence', 'Semantic_Correspondence', 'Spatial_Relation', 'Object_Localization', 'Visual_Correspondence', 'Multi-view_Reasoning', 'Relative_Reflectance', 'Forensic_Detection', 'IQ_Test'
        ]

    split = 'val'
    get_prediction_file(split, model_name)
    eval_prediction(split, model_name)
