# BLINK
This repo contains evaluation code for the paper "BLINK: Multimodal Large Language Models Can See but Not Perceive"

[**🌐 Homepage**](https://zeyofu.github.io/blink/) | [**🤗 Dataset**](https://huggingface.co/datasets/BLINK-Benchmark/BLINK) | [**🤗 Paper**](?) | [**📖 arXiv**](?) | [**GitHub**](https://github.com/zeyofu/BLINK_Benchmark) | [**Evaluation**](?)



This repo contains the evaluation code for the paper "[BLINK: Multimodal Large Language Models Can See but Not Perceive](arxiv?)"

## 🔔News

- **🔥[2024-04-17]: Our evaluation server for test set is now availble on [EvalAI](https://eval.ai/web/challenges/challenge-page/2179/overview). We welcome all submissions and look forward to your participation! 😆**

## Introduction
We introduce **BLINK**, a new benchmark for multimodal language models (LLMs) that focuses on core visual perception abilities not found in other evaluations. Most of the **BLINK** tasks can be solved by humans “within a blink” (e.g., *relative depth estimation, visual correspondence, forensics detection, and multi-view reasoning*). However, we find these perception-demanding tasks cast significant challenges for current multimodal LLMs because they resist mediation through natural language. **BLINK** reformats 14 classic computer vision tasks into 3,978 multiple-choice questions, paired with single or multiple images and visual prompting. While humans get 95.100% accuracy on average, **BLINK** is surprisingly challenging for existing multimodal LLMs: even the best-performing GPT-4V and Gemini achieve accuracies of 51.32% and 45.46%, only 13.23% and 7.47% higher than random guessing, indicating that such perception abilities have not “emerged” yet in recent multimodal LLMs. Our analysis also highlights that specialist CV models could solve these problems much better, suggesting potential pathways for future improvements. We believe **BLINK** will stimulate the community to help multimodal LLMs catch up with human-level visual perception.

![Alt text](image.png)

## Dataset Creation

BLINK is created to challenge multimodal models on hollistic visual perception abilities with tasks inherited from classic computer vision problems, stimulating future development of multimodal LLMs that achieve human-level visual perception. Please refer to our huggingface [**🤗 Dataset**](https://huggingface.co/datasets/BLINK-Benchmark/BLINK) for more details.

## Evaluation
Please refer to our [eval](eval)
 folder for more details.

## 🏆 Mini-Leaderboard
| Model                      | Val (1,973) | Test (2,005) |
|----------------------------|:-----------:|:------------:|
| Human                      |     95.7    |     95.7     |
| Gemini Pro                 |     45.4    |     45.5     |
| Qwen-VL-MAX                |     41.1    |     41.1     |
| Claude 3 Opus              |      ---    |      --      |
| GPT-4V(ision)              |     51.1    |   **51.3**   |
| Yi-VL-6B                   |     39.1    |     40.8     |
| Yi-VL-34B                  |     41.9    |     42.6     |
| LLaVA-1.5-7B               |     36.5    |     38.6     |
| LLaVA-1.5-13B              |     41.8    |     41.4     |
| LLaVA-1.6-34B*             |     46.4    |     45.4     |
| CogVLM                     |     40.5    |     40.4     |
| LLaVA-v1.5-7B-xtuner       |     40.1    |     40.1     |
| LLaVA-v1.5-13B-xtuner      |     42.1    |     41.2     |
| LLaVA-internLM2-7B         |     38.0    |     35.8     |
| InstructBLIP-7B            |     39.7    |     38.7     |
| InstructBLIP-13B           |     42.1    |     39.7     |
| MiniGPT-4-v2-7B            |     34.9    |     33.9     |
| OpenFlamingo2-9B           |     36.4    |     35.0     |
| Random Choice              |     38.1    |     38.1     |


🎯 **We have released a full suite comprising 1,973 validation samples, the prompt we used, and their [model predictions](outputs). However, the 2,005 test questions are available without their answers.** You can submit your model's predictions for the **test set** on **[EvalAI](?)**.

## Disclaimers
Blink makes use of data from existing image datasets, and does not cover all the visual perception abilities in the wild. For the forensics detection task, we manually collected images that are publicly available from online search. We have made every effort to ensure that the images included in this paper are used in accordance with applicable copyright laws and are properly credited. However, if you are the copyright owner of any image included in our work and believe that its use conflicts with your licensing agreements, please [contact](#contact) us directly. We are committed to addressing any legitimate concerns promptly.

## Contact
- Xingyu Fu: xingyuf2@seas.upenn.edu
- Yushi Hu:  yushihu@uw.edu
- Wei-Chiu Ma:    weichiu@cornell.edu
- Ranjay Krishna: ​ranjay@cs.washington.edu

## Citation

**BibTeX:**
```bibtex
...
```
