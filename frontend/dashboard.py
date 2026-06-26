import streamlit as st
import requests


st.set_page_config(page_title="Retrievel Augmentation Generation",layout="wide")
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
    
if not st.session_state.document_processed:
    try:
        resp = requests.get("http://localhost:8000/documents")
        if resp.status_code == 200:
            docs = resp.json()["documents"]
            if docs:
                st.session_state.document_processed = True
                st.session_state.ingested_files = docs
    except Exception:
        pass   
    
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = []
      
st.title("Reitrievel Augmentation Generation")

#sidebar
st.sidebar.header("Upload & Filter")
uploaded_file = st.sidebar.file_uploader("Upload your Document",type=["pdf"],accept_multiple_files=False)
if st.session_state.ingested_files:
    st.sidebar.write("Ingested documents:")
    for f in st.session_state.ingested_files:
        st.sidebar.write(f"- {f}")
#Process document
if st.sidebar.button("Process the Document"):  
    if not uploaded_file:
        st.sidebar.error("please enter a document")
    else:
        with st.spinner("Processing Document..."):
            try:
                response = requests.post("http://localhost:8000/ingest",files={"file": (uploaded_file.name,uploaded_file,"application/pdf")})
                if response.status_code == 200:
                    st.session_state.document_processed = True
                    st.session_state.uploaded_filename =  uploaded_file.name
                    st.session_state.ingested_files.append(uploaded_file.name)
                    st.success("Processed Sucessfully!!"f"  Loaded: {st.session_state.uploaded_filename}")
                else:
                    st.error(f"Processing error:{response.text}")    
            except Exception as e:
                st.error(f"Exeception: {str(e)}")

#Chat Interface
if not st.session_state.document_processed:
    st.info("Upload and process a document first.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Chat input
    question = st.chat_input("Ask a question about your documents...")
    if question:
    # Show user message
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        # Call FastAPI
        response = requests.post(
            "http://localhost:8000/query",
            json={"question": question}
        )
        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
            citations = data["citations"]
            # Store assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            with st.chat_message("assistant"):
                st.markdown(answer)
                if citations:
                    with st.expander("Sources"):
                        for c in citations:
                            st.markdown(f"**{c['source']}**, page {c['page_number']} (score: {c['score']})")
                            st.caption(c['excerpt'])
        else:
            st.error("Query failed")