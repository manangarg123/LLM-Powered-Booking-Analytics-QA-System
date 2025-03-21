import pandas as pd
import numpy as np
import fastapi
from fastapi import FastAPI, Query
from pydantic import BaseModel
import faiss
from sentence_transformers import SentenceTransformer
import nest_asyncio
nest_asyncio.apply()


# Load and Preprocess Data
def load_data(filepath):
    df = pd.read_csv("D:/AIML Assignment/hotel_bookings.csv")
    df.dropna(inplace=True)  # Handle missing values
    df["arrival_date"] = pd.to_datetime(df["arrival_date_year"].astype(str) + '-' + 
                                         df["arrival_date_month"] + '-' + 
                                         df["arrival_date_day_of_month"].astype(str))
    return df

# Basic Analytics
def revenue_trends(df):
    df["revenue"] = df["adr"] * df["stays_in_week_nights"]  # Ensure 'revenue' exists
    revenue_series = df.groupby(df["arrival_date"].dt.to_period("M"))["revenue"].sum()
    return revenue_series.rename_axis("month").reset_index().astype(str).set_index("month")["revenue"].to_dict()

def cancellation_rate(df):
    return df["is_canceled"].mean() * 100

def booking_distribution(df):
    return df["country"].value_counts()

def lead_time_distribution(df):
    return df["lead_time"].describe()

# Setup FAISS for RAG
model = SentenceTransformer("all-MiniLM-L6-v2")
def create_vector_store(df):
    texts = df.apply(lambda row: f"Booking from {row['country']} on {row['arrival_date']}", axis=1)
    embeddings = model.encode(texts.tolist(), convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

# FastAPI Setup
app = FastAPI()
df = load_data("hotel_bookings.csv")
vector_index = create_vector_store(df)

class QueryRequest(BaseModel):
    query: str

@app.post("/analytics")
def get_analytics():
    try:
        result = {
            "revenue_trends": revenue_trends(df),
            "cancellation_rate": cancellation_rate(df),
            "booking_distribution": booking_distribution(df).to_dict(),
            "lead_time_distribution": lead_time_distribution(df).to_dict()
        }
        print("Analytics Response:", result)  # Debugging
        return result
    except Exception as e:
        print("Error in analytics:", e)
        return {"error": str(e)}

@app.post("/ask")
def ask_question(request: QueryRequest):
    query_embedding = model.encode([request.query], convert_to_numpy=True)
    _, idx = vector_index.search(query_embedding, k=1)
    return {"answer": f"Relevant booking found at index {idx[0][0]}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
