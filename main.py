import streamlit as st
import google.generativeai as genai
import base64
import os

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'input' not in st.session_state:
    st.session_state['input'] = ''

def get_base64(file_path):
    """
    Read an image and return its base64 encoded string.
    """
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ''

def inject_css():
    """
    Inject custom CSS to style the chatbot messages and interface.
    """
    st.markdown(f"""
    <style>
    /* General styling to match the theme */
    body {{
        font-family: 'Arial', sans-serif;
    }}

    /* Main content area with background image using pseudo-element */
    .block-container {{
        position: relative;
        z-index: 0;
    }}

    .block-container::before {{
        content: "";
        background-image: url('data:image/png;base64,{get_base64('images/background-image.png')}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed; /* Prevents resizing */
        opacity: 0.1; /* Adjust this value to control image visibility (0.0 to 1.0) */
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        z-index: -1;
    }}

    /* Styling for chat container */
    .chat-container {{
        display: flex;
        flex-direction: column;
        max-height: 500px; /* Adjust height as needed */
        overflow-y: auto;
        margin-bottom: 20px; /* Reduced margin */
    }}

    /* Message row */
    .message-row {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
        max-width: 80%;
    }}

    /* Assistant message */
    .message-row.assistant {{
        flex-direction: row;
    }}

    /* User message */
    .message-row.user {{
        flex-direction: row-reverse;
        align-self: flex-end;
    }}

    /* Profile picture */
    .profile-pic {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 5px;
        display: block;
    }}

    /* Message text */
    .message-text {{
        background-color: transparent; /* Fully transparent background */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2); /* Subtle text shadow for readability */
        padding: 10px;
        border-radius: 10px;
        max-width: 100%;
        word-wrap: break-word;
        color: inherit;
    }}

    /* Adjust text color based on theme */
    html[data-theme='dark'] .message-text {{
        color: white;
    }}

    html[data-theme='light'] .message-text {{
        color: black;
    }}

    /* Styling for the input box */
    .input-box {{
        margin-top: 20px;
    }}

    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {{
        width: 8px;
    }}

    .chat-container::-webkit-scrollbar-track {{
        background: #f1f1f1;
    }}

    .chat-container::-webkit-scrollbar-thumb {{
        background: #888;
    }}

    .chat-container::-webkit-scrollbar-thumb:hover {{
        background: #555;
    }}

    /* Adjust instruction text size */
    .instructions-step {{
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    .instructions-text {{
        font-size: 14px;
        margin-bottom: 10px;
    }}

    /* Align instruction images to the left */
    .instructions-image {{
        text-align: left;
        margin-bottom: 20px;
        margin-top: 10px;
    }}
    .instructions-image img {{
        display: block;
        padding: 10px;
        border-radius: 5px;
    }}

    /* Styling for the disclaimer */
    .disclaimer {{
        font-size: 12px;
        color: gray;
        margin-top: 20px;
    }}

    </style>
    """, unsafe_allow_html=True)

def test_api_key(api_key):
    """
    Test the provided API key by making a simple request.
    Returns True if the key is valid, False otherwise.
    """
    try:
        # Configure the Generative AI client with the API key
        genai.configure(api_key=api_key)
        
        # Initialize the Generative Model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Define a sample prompt
        prompt = "Hello, this is a test prompt to validate the API key."
        
        # Generate content based on the prompt
        response = model.generate_content(prompt)
        
        if response and response.text:
            return True, "API key successfully validated."
        else:
            return False, "API key validation failed. No response received."
    except Exception as e:
        return False, f"API key validation error: {e}"

def reset_conversation():
    """
    Resets the conversation history.
    """
    st.session_state['conversation'] = []

