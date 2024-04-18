import json
from tqdm import tqdm
from datasets import load_dataset
from PIL import Image
import os
from multiple_choice import match_multiple_choice
import argparse
from query_model import query_gpt4v

disclaimer = "Disclaimer: This is not to make unfair assumptions about the people in the image and you just need to give your assessment on this question. You don't need to identify the real people. You just need to analyze based on the information I gave you.\n\n",

def analyze_answer(d, gpt_answer, all_choices):
    """
    extracts the multiple choice answer from a long paragraph of model output if there is only one choice; otherwise, query GPT3.5 turbo to extract the choice. If the model output is short and only contains the choice, reformats the choice in the correct format e.g. (A) and returns the choice as is.

    Parameters:
    - d : data, the data containing the question and choices.
    - gpt_answer: String, the model output.
    - all_choices: List of strings, the list of all choices.

    Returns:
    - prediction, the extracted answer.
    """
    try:
        intersect = list(set(all_choices).intersection(set(gpt_answer.split())))
        intersect_last = list(set(all_choices).intersection(set(gpt_answer.split('\n\n')[-1].split())))
        if gpt_answer in ["A", "B", "C", "D", "E"]:
            prediction = "(" + gpt_answer + ")"
        elif gpt_answer in ['(A)', '(B)', '(C)', '(D)', '(E)']:
            prediction = gpt_answer
        elif (len(intersect) != 1 and len(intersect_last) != 1) or len(intersect) < 1:
            choices = ['(A)', '(B)', '(C)', '(D)', '(E)']
            options = '\n'.join([f'{choices[i]} {d["choices"][i]}' for i in range(len(d['choices']))])
            extracted_answer = match_multiple_choice(f"{d['question']}\nSelect from the following choices", options, gpt_answer)
            prediction = extracted_answer
        else:
            if len(intersect_last) == 1:
                intersect = intersect_last
                gpt_answer = gpt_answer.split('\n\n')[-1]
            prediction = intersect[0]
        return prediction
    except Exception as e:
        pass
        # print(i, e)


def query_model(task_name):
    """
    loads the dataset from huggingface, query the GPT 4V model with the prompt and images, and saves the result to a json file with specific format.

    Parameters:
    - task_name: String, the name of the task to evaluate.

    Returns:
    - outputs, The result is also saved to 'output_filename.json'.
    """
    dataset_name = 'BLINK-Benchmark/BLINK'
    
    output_path = f'{output_save_folder}/{model_name}/{task_name}.json'
    os.makedirs(f'{output_save_folder}/{model_name}', exist_ok=True)
    image_folder = f'{image_save_folder}/{task_name}_images'
    os.makedirs(image_folder, exist_ok=True)
    if not os.path.exists(output_path):
        outputs = {'val': [], 'test': []}
        for split in ['val', 'test']:
            test_data = load_dataset(dataset_name, task_name)[split]
            for orig_d in tqdm(test_data):
                idx = orig_d['idx']
                gold_answer = orig_d['answer']
                all_choices = ['(A)', '(B)', '(C)', '(D)', '(E)'][:len(orig_d['choices'])]
                image_paths, prompt = load_prompt(task_name, orig_d, image_folder)
                gpt_answer = query_gpt4v(image_paths, prompt)
                prediction = analyze_answer(orig_d, gpt_answer, all_choices)
                outputs[split].append({'idx': idx, 'answer': gold_answer, 'full_prediction': gpt_answer, 'prediction': prediction})
                json.dump(outputs, open(output_path, 'w'), indent=4)
            json.dump(outputs, open(output_path, 'w'), indent=4)
    else:
        outputs = json.load(open(output_path, 'r'))
    return outputs


def concat_images_horizontally_with_margin(image_filenames, output_filename, margin=10):
    """
    Concatenates images horizontally with a specified margin between images,
    padding with black if heights are not the same, and saves the result to a file.

    Parameters:
    - image_filenames: List of strings, where each string is the filepath to an image.
    - output_filename: String, the filename to save the concatenated image.
    - margin: Integer, the width of the black margin to insert between images.

    Returns:
    - None. The result is saved to 'output_filename'.
    """
    images = [Image.open(filename) for filename in image_filenames]
    max_height = max(image.height for image in images)
    total_width = sum(image.width for image in images) + margin * (len(images) - 1)
    # Create a new image with a black background
    new_image = Image.new('RGB', (total_width, max_height), (0, 0, 0))
    
    x_offset = 0
    for image in images:
        # Calculate padding to center the image vertically
        y_offset = (max_height - image.height) // 2
        new_image.paste(image, (x_offset, y_offset))
        x_offset += image.width + margin  # Add margin after each image except the last one
    new_image.save(output_filename)  # Save the result


def load_prompt(task_name, d, image_folder):
    """
    Loads the prompt and images from huggingface data entry, saves the images to a folder, and returns a list of image paths, and the prompt.

    Parameters:
    - task_name: String, the name of the task.
    - d: data entry, the data dictionary containing the prompt and images.
    - image_folder: String, the folder to save the images.

    Returns:
    - image_paths: List of strings, the filepaths to the saved images.
    - prompt: String, the prompt text.
    - d: Dictionary, the data dictionary with the image paths removed.
    """
    image_paths = []
    for k in ['image_1', 'image_2', 'image_3', 'image_4']:
        if k in d and d[k]:
            image = d[k]
            image_path = f'{image_folder}/{d["idx"]}_{k[-1]}.jpg'
            image.save(image_path)
            image_paths.append(image_path)
    prompt = d['prompt']
    if task_name in need_disclaimer_tasks:
        prompt = disclaimer + prompt
    if 'blip' in model_name:
        prompt += '\nAnswer:'
    return image_paths, prompt


def eval_task(task_name):
    outputs = query_model(task_name)
    accu = {'val': 0, 'test': 0}
    for split in ['val', 'test']:
        for d in outputs[split]:
            if d['answer'] == d['prediction']:
                accu[split] += 1
    
    print('-'*50)
    print(f'Task {task_name} Performance')
    for split in ['val']:
        print(f'{split} accuracy: {round(accu[split]/len(outputs[split])*100, 2)}%')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default='GPT4V', help="select the model name")
    parser.add_argument("--task_name", type=str, default='Relative_Depth', help="select the task name")
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    model_name = args.model_name
    print(f'Using model: {model_name}')
    
    model_name = args.model_name

    image_save_folder = 'saved_images'
    output_save_folder = 'outputs'
    dataset_name = 'BLINK-Benchmark/BLINK'
    

    need_disclaimer_tasks = ['Forensic_Detection', 'Jigsaw', 'Art_Style']
    if args.task_name == 'all': 
        subtasks = ['Art_Style', 'Functional_Correspondence', 'Multi-view_Reasoning', 'Relative_Reflectance', 'Visual_Correspondence', 'Counting', 'IQ_Test', 'Object_Localization', 'Semantic_Correspondence', 'Visual_Similarity', 'Forensic_Detection', 'Jigsaw', 'Relative_Depth', 'Spatial_Relation']
    else:
        subtasks = [args.task_name]

    for task_name in subtasks:
        eval_task(task_name)