import pandas as pd


df_a = pd.read_csv('/data/manual_evaluation/collaborative_evaluation_teded.csv')
df_b = pd.read_csv('/data/manual_evaluation/collaborative_evaluation_khan.csv')


df_combined = pd.concat([df_a, df_b], axis=0).reset_index(drop=True)


df_combined = df_combined[df_combined['Question?'].str.lower() == 'yes'].dropna()


df_combined['Approach'] = df_combined['Approach'].str.lower()
df_combined['Model'] = df_combined['Model'].str.lower()
df_combined["Bloom's Level"] = df_combined["Bloom's Level"].str.lower()
df_combined['Relevance'] = df_combined['Relevance'].str.lower()
df_combined['Answerability'] = df_combined['Answerability'].str.lower()


df_zero_shot = df_combined[df_combined['Approach'] == 'zero-shot']
df_fine_tuned = df_combined[df_combined['Approach'] == 'fine-tuned']
df_audio_only = df_combined[df_combined['Approach'] == 'audio only']
df_frames_only = df_combined[df_combined['Approach'] == 'frames only']

approaches = {
    "zero-shot": df_zero_shot,
    "fine-tuned": df_fine_tuned,
    "audio only": df_audio_only,
    "frames only": df_frames_only
}


bloom_levels = ["-", "remembering", "understanding", "applying", "analyzing", "evaluating", "creating"]


def calculate_percentage(df, column, categories):
    counts = df[column].value_counts(normalize=True) * 100
    counts_rounded = {category: round(counts.get(category, 0), 2) for category in categories}
    return counts_rounded


results = {}
overall_results = {}

for approach, df_approach in approaches.items():
    approach_results = {}

    for model in df_approach['Model'].unique():
        df_model = df_approach[df_approach['Model'] == model.lower()]
        

        relevance_percentage = calculate_percentage(df_model, 'Relevance', ['yes', 'no'])
        answerability_percentage = calculate_percentage(df_model, 'Answerability', ['yes', 'no'])
        

        bloom_percentage = calculate_percentage(df_model, "Bloom's Level", bloom_levels)
        

        approach_results[model.lower()] = {
            'Relevance': relevance_percentage,
            'Answerability': answerability_percentage,
            "Bloom's Level": bloom_percentage
        }
    

    results[approach] = approach_results

    overall_relevance = calculate_percentage(df_approach, 'Relevance', ['yes', 'no'])
    overall_answerability = calculate_percentage(df_approach, 'Answerability', ['yes', 'no'])
    overall_bloom = calculate_percentage(df_approach, "Bloom's Level", bloom_levels)
    
    overall_results[approach] = {
        'Relevance': overall_relevance,
        'Answerability': overall_answerability,
        "Bloom's Level": overall_bloom
    }

for approach, approach_results in results.items():
    print(f"Results for {approach}:")
    for model, model_results in approach_results.items():
        print(f"\n  Model: {model}")
        print(f"    Relevance: {model_results['Relevance']}")
        print(f"    Answerability: {model_results['Answerability']}")
        print("    Bloom's Level:" +  str(model_results["Bloom's Level"]))

overall_relevance = calculate_percentage(df_combined, 'Relevance', ['yes', 'no'])
overall_answerability = calculate_percentage(df_combined, 'Answerability', ['yes', 'no'])
overall_bloom = calculate_percentage(df_combined, "Bloom's Level", bloom_levels)

print("\nOverall Results for all Approaches combined:")

print(f"  Relevance: {overall_relevance}")
print(f"  Answerability: {overall_answerability}")
print(f"  Bloom's Level: {overall_bloom}")
