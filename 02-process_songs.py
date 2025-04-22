import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_songs(raw_file_path, processed_file_path="data/processed_songs.json"):

    enriched_songs = []
    with open(raw_file_path, encoding='utf-8') as file:
        songs = json.load(file)
        
        for song in songs:
            metadata = extract_metadata(song['lyric'])

            post_with_metadata = song | metadata
            enriched_songs.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_songs)

    for song in enriched_songs:
        current_tags = song['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        song['tags'] = list(new_tags)

    with open(processed_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(enriched_songs, outfile, indent=4)

def get_unified_tags(enriched_songs):
    unique_tags = set()
    for song in enriched_songs:
        unique_tags.update(song['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Amor", "Amorío" can be all merged into a single tag "Amor". 
       Example 2: "Crítica", "Crítica social" can be mapped to "Crítica"
       Example 3: "Crecimiento Personal", "Desarrollo Personal" can be mapped to "Superación Personal"
    2. Each tag should be follow title case convention. example: "Amor", "Crítica"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Amor": "Amor",  "Amorío": "Amor"}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


def extract_metadata(post_arg): 
    template = '''
    You are given a song in Spanish by a certain artist.
    You need to extract number of lines, paragraphs, tags and mood. You must follow the following rules:

    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, tags and mood. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. mood is a text that represents the mood of the song.
    5. line_count is a number that represents the number of lines in the song.
    6. paragraph_count is a number that represents the number of paragraphs in the song.
    
    Here is the actual song on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post_arg})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res



if __name__ == "__main__":
    process_songs("data/raw_songs.json", "data/processed_songs.json")