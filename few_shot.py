import json
import pandas as pd


class FewShotsong:
    def __init__(self, file_path='data/processed_songs.json'):
        self.df = None
        self.unique_tags = None
        self.load_songs(file_path)
        #print(self.df)


    def load_songs(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            songs = json.load(f)
            self.df = pd.json_normalize(songs)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))
            self.unique_moods = set(list(self.df['mood']))
            self.df = self.df

    def categorize_length(self, line_count):
        if line_count <= 35:
            return 'Corta'
        elif line_count <= 60:
            return 'Mediana'
        else:
            return 'Larga'
        

    def get_tags(self):
        return self.unique_tags
    
    def get_moods(self):
        return self.unique_moods
    
    def get_filtered_songs(self, length, mood, tag):
        df_filtered = self.df[#(self.df['length'] == length) & 
                (self.df['mood'] == mood)]
               # (self.df['tags'].apply(lambda tags: tag in tags))]
        
        return df_filtered.to_dict(orient='records')

        

if __name__ == "__main__":
    fs = FewShotsong()
    songs = fs.get_filtered_songs("Larga", "romántico", "Transformación")
    print(songs)
    