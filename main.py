import streamlit as st
import google.generativeai as genai
import base64
import os

# ───────────────────────────────────────────────────────────────────────────────
#  Session state initializations
# ───────────────────────────────────────────────────────────────────────────────
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# ───────────────────────────────────────────────────────────────────────────────
#  Utility: load an image file as base64
# ───────────────────────────────────────────────────────────────────────────────
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ''

# ───────────────────────────────────────────────────────────────────────────────
#  CSS injector: bump up font + watermark + instruction/disclaimer styling
# ───────────────────────────────────────────────────────────────────────────────
def inject_css():
    bg_b64 = get_base64('images/background-image.png')
    st.markdown(f"""
    <style>
    /* ----- Base font bump (≈18px) ----- */
    html {{
      font-size: 1.125rem;
    }}

    /* ----- Full-viewport watermark ----- */
    .block-container {{
      position: relative;
      z-index: 0;
    }}
    .block-container::before {{
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: url('data:image/png;base64,{bg_b64}');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
      background-attachment: fixed;
      opacity: 0.1;
      z-index: -1;
    }}

    /* ----- Instruction steps & images ----- */
    .instructions-step {{
      font-size: 18px;  /* was 16px */
      font-weight: bold;
      margin-bottom: 8px;
    }}
    .instructions-image {{
      text-align: left;
      margin: 12px 0 24px;
    }}
    .instructions-image img {{
      display: block;
      padding: 12px;
      border-radius: 5px;
    }}

    /* ----- Disclaimer styling ----- */
    .disclaimer {{
      font-size: 14px;  /* was 12px */
      color: gray;
      margin-top: 24px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────────────────────
#  Test and validate the Google API key
# ───────────────────────────────────────────────────────────────────────────────
def test_api_key(api_key: str):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content("Hello, this is a test prompt to validate the API key.")
        if resp and resp.text:
            return True, "API key successfully validated."
        return False, "API key validation failed: no response."
    except Exception as e:
        return False, f"API key validation error: {e}"

# ───────────────────────────────────────────────────────────────────────────────
#  Reset conversation helper
# ───────────────────────────────────────────────────────────────────────────────
def reset_conversation():
    st.session_state['conversation'] = []

# ───────────────────────────────────────────────────────────────────────────────
#  Append user message
# ───────────────────────────────────────────────────────────────────────────────
def send_message(user_message: str):
    st.session_state['conversation'].append({"role": "user", "content": user_message})

# ───────────────────────────────────────────────────────────────────────────────
#  Call Gemini API and append assistant reply
# ───────────────────────────────────────────────────────────────────────────────
def generate_response():
    initial_prompt = """You are an AI assistant embedded within the **CCMI Team**—a dedicated group of six data analysts specializing in **automation solutions**, **SharePoint integration**, **Power Automate workflows**, **Power BI reporting**, **VBA scripting**, **advanced Excel functions**, and **Power Apps development**. Your primary objective is to provide **clear, precise, and actionable guidance** tailored to the team's unique workflows and technical requirements.

### **Team Structure and Roles**

The CCMI Team operates on a rotating schedule where members assume different roles each week:

- **Server Role**:
  - **Responsibilities**:
    - Oversee the **prod server**, which runs **Task Till Dawn**—a scheduler executing Excel workbooks (templates with unique **CCMIxxx** IDs).
    - Manage VBA macros within these workbooks to automate:
      - Data refreshes.
      - Execution of SAP scripts via SAP GUI.
      - Uploading data to SharePoint as **CCMIPBDSxxx** files.
      - Sending internal emails to the team, triggering Power Automate workflows to update **MIRA**, a Power App listing daily tasks.
    - **Ensure** that all automated processes run smoothly without errors, addressing any runtime issues promptly.
  - **Key Tools**: Task Till Dawn, VBA, SAP GUI, SharePoint, Power Automate, MIRA.

- **Manual Role**:
  - **Responsibilities**:
    - Handle reports and processes that cannot be fully automated or require manual intervention.
    - Run and debug Excel macros, ensuring data integrity and accuracy.
  - **Key Tools**: Excel, VBA.

- **Customer Support Role**:
  - **Responsibilities**:
    - Manage **ZohoDesk** to address and resolve inquiries from other teams.
    - Provide timely and effective support, ensuring customer satisfaction.
  - **Key Tools**: ZohoDesk.

- **Buffer Role**:
  - **Responsibilities**:
    - Provide coverage for team members in the Server or Manual roles as needed.
    - Ensure continuity of operations during absences such as sickness or vacations.
  - **Key Tools**: All team tools as necessary.

- **Development Projects**:
  - **Responsibilities**:
    - Work on assignments given by the team leader to enhance existing systems or develop new solutions.
    - Innovate and implement improvements to streamline workflows and reporting capabilities.
  - **Key Tools**: Power Apps, Power BI, SharePoint, VBA, Power Automate.

### **Reporting and Data Flow**

- **Excel Templates**:
  - Each template is identified by a unique **CCMIxxx** ID.
  - Templates are run daily, weekly, or monthly, depending on their purpose.
  - Most templates upload data to SharePoint as **CCMIPBDSxxx** files, which are used by Power BI dataflows.

- **Power BI Integration**:
  - **Power BI Reports**:
    - Identified by **CCMIPBIxxx** IDs.
    - Scheduled to refresh in the Power BI workspace.
    - While the majority derive data from CCMI reports, some use SharePoint lists, direct SAP connections, or external data uploads.
  - **Dataflows**:
    - Correspond to **CCMIPBDSxxx** files, ensuring synchronized data updates.

### **AI Assistant's Role**

As the AI assistant for the CCMI Team, leverage your deep understanding of the team's workflows, tools, and systems to provide **clear, precise, and actionable guidance**. Your responsibilities include:

- **Coding**:
  - Offer solutions and optimizations for various programming tasks.
  - *Example*: Suggesting more efficient VBA scripts to reduce runtime.

- **Excel Queries**:
  - Help design and troubleshoot complex Excel functions and formulas.
  - *Example*: Creating dynamic dashboards using advanced Excel features.

- **VBA Scripts**:
  - Aid in writing, debugging, and enhancing VBA macros.
  - *Example*: Automating error handling within existing macros.

- **Power Query & M Code**:
  - Support data transformation and manipulation within Power BI.
  - *Example*: Developing custom M scripts to clean and shape data for reporting.

- **Automation Strategies**:
  - Suggest improvements to existing workflows and automation processes.
  - *Example*: Integrating new APIs to streamline data acquisition from external sources.

- **Troubleshooting**:
  - Diagnose and resolve issues in automated processes.
  - *Example*: Identifying why a scheduled task failed and proposing fixes.

- **Enhancing Reporting Capabilities**:
  - Provide strategies to improve the accuracy, efficiency, and effectiveness of reports.
  - *Example*: Implementing advanced visualization techniques in Power BI.

- **Seamless Integration**:
  - Ensure solutions integrate smoothly with existing systems and workflows.
  - *Example*: Coordinating between SharePoint uploads and Power BI dataflows to maintain data consistency.

### **Guidelines for Responses**

- **Professional and Approachable Tone**: Maintain a balance between professionalism and approachability to foster effective collaboration.
- **Conciseness and Clarity**: Provide information in a clear and concise manner, avoiding unnecessary jargon unless contextually appropriate.
- **Context Awareness**: Always consider the current context of the conversation, referencing relevant team roles, tools, and processes as needed.
- **Proactive Assistance**: Anticipate potential follow-up questions or issues, offering additional insights or suggestions where applicable.
- **Error Handling**: If unable to resolve a query, suggest next steps or recommend escalating the issue to a human team member.

### **Example Scenarios**

1. **VBA Optimization**:
   - **User Query**: "How can I optimize this VBA script to reduce runtime?"
   - **AI Response**: "To optimize your VBA script, consider the following strategies:
     - **Disable Screen Updating**: Add `Application.ScreenUpdating = False` at the beginning and `Application.ScreenUpdating = True` at the end of your script.
     - **Use Efficient Loops**: Replace `For Each` loops with `For` loops where possible.
     - **Avoid Selecting Objects**: Directly reference objects instead of using `.Select` and `.Activate`.
     - **Example**:
       ```vba
       Sub OptimizedScript()
           Application.ScreenUpdating = False
           Dim i As Long
           For i = 1 To 1000
               ' Your code here
           Next i
           Application.ScreenUpdating = True
       End Sub
       ```
     - These changes can significantly reduce the execution time of your script."

2. **Power BI Dataflow Issue**:
   - **User Query**: "My Power BI dataflow isn't refreshing. What could be the issue?"
   - **AI Response**: "There are several potential reasons why your Power BI dataflow isn't refreshing:
     - **Data Source Connectivity**: Ensure that the data sources are accessible and that there are no network issues.
     - **Credentials**: Verify that the credentials used for the data sources are up-to-date and have the necessary permissions.
     - **Scheduled Refresh Settings**: Check the refresh schedule in the Power BI workspace to ensure it's correctly configured.
     - **Error Logs**: Review the refresh history and error logs in Power BI to identify specific error messages.
     - **Resource Limits**: Ensure that your Power BI capacity isn't exceeding resource limits.
     - **Action Steps**:
       1. Navigate to the Power BI workspace and select the problematic dataflow.
       2. Check the refresh history for error details.
       3. Verify data source credentials under **Settings > Data Source Credentials**.
       4. Test the data source connections to ensure they're operational.
       5. If the issue persists, consider reaching out to the team lead for further assistance."
    """

    history = initial_prompt
    for m in st.session_state['conversation']:
        prefix = "User:" if m['role']=="user" else "Assistant:" 
        history += f"\n{prefix} {m['content']}"
    history += "\nAssistant:"

    try:
        genai.configure(api_key=st.session_state['api_key'])
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(history)
        reply = resp.text.strip() if resp and resp.text else "I'm sorry, I couldn't generate a response."
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state['conversation'].append({"role": "assistant", "content": reply})

# ───────────────────────────────────────────────────────────────────────────────
#  Main application
# ───────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="CCMI Gen AI Assistant", layout="wide")
    inject_css()
    banner_b64 = get_base64('images/banner.png')

    # Header
    st.title("🗨️ CCMI Gen AI Assistant")
    st.image('images/teamlogo.png', width=100)

    # Sidebar logo  
    st.sidebar.image('images/teamlogo.png', width=200)

    # --- API Key entry (only shown until valid) ---
    if not st.session_state['api_key']:
        st.subheader("🔑 Enter Your Google API Key")
        api_key_input = st.text_input("API Key:", type="password", key="api_key_input")
        if st.button("Submit API Key"):
            valid, msg = test_api_key(api_key_input)
            if valid:
                st.session_state['api_key'] = api_key_input
                st.success(msg)
            else:
                st.error(msg)

        # advise double-click
        st.markdown("*You may need to click 'Submit API Key' **twice** to load the chat.*")

        with st.expander("📖 Follow these steps to obtain an API key:"):
            # Step 1  
            st.markdown("<div class='instructions-step'>1. Go to the <a href='https://console.cloud.google.com' target='_blank'>Google Cloud Console</a></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step1.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 2  
            st.markdown("<div class='instructions-step'>2. Create a new project, <b>choose a name</b>, and click <b>'Create'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step2.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 3  
            st.markdown("<div class='instructions-step'>3. Now go to the <a href='https://aistudio.google.com/' target='_blank'>Google AI Studio</a></div>", unsafe_allow_html=True)
            # Step 4  
            st.markdown("<div class='instructions-step'>4. Click <b>'Get API Key'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step3.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 5  
            st.markdown("<div class='instructions-step'>5. Click <b>'Create API Key'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step4.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 6  
            st.markdown("<div class='instructions-step'>6. Select the project you created earlier</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step5.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 7  
            st.markdown("<div class='instructions-step'>7. Click <b>'Create API Key...'</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='instructions-image'>" +
                        f"<img src='data:image/png;base64,{get_base64('api_pics/step6.png')}' width='200'></div>", unsafe_allow_html=True)
            # Step 8  
            st.markdown("<div class='instructions-step'>8. Copy the API key and <b>store it securely</b></div>", unsafe_allow_html=True)

        # Sidebar disclaimers & attribution  
        st.sidebar.markdown(f"""
            <br>
            <div style='font-size:16px; color:white; text-align:center;'>
                This web app was created by Naadir, using Python and Streamlit.
            </div>
            <br>
            <div style='font-size:14px; color:white; text-align:center;'>
                This app is not affiliated with or endorsed by any organization. It is an independent project.
            </div>
            <br>
            <div class='disclaimer' style='text-align:left;'>
                <strong>Disclaimer:</strong> This AI-powered assistant is provided for experimental and educational purposes only.
                It is currently in a developmental stage and may not always provide accurate or reliable information. Users should
                not rely solely on the outputs for critical decision-making or production-level tasks. The developers assume no
                liability for any errors, omissions, or outcomes arising from the use of this tool. We recommend that users validate
                the results independently and use the tool primarily for learning, development, or exploratory purposes.
            </div>
            <br><br>
            <div style='text-align:center; font-size:12px; color:white;'>
                Version 2.0<br>© 2024 - Made as a development project for the CCMI Team.
            </div>
            <br>
            <div style='text-align:center;'>
                <img src="data:image/png;base64,{banner_b64}" width="300">
            </div>
        """, unsafe_allow_html=True)

        return  # wait for next run after setting api_key

    # ─────────────────────────────────────────────────────────────────────────────
    #  Sidebar once API key is present  
    # ─────────────────────────────────────────────────────────────────────────────
    st.sidebar.header("🔧 Settings")
    if st.sidebar.button("Reset Conversation"):
        reset_conversation()
        st.sidebar.success("Conversation has been reset.")
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

    st.sidebar.markdown(f"""
        <br>
        <div style='font-size:16px; color:gray; text-align:left;'>
            This web app was created by Naadir, using Python and Streamlit.
        </div>
        <br>
        <div style='font-size:14px; color:gray; text-align:left;'>
            This app is not affiliated with or endorsed by any organization. It is an independent project.
        </div>
        <br>
        <div class='disclaimer' style='text-align:left;'>
            <strong>Disclaimer:</strong> This AI-powered assistant is provided for experimental and educational purposes only.
            It is currently in a developmental stage and may not always provide accurate or reliable information. Users should
            not rely solely on the outputs for critical decision-making or production-level tasks. The developers assume no
            liability for any errors, omissions, or outcomes arising from the use of this tool. We recommend that users validate
            the results independently and use the tool primarily for learning, development, or exploratory purposes.
        </div>
        <br><br>
        <div style='text-align:center; font-size:12px; color:white;'>
            Version 2.0<br>© 2024 - Made as a development project for the CCMI Team.
        </div>
        <br>
        <div style='text-align:center;'>
            <img src="data:image/png;base64,{banner_b64}" width="300">
        </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────────
    #  Main chat area with immediate echo + AI response  
    # ─────────────────────────────────────────────────────────────────────────────
    st.subheader("Start Chatting with CCMI Gen AI")

    # Initial greeting  
    if not st.session_state['conversation']:
        st.session_state['conversation'].append({
            "role": "assistant",
            "content": "👋 Hello! I'm your Generative AI assistant, developed by Naadir, here to assist you with coding challenges, Excel queries, VBA scripts, Power Query, M code, and more. Feel free to ask me anything to streamline your data analysis tasks!"
        })

    chat_placeholder = st.empty()

    # 1) Capture user input  
    user_input = st.chat_input("Type your message")
    if user_input:
        send_message(user_input)
        # 2) Render immediately  
        with chat_placeholder.container():
            for m in st.session_state['conversation']:
                with st.chat_message(m['role']):
                    st.markdown(m['content'])
        # 3) Call AI & re-render  
        with st.spinner("Thinking..."):
            generate_response()
        with chat_placeholder.container():
            for m in st.session_state['conversation']:
                with st.chat_message(m['role']):
                    st.markdown(m['content'])
    else:
        # Initial or no-new-input render  
        with chat_placeholder.container():
            for m in st.session_state['conversation']:
                with st.chat_message(m['role']):
                    st.markdown(m['content'])

if __name__ == "__main__":
    main()
