import pandas as pd
import krippendorff


def convert_yes_no(value):
    if pd.isna(value):
        return None
    val = str(value).strip().lower()
    if val == 'yes':
        return 1
    elif val == 'no':
        return 0
    else:
        try:
            return int(value)
        except ValueError:
            print("error")
            return None

bloom_mapping = {
    "-": 0,
    "remembering": 1,
    "understanding": 2,
    "applying": 3,
    "analyzing": 4,
    "evaluating": 5,
    "creating": 6
}

def convert_bloom(value):

    if pd.isna(value):
        return None
    val = str(value).strip().lower()
    return bloom_mapping.get(val, None)


def process_files(file_list):
    df_list = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    if not df_list:
        return pd.DataFrame()
    
    df_all = pd.concat(df_list, ignore_index=True)
    
    df_all = df_all[['Relevance', 'Answerability', "Bloom's Level"]]
    df_all = df_all.dropna(how='all').reset_index(drop=True)
    df_all['Relevance'] = df_all['Relevance'].apply(convert_yes_no)
    df_all['Answerability'] = df_all['Answerability'].apply(convert_yes_no)
    df_all["Bloom's Level"] = df_all["Bloom's Level"].apply(convert_bloom)
    
    return df_all


person_a_files = ['/data/manual_evaluation/video_evaluation_annotator1_teded.csv', '/data/manual_evaluation/video_evaluation_annotator1_khan.csv']
person_b_files = ['/data/manual_evaluation/video_evaluation_annotator2_teded.csv', '/data/manual_evaluation/video_evaluation_annotator2_khan.csv']


df_a = process_files(person_a_files)
df_b = process_files(person_b_files)

merged_df = pd.concat([df_a.reset_index(drop=True), df_b.reset_index(drop=True)], axis=1)

data_relevance = merged_df.iloc[:, [0, 3]].T.values.tolist()
data_answerability = merged_df.iloc[:, [1, 4]].T.values.tolist()
data_bloom = merged_df.iloc[:, [2, 5]].T.values.tolist()


print(data_relevance)


alpha_relevance = round(krippendorff.alpha(reliability_data=data_relevance, level_of_measurement='nominal'), 2)
alpha_answerability = round(krippendorff.alpha(reliability_data=data_answerability, level_of_measurement='nominal'), 2)
alpha_bloom = round(krippendorff.alpha(reliability_data=data_bloom, level_of_measurement='ordinal'), 2)

print("Krippendorff's Alpha for Relevance:", alpha_relevance)
print("Krippendorff's Alpha for Answerability:", alpha_answerability)
print("Krippendorff's Alpha for Bloom's Level:", alpha_bloom)
