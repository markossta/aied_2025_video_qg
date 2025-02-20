# Evaluation  

This folder contains Python scripts for various evaluation calculations related to the generated output of the models.  

## Installation  
Before running the scripts, make sure to install the required dependencies:  

```bash
pip install -r requirements.txt
```

## Evaluation Scripts
### `alpha.py`  
Calculates **Krippendorff's Alpha** to measure inter-annotator agreement.  

### `distribution.py`  
Analyzes the **final manual evaluation** (collaborative discussion) and calculates the percentage distribution of:  
- **Relevance**  
- **Answerability**  
- **Levels of Understanding** (Bloom’s Taxonomy)  

### `embed_sim_evaluator.py`  
Computes values for the **ICD metric** (requires a JSON file containing the cosine similarities of questions to transcripts).

### `evaluate_question_statistics.py`  
Generates statistics for a selected model/approach, including:  
- **Distribution of question words**  
- **Percentage of questions, statements, and empty outputs**  
- **Readability and sentence length**  

**Note:** The file path for TED-ED and Khan Academy outputs must be specified in the script.  

### `standard_metrics_calculation.py`  
Computes **ROUGE-L** and **BERTScore** for a selected model/approach.  

**Note:** The file path for TED-ED and Khan Academy outputs must be specified in the script.  

### `video_length_calculator.py`  
Calculates video length statistics for the downloaded videos.  
