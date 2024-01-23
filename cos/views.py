from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from django.shortcuts import render

# from django.conf import settings
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    
)
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
# from langchain.output_parsers import PydanticOutputParser
# from pydantic import BaseModel, Field
# from langchain.output_parsers import CommaSeparatedListOutputParser
# import tkinter as tk
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
# from tkinter import messagebox
# import re
# import requests
# from langchain.text_splitter import CharacterTextSplitter
chat = ChatOpenAI(openai_api_key="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",temperature=0,)
import os
os.environ["OPENAI_API_KEY"]="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"
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
# from datetime import datetime
import json
# import cx_Oracle
# Create your views here.

def error_details_generator(error_info, error_code):
    sytem_template = '''You are the oracle ebs expert in solving the error. Give the highly detailed discription on error. 
    Write the information of the error based on the details of the error mentioned below : 
    
    error code : {error_code} ,
    modeule : {module}
    Applies to : {app_to}
    Symptoms : {symp}
    Cause : {cause}
    Solution : {solu}
    Do not write sql quries
    '''
    system_message_prompt = SystemMessagePromptTemplate.from_template(sytem_template)
    chat_promt_1 = ChatPromptTemplate.from_messages([system_message_prompt])
    request = chat_promt_1.format_prompt(error_code= error_code ,module = error_info[error_code]["Module"] , app_to =  error_info[error_code]["Applies To"],
                                         symp = error_info[error_code]["Symptoms"], cause = error_info[error_code]["Cause"], solu = error_info[error_code]["Solution"] ).to_messages()
    result = chat(request)
    result = result.content
    return result

def home(request):
    return render(request, 'cos/home.html',)

class error_code_response(APIView):
    def post(self, request):
        input_data = request.data.get('user_input', None)

        with open('cos/error.json', 'r') as file:
            error_data = json.load(file)

        result = error_details_generator(error_data, input_data)
        place_holder= error_data[input_data]['place_holder']
        context = {"result": {"error_result":result,"place_holder":place_holder}}
        return Response(context)

    
class place_holders(APIView):

    def post(self, request):
        user_input = request.data.get('user_input', None)
        input_place_holders = request.data.get('place_holders', None)

        with open('cos/error.json', 'r') as file:
            error_data = json.load(file)

        place_holder = error_data[user_input]['place_holder']
        replaced_queries = []

        for key , values in error_data[user_input]['check_list'].items():
            for i in range(len(place_holder)):
                if place_holder[i] in values[1]:
                    values[1]= values[1].replace(place_holder[i],input_place_holders[i])
                a= values[1]

            replaced_queries.append(a)

        # query_results=[]
 
 
        # for query in replaced_queries:
        #     wrapped_query= f"SELECT CASE WHEN EXISTS ({query}) THEN 0 ELSE 1 END AS result FROM dual;"
        #     cleaned_query = wrapped_query.replace(',', '').replace(';', '').replace('"', '')
 
        #     try:
        #         oracle_db_config = settings.DATABASES['oracledb']
        #         with cx_Oracle.connect(
        #             user=oracle_db_config['USER'],
        #             password=oracle_db_config['PASSWORD'],
        #             dsn=f"{oracle_db_config['HOST']}:{oracle_db_config['PORT']}/{oracle_db_config['NAME']}",
        #             encoding='UTF-8'
        #         ) as connection:
        #             cursor = connection.cursor()
                   
        #             cursor.execute(cleaned_query)
        #             result = cursor.fetchall()
        #             query_results.append({'query': query, 'result': result})
        #     except cx_Oracle.DatabaseError as e:
        #         error, = e.args
        #         query_results.append({'query': query, 'error': f"Error executing query: {error.message}"})
        return Response({'replaced_queries': replaced_queries})

