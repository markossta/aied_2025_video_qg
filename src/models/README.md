# Models  

This folder contains the modified inference code for the four models used in the question generation process. The provided scripts allow question generation without the need for a GUI.  

## Pre-Trained Models  
To use the inference scripts, you need to download the pre-trained models from the respective GitHub repositories of the original authors. These models are required both for inference and, in the case of **PG-Video-LLaVA** and **Video-LLaMA**, for fine-tuning. 

Github-Repositories:
[Video-LLaVA](https://github.com/PKU-YuanGroup/Video-LLaVA)
[PG-Video-LLaVA](https://github.com/mbzuai-oryx/Video-LLaVA)
[Video-LLaMA](https://github.com/DAMO-NLP-SG/Video-LLaMA)


For Mistral-7B we used the [HugginFace version](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
## Fine-Tuning  
Fine-tuning was conducted for **PG-Video-LLaVA** and **Video-LLaMA** using the pre-processed LearningQ dataset. The original training code from the respective repositories was used for this process.

For **Video-LLaMA**, additional training data was prepared to ensure compatibility with the fine-tuning process (see folder `data_processing/`).  

## Environment Setup  
Since the models have different dependencies, it is recommended to use a  **Conda environment** for each model to avoid conflicts.  

The installation instructions and required dependencies for each model can be found in their respective original GitHub repositories. Follow those guidelines to set up the correct environment before running inference or fine-tuning.

## Recommended Placement of Inference Code  
For proper execution and optimal organization, here are the recommended locations for the inference code for each model (can be used for zero-shot, fine-tuned, ablation study (some lines need to be commented/uncommented as in the code described):

- **Video-LLaVA**: Place the inference code directly in the main directory of the original GitHub project.
- **PG-Video-LLaVA**: Place the inference code in the `video_chatgpt`folder of the original GitHub project.
- **Video-LLaMA**: Place the inference code directly in the main directory of the original GitHub project.
- **Mistral-7B**: This model uses the **transformers** library, so the placement of the inference code is not critical. You can place it wherever is most convenient.  
