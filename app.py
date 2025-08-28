import streamlit as st 
import pandas as pd 
#Brings in Pandas for working with data tables(Dataframes)
from agent_logic import(
    parse_resume_pdf_agent,
    parse_resume_txt_agent,
    extract_skills_agent,
    calculate_score_agent,
    get_candidate_name_agent
)
#Import the function we wrote earlier in agent_logic.py 
st.set_page_config(
    page_title="Recruitment AI Agent",
    page_icon="",
    layout="centered"
)
#Sets up the look and feel of the streamlit app 
#page_title--> browser tab title 
#page_icon -->small emoji/icon in tab 
#layout="centered" ->keeps UI centered on page 

st.title("Recruitment AI Agent")
st.subheader("Automate Resume Screening with AI")
#Big title at the top of the app 
#Subtitle under it 

#------User Input------ 
job_description=st.text_area(
    "Paste the Job Description Here",
    height=200,
    placeholder="e.g.., We are looking for a python developer with skills in NLP, machine learning"
)
#Creates a multiline input box where the recruiter pastes the job 
uploaded_resume=st.file_uploader(
    "Uploaded Resumes (.pdf or .txt)"
    ,type=["pdf","txt"],
    accept_multiple_files=True
)
if st.button("Screen Candidate",use_container_width=True):
    if job_description and uploaded_resume:
        with st.spinner("Screening candidate..."):
           job_skills=extract_skills_agent(job_description)
           candidate_results=[]
           for resume_file in uploaded_resume:
               file_extension=resume_file.name.split(".")[-1].lower()
               if file_extension=="pdf":
                   resume_text=parse_resume_pdf_agent(resume_file) 
               elif file_extension=="txt":
                   resume_text=parse_resume_pdf_agent(resume_file)
               else:
                   st.warning(f"Skipping unsupported file type: {resume_file.name}")
                   continue 
               resume_skills=extract_skills_agent(resume_text)
               score=calculate_score_agent(resume_skills,job_skills)
               candidate_results.append({
                   "Candidate Name":get_candidate_name_agent(resume_text),
                   "Match Score":score,
                   "File Name":resume_file.name,
                   "Matching Skills": ", ".join(resume_skills.intersection(job_skills)),
                   
               })    
               
        candidate_results.sort(key=lambda x: x["Match Score"], reverse=True)
        st.success("Screening Complete ")
        st.markdown("----")
        st.header("Ranking of Candidates")
        df=pd.DataFrame(candidate_results)
        st.dataframe(df,use_container_width=True)
        st.markdown("---")
        st.header("Detailed Analysis")
        for candidate in candidate_results:
            st.subheader(f"Analysis for {candidate['Candidate Name']}")  
            st.metric("Match Score",f"{candidate["Match Score"]}%")
            st.markdown("**Matching Skills**")
            if candidate["Matching Skills"]:
                st.code(candidate["Matching Skills"])
            else:
                st.warning("No Skills Match")
    else:
        st.warning("Please provide a job description and upload at least one resume.")
                            