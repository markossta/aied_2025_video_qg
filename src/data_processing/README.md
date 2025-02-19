# Data Processing  

This folder contains scripts for preparing the LearningQ dataset before using it for question generation.  
Before running any scripts, please make sure to install the required dependencies.

## Installation  
For optimal performance, especially when using PyTorch-based models, it is recommended to install Torch with CUDA support.
Run the following command to install the remaining necessary dependencies:  

```pip install -r requirements.txt```

## Processing Steps
The scripts must be executed in the following order to obtain the final processed data:  

1. `make_khan_video_list.py`  
- Uses the original LearningQ data related to Khan Academy videos.  
- Extracts video information from `predicted_video_questions` to generate a list of YouTube links for Khan Academy videos (`yt_khan_links.txt`).  

2. `download_videos.py`  
- Downloads videos from YouTube using LearningQ’s `yt_teded_links.txt` (TED-Ed videos).  
- The same script should be modified to also process Khan Academy videos (replace "teded" with "khan").  
- Videos will be saved in `data/learningq_videos/`.  
- Generates log files for videos that couldn't be downloaded:  
  - `restricted_videos_teded.txt`  
  - `restricted_videos_khan.txt`

3. `filter_ignored_videos.py`  
- Uses LearningQ data and the list of undownloadable videos to create a refined set of questions linked to available videos.  
- Outputs:  
  - `teded_filtered_questions.txt`  
  - `khan_filtered_questions.txt`  

4. `dataset_splitter.py`  
- Splits the filtered question dataset into training, validation, and test sets.  
- Outputs:  
  - `khan_datasplit.txt`  
  - `teded_datasplit.txt`

5. `make_transcripts.py`  
- Generates speech transcripts for the downloaded videos.  
- Run once for **Khan Academy** videos and again for **TED-Ed** videos (replace "khan" with "teded" in the script).  
- Saves transcripts in `data/learningq_videos/`
