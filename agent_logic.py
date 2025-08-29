import spacy
#spacy is an NLP LIbrary in python 
#Helps computers understand,process, and analyze human language text 
#Thinks of it like a toolbox for text tokenization 
#named entity recognition, (Detects entities-->ex:Python:language,Machine-learning:field)
#part-of-speech tagging, dependency parsing 
from pypdf import PdfReader
#Imports pdfreader class from pypdf library to read PDF files
#use :To extract text from PDF files 
import io 
#Providea tools to work with streams ,like files in memory
#Use: Here , to handle PDF files uploaded as bytes (in-memory files objects)


# Load the spaCy model for English language processing
# try:
#     nlp = spacy.load("en_core_web_sm")
#     #Loads a small English language NLP model en_core_web_sm from spaCy 
#     #nlp is a variable that will noe hold a reday-to-use NLP pipeline
# except OSError:
#     print("Downloading spacy model...")
#     spacy.cli.download("en_core_web_sm")
#     #In spacy, spacy.cli is a module that contians functions
#     #you normally run from the terminal/command line
#     #Downloads the nlp model .Happens only once on the system 
nlp = spacy.load("en_core_web_sm") 
    #Loads the model again after downloading ,so we can use it immediately 


#The Resume Parsing Agent functions 
def parse_resume_pdf_agent(pdf_file):
    """Extracts text form a PDF file"""   
    try:
        reader=PdfReader(io.BytesIO(pdf_file.read()))
        #pdf_file.read(...)--> reads the entire content of the uploaded PDF file as bytes
        #io.BytesIO(....) --> Converts the bytes into an in-memory file-like objects 
        #PdfReader(....) --> Creates a PDF Reader object to read pages 
        text=""
        #Initialize an empty string to hold the extracted text 
        for page in reader.pages:
            text+=page.extract_text() or ""
            #page.extract_text()--> Extracts text from each page 
            #or "" --> Ensures that if no text is found, an empty string is added instead of None 
        return text
        #Returns the complete extracted text from all pages 
    except Exception as e: 
        return f"Error reading PDF file: {e}"      
def parse_resume_txt_agent(txt_file):
    """Extracts text from a TXT file"""
    return txt_file.read().decode("utf-8")
   #txt.file.read() --> Reads the entire content of the uploaded TXT file as bytes 
   #.decode("utf-8") --> converts the bytes into a UTF-8 string and returns it.(normal Python text) 
   #Returns the decoded text content 


#The skill Extraction Agent function
def extract_skills_agent(text):
    """Extracts skills from text using a pre-trained list"""
    skills_list=[
        "python","r","sql","pandas","numpy","scikit-learn","tableau",
        "power bi","statistics","data cleaning","java","machine learning",
        "nlp","flask","django","fastapi","git","docker","blockchain","web development",
        "backend","data analysis","predictive modeling"
    ]
    #A predefined list of skills to look for in the resume 
    
    doc=nlp(text.lower()) 
    #Converts text to lowercase ->text.lower() 
    #Passes it to nlp(...) -->spaCy breaks the text into tokens ,sentences etc 
    found_skills={token.text for token in doc if token.text in skills_list}
    #Set comprehension to find skills 
    #Loops over each token in the text  
    #If token is in the skills_list ,include it in found_skills. 
    #{...} creates a set of unique skills found
    return found_skills 
    #Returns the set of found skills 

#The Candidate Information Agent funcion  
def get_candidate_name_agent(resume_text):
    """Extracts a simple name from the first few lines of the text"""
    lines=resume_text.strip().split("\n") 
    #.strip() removes leading/trailing whitespace
    #.split("\n") splits the text into a list of lines 
    if lines:
    #checks if the list is not empty
        return lines[0].strip()    
        #Returns the first line as the candidate's name (removing extra spaces)
    return "Unknown Candidate"
    #If no lines found, return "Unknown Candidate" 
    
#The Scoring & Ranking Agent function 
def calculate_score_agent(resume_text,job_skills):
    """Calculates a match score based on shared skills"""
    if not job_skills:
        return 0.0 
        #If job_skills is empty, return a score of 0.0 
    matching_skills=resume_text.intersection(job_skills) 
    #Finds the common skills between resume_skills and job_skills 
    score=len(matching_skills)/len(job_skills)*100 
    #Calculates the match score as a percentage
    return round(score,2)            
    #Returns the score rounded to 2 decimal places 
    
