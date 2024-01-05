import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import spacy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import mysql.connector

# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

def calculate_cosine_similarity(text1, text2):
    tokens1 = nlp(text1)
    tokens2 = nlp(text2)
    similarity = cosine_similarity([tokens1.vector], [tokens2.vector])[0][0]
    return similarity

def calculate_bert_similarity(text1, text2):
    model = SentenceTransformer('bert-base-uncased')
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    cosine_similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
    return cosine_similarity_score

def calculate_cosine_similarity_for_dataset(text, dataset_column):
    z = []
    for i in dataset_column:
        similarity = calculate_cosine_similarity(text, i)
        z.append(similarity)
    return z

def calculate_bert_similarity_for_dataset(text, dataset_column):
    model = SentenceTransformer('bert-base-uncased')
    embeddings1 = model.encode(text, convert_to_tensor=True)
    
    z = []
    for i in dataset_column:
        embeddings2 = model.encode(i, convert_to_tensor=True)
        cosine_similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
        z.append(cosine_similarity_score)
    return z

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="supes"
)

query = "SELECT goal FROM customer ORDER BY goal DESC LIMIT 1"
data = pd.read_sql_query(query, conn)
# Sample paragraphs
paragraph1 = "ESG stands for Environmental, Social, and Governance, and it is a set of criteria used to evaluate a company's performance and impact in these three key areas..."
paragraph2 = data['goal'][0]


cosine_scores = calculate_cosine_similarity_for_dataset(paragraph1, paragraph2)
#bert_scores = calculate_bert_similarity_for_dataset(paragraph1, paragraph2)
print(cosine_scores)

#=========================climate==========================
import pyowm

def get_weather_information(api_key, location):
    owm = pyowm.OWM(api_key)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)
    w = observation.weather
    
    # Get temperature in Celsius
    temperature_celsius = w.temperature('celsius')['temp']

    wind_speed = w.wind()["speed"] * 3.6
    
    rainfall = w.rain.get('1h', 0)
    
    humidity = w.humidity
    
    weather_status = w.status
    
    return {
        'temperature_celsius': temperature_celsius,
        'wind_speed': wind_speed,
        'rainfall_mm': rainfall,
        'humidity_percentage': humidity,
        'weather_status': weather_status
    }


query = "SELECT location FROM customer ORDER BY goal DESC LIMIT 1"
data = pd.read_sql_query(query, conn)
weather_info = get_weather_information('c810411163f49a394df7ac5c7ad97c51', data['location'][0])

# Print the weather information
print(f"Temperature: {weather_info['temperature_celsius']}°C")
print(f"Wind Speed: {weather_info['wind_speed']} km/hr")
print(f"Rainfall: {weather_info['rainfall_mm']} mm")
print(f"Humidity: {weather_info['humidity_percentage']}%")
print(f"Weather Status: {weather_info['weather_status']}")

conn.close()
