import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import tempfile
import os

# API Key
API_KEY = "AIzaSyDBYrye_IhG5fcZzqQjOaPLP0iL9zenqfY"

# အရေးကြီးဆုံးအပိုင်း - API version ကို v1 လို့ အတင်းသတ်မှတ်ပါမယ်
genai.configure(api_key=API_KEY, transport='rest') 

# Model ကို နာမည်အပြည့်အစုံမဟုတ်ဘဲ gemini-1.5-flash လို့ပဲ သုံးပါမယ်
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🇲🇲 AI Myanmar Voice (Final Fix)")

if prompt := st.chat_input("မေးခွန်းရိုက်ပါ..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Model အလုပ်လုပ်မလုပ် အရင်စစ်မယ်
            response = model.generate_content(prompt)
            ai_text = response.text
            st.markdown(ai_text)
            
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
            st.error(f"Error Detail: {str(e)}")
            st.info("အကယ်၍ 404 ဖြစ်နေသေးရင် app settings ထဲမှာ API Key ကို ပြန်စစ်ပေးပါ။")
