
import csv
import google.generativeai as genai
import sql
import time
import yaml

with open('data/api_key.yaml', 'r') as file:
    config = yaml.safe_load(file)
    API_KEY = config.get('api_key')
    
# create an AI model
def create_model(instruction):
    genai.configure(api_key = API_KEY)
    model = genai.GenerativeModel(
        model_name = "gemini-1.5-flash",
        system_instruction = instruction
        )
    
    # return the newly created model
    return model

# strip formatting tags off of the returned SQL query
def clean_query(query):
    # Strip the 'sqlite' tag and backticks from the input string
    cleaned_query = query.strip().replace('```sqlite', '').replace('```', '').strip()
    return cleaned_query

# convert natural language to an SQLite query
def convert_language_to_sql(prompt):
    # instructions for the converter model
    instruction = '''Your job is to convert a natural language question to an SQLite query. Use the provided database schema to make the queries. When building the query, be very liberal with how much data you SELECT. Always JOIN PlayerStats and GameInfo to get the most information as possible. JOIN multiple tables together if necessary. Provide no other output other than the final SQL query.
            SCHEMA:
            CREATE TABLE IF NOT EXISTS Players (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Number INT, HomeCity TEXT, HomeState TEXT, Height TEXT, Weight INT, BirthYear INT, BirthMonth INT, BirthDay INT)
            CREATE TABLE IF NOT EXISTS PlayerStats (id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Team TEXT, Name TEXT, Minutes INT, FGM INT, FGA INT, TFGM INT, TFGA INT, FTM INT, FTA INT, ORB INT, DRB INT, TRB INT, PF INT, AST INT, STL INT, BLK INT, TOV INT, PTS INT)
            CREATE TABLE GameInfo (id INTEGER PRIMARY KEY AUTOINCREMENT, Date DATE, Day TEXT, Season TEXT, Opponent TEXT, Result TEXT, Location TEXT, UKScore INT, OppScore INT, Notes TEXT, Arena TEXT, Attendance INT, City TEXT, UKHalfScore INT, OppHalfScore INT, OTS INT, UKRank INT, OppRank INT, OppCoach TEXT, OppConference TEXT, LeadScorer TEXT, LeadScorerPoints INT, LeadRebounder TEXT, LeadRebounderRebs INT, LeadAssister TEXT, LeadAssisterAsts INT, LeadStealer TEXT, LeadStealerSteals INT, LeadBlocker TEXT, LeadBlockerBlocks INT)
        '''
    # create the model
    model = create_model(instruction)
    
    # return the model's response to the prompt
    return clean_query(model.generate_content(prompt).text)

# presents the results in conversational format
def results_cleaner(question, answer):
    if answer == "None":
        return "No response possible."
    else:
        # instructions for the response model
        instruction = '''You will receive a prompt in the format:
            QUESTION: <question the user asked>
            ANSWER: <answer to the user's question>
            
            Provide a response that communicates the answer to the user's question. Do NOT respond with JSON data. Convert dates to string format. Assume that the user always wants to know as much information about the game(s) as possible.
        '''
        
        # create the model
        model = create_model(instruction)
        
        # return the model's response to the prompt
        return model.generate_content(f'''
                                    QUESTION: {question}
                                    ANSWER: {answer}
                                    ''').text[:-1]  

def main():
    # ask the user to enter their prompt
    prompt = str(input("Enter the information you'd like to find... "))
    # obtain the prompt's corresponding SQL query
    sql_query = convert_language_to_sql(prompt)
    
    # create a connection to the database
    cursor = sql.sqlite3.connect('ukgames2.db').cursor()
    # query the database and get the response
    try:
        sql_response = sql.run_query(cursor, sql_query)    
    except:
        print("Something went wrong when running the query. Please try again.")
        sql_response = "None"
        
    # print the final response
    print(results_cleaner(prompt, sql_response))
    
if __name__ == "__main__":
    main()