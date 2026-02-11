import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import tempfile
import os

# API Key
API_KEY = "AIzaSyDBYrye_IhG5fcZzqQjOaPLP0iL9zenqfY"

# အရေးကြီးဆုံးအချက် - v1beta အစား v1 ကို အတင်းသုံးခိုင်းပါမယ်
# ဒါက 404 Error ကို ကျော်လွှားဖို့ တစ်ခုတည်းသောနည်းလမ်းပါ
genai.configure(api_key=API_KEY)

# Model နာမည်ကို နာမည်အပြည့်အစုံ သုံးပါမယ်
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

st.title("🇲🇲 AI Myanmar Voice (Final Test)")

if prompt := st.chat_input("မေးခွန်းရိုက်ပါ..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # Generate content with exact model
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
            # ဘာကြောင့် Error တက်လဲဆိုတာ အတိအကျပြပါမယ်
            st.error(f"Error Detail: {str(e)}")
            st.info("အကယ်၍ 404 ဖြစ်နေသေးရင် API Key အသစ်တစ်ခု လိုအပ်နိုင်ပါတယ်။")
            
