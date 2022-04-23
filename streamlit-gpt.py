import streamlit as st
import openai

class Model:
    def __init__(self, api_key, max_length):
        openai.api_key = api_key
        self.completion = openai.Completion
        self.max_length = max_length
        self.options = {
            'engine': 'text-davinci-002',
            'temperature': 0.05,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }

    def __call__(self, url, q_1, q_2):
        ans_1 = self.prediction(url, q_1)
        ans_2 = self.prediction(url, q_2)

        return ans_1, ans_2

    def prediction(self, t1, t2):        
        prompt = '{text_1}\n{text_2}'.format(text_1=t1, text_2=t2)

        answer = self.completion.create(
            prompt=prompt,
            max_tokens=self.max_length,
            **self.options
        )['choices'][0]['text']

        return answer

    def opinion(self, txt):
        return self.completion.create(
            prompt=txt,
            max_tokens=self.max_length,
            **self.options
        )['choices'][0]['text']
def page():
    st.set_page_config(
        page_title='GPT-3 showcase',
        layout='centered'
        )

    key = st.sidebar.text_input('OpenAI API Key:', type='password')

    length = st.sidebar.slider('Maximum length of the answer', 32, 512, 64)

    if not key:
        st.header('🔑 Pass API key to get access to form.')

    elif key:    
        st.header('🌎 Find out something about website!')

        model = Model(
            api_key=key,
            max_length=length
        )

        side_text = st.sidebar.text_input(label='Opinion', placeholder='Tell GPT-3 what do you think about it.')
        side_button = st.sidebar.button('Submit form', key=0)

        if side_button:
            st.sidebar.markdown('GPT-3: {answer}'.format(answer=model.prediction('Answer that opinion:', side_text)))


        url = st.text_input(
            label='URL', 
            placeholder='Please, put here url to website.'
        )
        q_1 = st.text_input(
            label='Question 1', 
            placeholder='Put here question that you have about this website.', 
            disabled=False if url else True
        )
        q_2 = st.text_input(
            label='Question 2', 
            placeholder='Put here 2nd question about website or about something else.', 
            disabled=False if url and q_1 else True
        )

        button_1 = st.button('Submit form', disabled=False if url and q_1 and q_2 else True, key=1)

        if button_1:
            a1, a2 = model(url, q_1, q_2)

            st.markdown(f'Q1: {a1}')
            st.markdown(f'Q2: {a2}')

    footer_css = '''
        <style>
            footer {
                visibility: visible;
                font-size: 0 !important;
            } 
            footer:after {
                content: 'Created by jmisilo';
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 5px;
                font-size: 14px;
            }
        </style>
    '''

    st.markdown(footer_css, unsafe_allow_html=True)

if __name__ == '__main__':
    page()