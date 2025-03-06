
from config import load_config, _parse_args
import google.generativeai as genai
import sql
import sys
    
# create an AI model
def create_model(api_key, instruction):
    genai.configure(api_key = api_key)
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
def convert_nl_to_sql(config, prompt):
    # create a model using values from the config as parameters
    model = create_model(config.gemini.api_key, config.gemini.query_instruction)
    
    # get the model's response
    response = model.generate_content(prompt).text
    
    # return a cleaned version of the model's translation of the prompt
    return clean_query(response)

# presents the results in conversational format
def results_cleaner(question, answer):
    if answer == "None":
        return "No response possible."
    else:
        # instructions for the response model
        instruction = '''You will receive a prompt in the format:
            QUESTION: <question the user asked>
            RESPONSE: <results of running SQL query>
            
            Provide a response that combines QUESTION and ANSWER into a valid conversational statement. Include as much data from ANSWER as possible.
        '''
        
        # create the model
        model = create_model(instruction)
        
        # return the model's response to the prompt
        return model.generate_content(f'''
                                    QUESTION: {question}
                                    ANSWER: {answer}
                                    ''').text[:-1]  

def main(argv = sys.argv[1:]):
    # get the config data from the command-line arguments
    args = _parse_args(argv)
    config = load_config(args.config)
    
    # ask the user to enter their prompt
    prompt = str(input("Enter the information you'd like to find... "))
    
    # obtain the prompt's corresponding SQL query
    query = convert_nl_to_sql(config, prompt)
    
    # create a connection to the database
    cursor = sql.sqlite3.connect(config.sql.db_file).cursor()
    
    # query the database and get the response
    try:
        sql_response = sql.run_query(cursor, query)
    except:
        print("Something went wrong when running the query. Please try again.")
        sql_response = "None"
    
    # print the SQL query that was generated
    print(f"SQL Query: {query}")
    # print the final response
    print(f"Response: {results_cleaner(prompt, sql_response)}")
    
if __name__ == "__main__":
    main()