# Data  

This folder is structured to organize and store the required data for the project.  

## Folder Structure  

### `learningq_questions/`  
Contains processed question data for use in the experiments.  

To generate additional necessary files, refer to the scripts in `src/data_processing`.  
The original LearningQ dataset is required and should be placed in this directory as `learningQ/`, where it will be used for pre-processing.  

### `learningq_videos/`  
This folder stores:  
- **Downloaded videos** (processed using the provided python scripts in `src/data_processing`).  
- **Generated transcripts** from the videos (python script in `src/data_processing`) .  

### `manual_evaluation/`  
Contains the data from the **manual evaluation** process, including:  
- **Independent evaluations** from both annotators (each with a file for Khan Academy and TED-ED).  
- **Final collaborative evaluations** (one for Khan Academy, one for TED-ED).  

## Additional Data Availability  
If you are interested in accessing **fine-tuned models**, **cosine similarity calculations** (e.g. questions to transcripts similarity) and **model-generated outputs**, please contact the author. These files are too large to be included in this repository.  

