import pandas as pd

df = pd.read_csv('extracted_sentences_captions.txt', sep='\t')
# print(df)
df_text2concept = df.groupby('sentence')[
    'source'].apply(list).to_frame().reset_index()
# print(df_text2concept)
df_filtered = df_text2concept[
    (df_text2concept['sentence'].apply(lambda x: len(x.split()) > 50)) &\
    (df_text2concept['source'].apply(lambda x: len(x) >3))
].drop_duplicates('sentence')
print(df_filtered)
df_filtered.to_csv('filtered_sentences_captions.txt', sep='\t', index=False)
