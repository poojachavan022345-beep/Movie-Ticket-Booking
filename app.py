from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOVIES = [
    "Avengers: Endgame",
    "Spider-Man: No Way Home",
    "Interstellar",
    "The Dark Knight"
]
TIMINGS = ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"]
PRICE_PER_TICKET = 200

class Booking(BaseModel):
    movie_index: int
    timing_index: int
    tickets: int
    name: str
    phone: str

class AIRequest(BaseModel):
    query: str

@app.get("/")
def serve_home():
    return FileResponse("index.html")

@app.get("/config")
def get_config():
    return {"movies": MOVIES, "timings": TIMINGS, "price": PRICE_PER_TICKET}

@app.post("/book")
def book_ticket(b: Booking):
    if not (0 <= b.movie_index < len(MOVIES)) or not (0 <= b.timing_index < len(TIMINGS)):
        raise HTTPException(status_code=400, detail="Invalid selection")
    if b.tickets <= 0:
        raise HTTPException(status_code=400, detail="Tickets must be greater than zero")

    total = b.tickets * PRICE_PER_TICKET
    return {
        "booking_id": f"TKT-{os.urandom(3).hex().upper()}",
        "name": b.name,
        "phone": b.phone,
        "movie": MOVIES[b.movie_index],
        "timing": TIMINGS[b.timing_index],
        "tickets": b.tickets,
        "price_per_ticket": PRICE_PER_TICKET,
        "total_amount": total
    }

@app.post("/ai-recommend")
def ai_recommend(req: AIRequest):
    q = req.query.lower()
    if any(k in q for k in ["space", "sci-fi", "science", "mind", "physics"]):
        rec = "Interstellar"
        desc = "A thrilling trip through space, black holes, and the Fourth Dimension."
    elif any(k in q for k in ["dark", "batman", "crime", "joker", "serious"]):
        rec = "The Dark Knight"
        desc = "A gritty psychological crime thriller set in Gotham City."
    elif any(k in q for k in ["superhero", "thanos", "avengers", "action"]):
        rec = "Avengers: Endgame"
        desc = "The ultimate Marvel clash to save the universe."
    else:
        rec = "Spider-Man: No Way Home"
        desc = "Action-packed, humorous, and full of multiversal nostalgia."

    return {"recommended_movie": rec, "reason": desc}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
