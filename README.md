# Additional Information for 2025 AIED - Enhancing the Learning Experience: Using Vision-Language Models to Generate Questions for Educational Videos
This repository contains additional information about the AIED'25 submission #4602 titled **"Enhancing the Learning Experience: Using Vision-Language Models to Generate Questions for Educational Videos"**.
## Manual Evaluation
Since the detailed evaluation of the individual questions is very large, it is provided here as a excel files (evaluation folder).

Each table includes the following details: video ID, video link (YouTube), model used, approach applied, prompt used, generated output, whether it is a question (yes/no), and our evaluation categories: _Relevance_ (yes/no), _Answerability_ (yes/no), and _Bloom's Taxonomy Level_ (Remembering, Understanding, Applying, Analyzing, Evaluating, Creating). _Bloom's Taxonomy Level_ is also referenced as _Levels of understanding_ in our submission.

We evaluated the following models: _Mistral-7B_, _Video-LLaVA_, _PG-Video-LLaVA_, and _Video-LLaMA_. For the first two models, we used the zero-shot approach, as they serve as baselines due to their mono-modal function. For the other two models, we analyzed zero-shot and fine-tuned approaches, as well as the isolated modality for the fine-tuned models (audio-only and frames-only).

For a better understanding of Bloom's Level we are providing the following table:
| **Level**       | **Description**                                                                                  | **Example**                                                                                                  |
|-----------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Remember        | Retrieving relevant knowledge from long-term memory.                                              | How big is an atom?                                                                                           |
| Understand      | Questions that are solved by constructing meanings from content.                                  | Why do some plankton migrate vertically?                                                                      |
| Apply           | Answering using, for example, a specific procedure.                                               | If I double the area and take half of the fraction, do I get the same result?                                 |
| Analyze         | Content must be broken down into individual parts to understand the purpose.                      | Why did sea levels drop during the ice age?                                                                   |
| Evaluate        | Evaluating information based on criteria.                                                        | Will all the cultures merge into one big culture, due to the fading genetic distinctions?                     |
| Create          | Putting information together to design a new structure.                                           | Can somebody please explain to me what marginal benefits are and give me some examples?                       |

## Data and Code
Code and data will be made available at the start of the conference.
