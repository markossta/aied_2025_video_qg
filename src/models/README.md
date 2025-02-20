# Models  

This folder contains the modified inference code for the four models used in the question generation process. The provided scripts allow question generation without the need for a GUI.  

## Pre-Trained Models  
To use the inference scripts, you need to download the pre-trained models from the respective GitHub repositories of the original authors. These models are required both for inference and, in the case of **PG-Video-LLaVA** and **Video-LLaMA**, for fine-tuning. 

## Fine-Tuning  
Fine-tuning was conducted for **PG-Video-LLaVA** and **Video-LLaMA** using the pre-processed LearningQ dataset. The original training code from the respective repositories was used for this process.

For **Video-LLaMA**, additional training data was prepared to ensure compatibility with the fine-tuning process (see folder `data_processing/').  

## Environment Setup  
Since the models have different dependencies, it is recommended to use a  **Conda environment** for each model to avoid conflicts.  

The installation instructions and required dependencies for each model can be found in their respective original GitHub repositories. Follow those guidelines to set up the correct environment before running inference or fine-tuning.

## Recommended Placement of Inference Code  
For proper execution and optimal organization, here are the recommended locations for the inference code for each model:

- **Video-LLaVA**: Place the inference code directly in the main directory of the original GitHub project.
- **PG-Video-LLaVA**: Place the inference code in the `video_chatgpt`folder of the original GitHub project.
- **Video-LLaMA**: Place the inference code directly in the main directory of the original GitHub project.
- **Mistral-7B**: This model uses the **transformers** library, so the placement of the inference code is not critical. You can place it wherever is most convenient.  
