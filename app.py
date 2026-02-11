import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import tempfile
import os

# သင် အခုလေးတင် ပေးလိုက်တဲ့ API Key အသစ်
API_KEY = "AIzaSyBVZ7D9YugpdTKxyCe0yRfHVhG819NDY1g"
genai.configure(api_key=API_KEY)

# တည်ငြိမ်မှု အရှိဆုံး Model ကို သုံးပါမယ်
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🇲🇲 AI Myanmar Voice (Final Success)")

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
            st.error(f"Error: {str(e)}")

