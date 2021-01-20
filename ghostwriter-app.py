import streamlit as st
from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer

#---------------------------------#
# Page layout
st.set_page_config(page_title='Rap Ghostwriter')

#---------------------------------#
# Model loading
model = GPT2LMHeadModel.from_pretrained('model/out').to('cpu') # because its loaded on xla by default
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

#---------------------------------#
st.write("""
# The Rap Ghostwriter App
The model is built with GPT-2 trained on top 20 popular song lyrics of each rap/hip-hop artist listed on annual Top 50 of BillBoard from last 10 years. Trained on TPUs via Pytorch/XLA for less than 30 mins.

In the following section, please input a word, a phrase or a paragraph as you wish, 
and also how long would you like the text to be?  
""")
st.write(":exclamation: Some ***profane words*** and ***racial slurs*** might be present in generated text.")

default_value_start_prompt="""I'm tired of being the one
'Cause I see the sunrise when it comes
In your face
A new woman, that's how I feel
It's all I see"""

start_prompt=st.text_area("Start prompt (a word, phrase, paragraph)", default_value_start_prompt)
max_len=st.text_input("Length for texts to be generated", 250)
max_len_int=int(max_len)

inputs=tokenizer.encode(start_prompt, add_special_tokens=False, return_tensors="pt")
prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
outputs = model.generate(inputs, max_length=max_len_int, do_sample=True, top_p=0.95, top_k=60)
generated = tokenizer.decode(outputs[0])

st.write(":ghost: ghost might need a couple of minutes to write, but hey, it's not easy for them to grab physical elements.")
if st.button('Write me some texts, Ghost!'):
    st.text_area('Text generated:',generated,height=800)