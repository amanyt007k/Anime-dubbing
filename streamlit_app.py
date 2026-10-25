
import streamlit as st
import whisper
from googletrans import Translator
import asyncio
import edge_tts
import subprocess

st.title("🎬 Free Anime Hindi Dubbing Web App")
st.write("Apni Anime Clip Upload Karein Aur Hindi Voice Me Dub Karein!")

uploaded_file = st.file_uploader("Video File Upload Karein (MP4)", type=["mp4"])

if uploaded_file is not None:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    
    if st.button("Start Hindi Dubbing"):
        st.info("⏳ Audio extract ho raha hai...")
        subprocess.run(["ffmpeg", "-y", "-i", "input.mp4", "-ar", "16000", "-ac", "1", "audio.wav"])
        
        st.info("🧠 Whisper AI Dialogues sun raha hai...")
        model = whisper.load_model("base")
        result = model.transcribe("audio.wav")
        original_text = result["text"]
        st.write("Original Dialogues:", original_text)
        
        st.info("🌐 Hindi me translate ho raha hai...")
        translator = Translator()
        hindi_text = translator.translate(original_text, dest='hi').text
        st.write("Hindi Dialogues:", hindi_text)
        
        st.info("🗣️ Hindi AI Voice create ho rahi hai...")
        async def generate_voice():
            communicate = edge_tts.Communicate(hindi_text, "hi-IN-MadhurNeural")
            await communicate.save("hindi_audio.mp3")
        
        asyncio.run(generate_voice())
        
        st.info("🎬 Final Video Sync ho rahi hai...")
        subprocess.run([
            "ffmpeg", "-y", 
            "-i", "input.mp4", 
            "-i", "hindi_audio.mp3", 
            "-c:v", "copy", 
            "-c:a", "aac", 
            "-map", "0:v:0", 
            "-map", "1:a:0", 
            "output_dubbed.mp4"
        ])
        
        st.success("🎉 Hindi Dubbing Complete!")
        st.video("output_dubbed.mp4")
        
        with open("output_dubbed.mp4", "rb") as file:
            st.download_button("Download Dubbed Video", file, file_name="dubbed_anime.mp4")
