# README - LLM-Powered-Booking-Analytics-QA-System

## Approach
The solution was implemented in the following steps:
1. **Data Collection & Preprocessing**
   - Loaded hotel booking data from `hotel_bookings.csv`.
   - Cleaned the dataset by handling missing values and formatting date fields.
   - Structured data for analysis and retrieval.

2. **Analytics & Reporting**
   - Implemented revenue trend analysis over time.
   - Calculated cancellation rates.
   - Analyzed booking distributions based on geography.
   - Computed lead time statistics for bookings.

3. **Retrieval-Augmented Question Answering (RAG)**
   - Embedded booking data using `all-MiniLM-L6-v2` from Sentence Transformers.
   - Used FAISS for efficient similarity search.
   - Built a query interface to retrieve relevant bookings based on user input.

4. **API Development**
   - Built a REST API using FastAPI.
   - Created endpoints for analytics and retrieval.

## Prerequisites
- Python 3.8+
- pip
- Required Python libraries:
    pandas
    numpy
    fastapi
    pydantic
    faiss
    sentence_transformers
    nest_asyncio
  ```sh
  pip install fastapi uvicorn pandas numpy sentence-transformers faiss-cpu pydantic nest_asyncio
  ```

## Running the API
```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Running the API on WebBrowser
http://127.0.0.1:8000/docs

## API Endpoints
### 1. Analytics Endpoint
- **POST `/analytics`**
- Returns revenue trends, cancellation rates, booking distributions, and lead time statistics.

### 2. Retrieval Endpoint
- **POST `/ask`**
- Accepts a query and retrieves relevant bookings using FAISS.

### Example Request
```json
POST http://127.0.0.1:8000/ask
{
    "query": "Booking from France in January 2022"
}
```

### Example Response
```json
{
    "answer": "Relevant booking found at index 45"
}
```

## Implementation Challenges
- **Data Cleaning**: Handling missing values and formatting inconsistencies.
- **FAISS Optimization**: Efficiently indexing booking data for fast retrieval.

## Contact
For any queries, feel free to reach out at manangarg764@gmail.com.