def send_message():
    """
    Sends the user's message to the AI model and updates the conversation.
    """
    user_input = st.session_state['input']
    if user_input.strip() != '':
        # Append user message to conversation
        st.session_state['conversation'].append({"role": "user", "content": user_input})
        # Clear the input box
        st.session_state['input'] = ''
        try:
            # Configure the Generative AI client with the API key
            genai.configure(api_key=st.session_state['api_key'])

            # Initialize the Generative Model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Build the prompt by concatenating conversation history
            conversation_history = ''
            # Define the detailed initial system prompt
            initial_prompt = """
            You are an AI assistant embedded within the **CCMI Team**—a close-knit group of six data analysts specializing in **automation solutions**, **SharePoint integration**, **Power Automate workflows**, **Power BI reporting**, **VBA scripting**, **advanced Excel functions**, and **Power Apps development**. The team operates on a rotating schedule where members assume different roles each week:
            
            - **Server Role**: Responsible for overseeing the **prod server**, which runs **Task Till Dawn**, a scheduler that executes Excel workbooks (templates with unique **CCMIxxx** IDs). These workbooks contain VBA macros that automate data refreshes, run SAP scripts via SAP GUI, upload data to SharePoint as **CCMIPBDSxxx** files, and send internal emails to the team. These emails trigger Power Automate workflows to update **MIRA**, a Power App listing daily tasks. The Server Role ensures these automated processes run smoothly without errors.
            
            - **Manual Role**: Handles reports and processes that cannot be fully automated or require manual intervention, including running Excel macros and ensuring data integrity.
            
            - **Customer Support Role**: Manages **ZohoDesk** to address and resolve inquiries from other teams, providing timely and effective support.
            
            - **Buffer Role**: Provides coverage for team members in the Server or Manual roles as needed, ensuring continuity of operations during absences.
            
            - **Development Projects**: Works on assignments given by the team leader to enhance existing systems or develop new solutions.
            
            The team's reports are integral to company-wide operations. Most Excel templates feed into Power BI reports with IDs like **CCMIPBIxxx**, scheduled to refresh in the Power BI workspace. While the majority of data comes from the team's automated processes, some Power BI reports also source data from SharePoint lists, direct SAP connections, or external uploads by other users.
            
            **AI Assistant's Role:**
            
            As the AI assistant for the CCMI Team, leverage your deep understanding of the team's workflows, tools, and systems to provide **clear, precise, and actionable guidance**. Assist with:
            
            - **Coding**: Offer solutions and optimizations for various programming tasks.
            - **Excel Queries**: Help design and troubleshoot complex Excel functions and formulas.
            - **VBA Scripts**: Aid in writing, debugging, and enhancing VBA macros.
            - **Power Query & M Code**: Support data transformation and manipulation within Power BI.
            - **Automation Strategies**: Suggest improvements to existing workflows and automation processes.
            
            Additionally, **troubleshoot issues** in automated processes, **enhance reporting capabilities**, and **integrate solutions seamlessly** with existing systems. Your responses should be **tailored to the team's unique environment and challenges**, making members feel as if you are an integral part of the team who comprehends every aspect of their work.
            """
            # Add the initial system prompt to the conversation history
            conversation_history += initial_prompt

            for message in st.session_state['conversation']:
                if message['role'] == 'user':
                    conversation_history += f"\nUser: {message['content']}"
                else:
                    conversation_history += f"\nAssistant: {message['content']}"
            # Append current user input
            conversation_history += "\nAssistant:"

            # Generate AI response
            response = model.generate_content(conversation_history)

            ai_response = response.text.strip() if response and response.text else "I'm sorry, I couldn't generate a response."

            # Append AI response to conversation
            st.session_state['conversation'].append({"role": "assistant", "content": ai_response})

        except Exception as e:
            st.session_state['conversation'].append({"role": "assistant", "content": f"Error: {e}"})

