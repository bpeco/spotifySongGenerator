from llm_helper import llm
from few_shot import FewShotsong

few_shot = FewShotsong()



def get_length_str(length):
    if length == "Corta":
        return "1 to 35 lines"
    if length == "Mediana":
        return "36 to 60 lines"
    if length == "Larga":
        return "Minimum 61 lines"

def get_prompt(length, mood, tag):
    length_str = get_length_str(length)
    prompt = f"""
    Generate a song using the below information. No preamble.
    \nRemember following these instructions:
        1) Do not include any preamble.
        2) Do not use the same chorus as the given examples (if there are any examples).
        3) Write the song considering the tag, mood and lenght.
        4) Some paragraphs have to have a rhyme. Not all of them, but some of them must.
        5) Give a name to the song afterwards. Do not use the tag, mood and length for the name, use the lyrics you created. Write the name on top of the song.

    The lyric for the generated song should always be Spanish.
    """

    examples = few_shot.get_filtered_songs(length, mood, tag)
    if len(examples) > 0:
        prompt += f"""
        6) Use the writing style as per the following examples..
"""
        
        for i, song in enumerate(examples):
            song_text = song['lyric']
            prompt += f"\n\n\nExample {i+1}: \n\n {song_text}"
            if i == 3:
                break
   
    prompt += "\n\nOnly imitate the writing style, do not copy the lyrics. Write your own words and idea for the song but keeping the style of the examples"
    print("-------------------------\n\n",prompt,"-------------------------\n\n")
    return prompt

    
def generate_song(length, mood, tag):
    
    prompt = get_prompt(length, mood, tag)
    response = llm.invoke(prompt)
    return response.content

def get_song_name(song):
    return song.split("\n")[0]

def get_song_lyric(song):
    return song.split("\n")[1:]

if __name__ == "__main__":
    song = generate_song("Larga", "romántico", "Transformación")
    print(song)