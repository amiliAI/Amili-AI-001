import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import tempfile
import os

# API Key
API_KEY = "AIzaSyDBYrye_IhG5fcZzqQjOaPLP0iL9zenqfY"
genai.configure(api_key=API_KEY)

# အရှင်းဆုံး Model နာမည်ကို သုံးပါမယ်
model = genai.GenerativeModel('gemini-pro')

st.title("🇲🇲 AI Myanmar Voice (Final)")

if prompt := st.chat_input("မေးခွန်းရိုက်ပါ..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # AI အဖြေထုတ်ခြင်း
            response = model.generate_content(prompt)
            ai_text = response.text
            st.markdown(ai_text)
            
            # အသံဖိုင်ပြောင်းလဲခြင်း
            async def speak(text):
                communicate = edge_tts.Communicate(text, "my-MM-NilarNeural")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    await communicate.save(tmp.name)
                    return tmp.name
            
            audio_path = asyncio.run(speak(ai_text))
            with open(audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove(audio_path)
            
        except Exception as e:
            # Error အသေးစိတ်ကို ပြခိုင်းပါမယ်
            st.error(f"Error Detail: {str(e)}")
            st.info("အကယ်၍ 404 ဖြစ်နေရင် Streamlit Reboot လုပ်ပေးပါ။")