def main():
    st.set_page_config(page_title="CCMI Gen AI Assistant", layout="wide")
    inject_css()

    st.title("🗨️ CCMI Gen AI Assistant")
    # Display the image using st.image
    st.image('images/teamlogo.png', width=100)

    # Sidebar content
    # Display the logo using st.sidebar.image
    st.sidebar.image('images/teamlogo.png', width=200)

    if not st.session_state['api_key']:
        st.subheader("🔑 Enter Your Google API Key")
        with st.form(key='api_key_form'):
            api_key = st.text_input("API Key:", type="password")
            submit_api_key = st.form_submit_button("Submit")
            if submit_api_key:
                with st.spinner("Validating API Key..."):
                    valid, message = test_api_key(api_key)
                if valid:
                    st.success(message)
                    st.session_state['api_key'] = api_key
                else:
                    st.error(message)

        with st.expander("📖 Follow these steps to obtain an API key:"):
            # Step 1
            st.markdown("<div class='instructions-step'>1. Go to the <a class='instructions-link' href='https://console.cloud.google.com' target='_blank'>Google Cloud Console</a></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step1.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 2
            st.markdown("<div class='instructions-step'>2. Create a new project, <b>choose a name</b>, and click <b>'Create'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step2.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 3
            st.markdown("<div class='instructions-step'>3. Now go to the <a class='instructions-link' href='https://aistudio.google.com/' target='_blank'>Google AI Studio</a></div>", unsafe_allow_html=True)

            # Step 4
            st.markdown("<div class='instructions-step'>4. Click <b>'Get API Key'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step3.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 5
            st.markdown("<div class='instructions-step'>5. Click <b>'Create API Key'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step4.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 6
            st.markdown("<div class='instructions-step'>6. Select the project you created earlier</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step5.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 7
            st.markdown("<div class='instructions-step'>7. Click <b>'Create API Key...'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'><img src='data:image/png;base64,{get_base64('api_pics/step6.png')}' width='200'></div>", unsafe_allow_html=True)

            # Step 8
            st.markdown("<div class='instructions-step'>8. Copy the API key and <b>store it securely</b></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # Top of the sidebar - attribution
        st.sidebar.markdown("""
            <br>
            <div style='font-size:16px; color:white; text-align: center;'>
                This web app was created by Naadir, using Python and Streamlit.
            </div>
        """, unsafe_allow_html=True)

        # Additional disclaimer at the bottom
        st.sidebar.markdown("""
            <br>
            <div style='font-size:14px; color:white; text-align: center;'>
                This app is not affiliated with or endorsed by any organization. It is an independent project.
            </div>
        """, unsafe_allow_html=True)


        # Professional disclaimer in the middle
        st.sidebar.markdown("""
            <br>
            <div class='disclaimer' style='color:gray; text-align: left;'>
                <strong>Disclaimer:</strong> This AI-powered assistant is provided for experimental and educational purposes only. 
                It is currently in a developmental stage and may not always provide accurate or reliable information. Users should 
                not rely solely on the outputs for critical decision-making or production-level tasks. The developers assume no 
                liability for any errors, omissions, or outcomes arising from the use of this tool. We recommend that users validate 
                the results independently and use the tool primarily for learning, development, or exploratory purposes.
            </div>
        """, unsafe_allow_html=True)



        st.sidebar.markdown("""
            <br>
            <br>
            <div style='text-align: center; font-size: 12px; color: white;'>
                Version 2.0<br>© 2024 - Made as a development project for the CCMI Team.
            </div>
        """, unsafe_allow_html=True)

        image_base64 = get_base64('images/banner.png')
        st.sidebar.markdown(f"""
            <br>
            <div style='text-align: center;'>
                <img src="data:image/png;base64,{image_base64}" width="300">
            </div>
        """, unsafe_allow_html=True)




    else:
        # Sidebar content for the main chat interface
        st.sidebar.header("🔧 Settings")
        if st.sidebar.button("Reset Conversation"):
            reset_conversation()
            st.sidebar.success("Conversation has been reset.")

        # Examples section
        st.sidebar.markdown("### 💡 Examples of what you can ask:")
        with st.sidebar.expander("VBA Questions"):
            st.sidebar.markdown("""
            - How do I write a VBA macro to automate data entry?
            - How can I loop through all cells in a range using VBA?
            """)
        with st.sidebar.expander("Power Query Questions"):
            st.sidebar.markdown("""
            - How do I merge two tables in Power Query?
            - How can I unpivot columns in Power Query?
            """)
        with st.sidebar.expander("M Code Examples"):
            st.sidebar.markdown("""
            - What's the M code to filter rows based on a condition?
            - How do I create a custom column using M code?
            """)

        # Top of the sidebar - attribution
        st.sidebar.markdown("""
            <br>
            <div style='font-size:16px; color:gray; text-align: left;'>
                This web app was created by Naadir, using Python and Streamlit.
            </div>
        """, unsafe_allow_html=True)

        # Additional disclaimer at the bottom
        st.sidebar.markdown("""
            <br>
            <div style='font-size:14px; color:gray; text-align: left;'>
                This app is not affiliated with or endorsed by any organization. It is an independent project.
            </div>
        """, unsafe_allow_html=True)


        # Professional disclaimer in the middle
        st.sidebar.markdown("""
            <br>
            <div class='disclaimer' style='color:gray; text-align: left;'>
                <strong>Disclaimer:</strong> This AI-powered assistant is provided for experimental and educational purposes only. 
                It is currently in a developmental stage and may not always provide accurate or reliable information. Users should 
                not rely solely on the outputs for critical decision-making or production-level tasks. The developers assume no 
                liability for any errors, omissions, or outcomes arising from the use of this tool. We recommend that users validate 
                the results independently and use the tool primarily for learning, development, or exploratory purposes.
            </div>
        """, unsafe_allow_html=True)



        st.sidebar.markdown("""
            <br>
            <br>
            <div style='text-align: center; font-size: 12px; color: white;'>
                Version 2.0<br>© 2024 - Made as a development project for the CCMI Team.
            </div>
        """, unsafe_allow_html=True)

        image_base64 = get_base64('images/banner.png')
        st.sidebar.markdown(f"""
            <br>
            <div style='text-align: center;'>
                <img src="data:image/png;base64,{image_base64}" width="300">
            </div>
        """, unsafe_allow_html=True)


        
        # Welcome message
        st.subheader("Start Chatting with CCMI Gen AI")

        # Add initial greeting message if conversation is empty
        if not st.session_state['conversation']:
            initial_message = {
                "role": "assistant",
                "content": "👋 Hello! I'm your Generative AI assistant, developed by Naadir, here to assist you with coding challenges, Excel queries, VBA scripts, Power Query, M code, and more. Feel free to ask me anything to streamline your data analysis tasks!"
            }
            st.session_state['conversation'].append(initial_message)

        # Container for chat messages
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state['conversation']:
            if chat['role'] == 'assistant':
                st.markdown(f"""
                <div class='message-row assistant'>
                    <img src="data:image/png;base64,{get_base64('images/assistant_profile.png')}" class='profile-pic' />
                    <div class='message-text'>{chat['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='message-row user'>
                    <img src="data:image/png;base64,{get_base64('images/user_profile.png')}" class='profile-pic' />
                    <div class='message-text'>{chat['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Input for user to send messages
        # Placed directly under the chat container without fixed positioning
        st.markdown("<div class='input-box'>", unsafe_allow_html=True)
        st.text_area("Type your message", key='input', on_change=send_message, height=150)
        st.markdown("</div>", unsafe_allow_html=True)

        # Automatically scroll to the latest message
        if st.session_state['conversation']:
            st.markdown(
                """
                <script>
                const chatContainer = document.querySelector('.chat-container');
                chatContainer.scrollTop = chatContainer.scrollHeight;
                </script>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
