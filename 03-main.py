import streamlit as st
from few_shot import FewShotsong
from song_generator import generate_song, get_song_name, get_song_lyric

length_options = ['Corta', 'Mediana', 'Larga']
language_options = ['Spanish']

def main():
    st.title("Song Generator")
    
    col1, col2, col3 = st.columns(3)
    fs = FewShotsong()

    with col1:
        selected_tag = st.selectbox('Tag', options=fs.get_tags())

    with col2:
        selected_lenght = st.selectbox('Largo', options=length_options)

    with col3:
        selected_mood = st.selectbox('Mood', options=fs.get_moods())

    if st.button('Generate song'):
        song = generate_song(selected_lenght, selected_mood, selected_tag)
        st.header(get_song_name(song))
        st.write(get_song_lyric(song))

    
    

if __name__ == "__main__":
    main()