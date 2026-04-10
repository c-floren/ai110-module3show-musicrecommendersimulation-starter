from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numeric fields to appropriate types
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
        
    # Feature weights (percentage values sum to 100)
    weights = {
        "genre":          0.40,
        "mood":           0.30,
        "energy":         0.15,
        "danceability":   0.10,
        "acousticness":   0.05,
    }
    
    total_score = 0.0
    reasons = []
    
    # CATEGORICAL SCORES (0 or 1)
    genre_match = 1.0 if song["genre"] == user_prefs["genre"] else 0.0
    mood_match = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
    
    if genre_match:
        reasons.append(f"Matches favorite genre: {song['genre']}")
    
    if mood_match:
        reasons.append(f"Matches favorite mood: {song['mood']}")
    
    # NUMERICAL SCORES (distance-based, 0.0-1.0)
    energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"]) / 1.0
    energy_diff = abs(song["energy"] - user_prefs["energy"])
    if energy_diff < 0.2:
        reasons.append(f"Energy level close to preference ({song['energy']:.2f})")
    
    danceability_score = 1.0 - abs(song["danceability"] - 0.7) / 1.0  # Assume neutral target = 0.7
    if song["danceability"] > 0.75:
        reasons.append(f"High danceability ({song['danceability']:.2f})")
    
    acousticness_score = 1.0 if user_prefs.get("likes_acoustic", False) else 1.0 - song["acousticness"]
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        reasons.append(f"Good acousticness match ({song['acousticness']:.2f})")

    # WEIGHTED TOTAL
    total_score = (
        genre_match * weights["genre"] * 100 +
        mood_match * weights["mood"] * 100 +
        energy_score * weights["energy"] * 100 +
        danceability_score * weights["danceability"] * 100 +
        acousticness_score * weights["acousticness"] * 100
    )
    
    # Add fallback reason if no specific matches
    if not reasons:
        reasons.append("General match based on musical attributes")
    
    # Expected return format: (score, reasons)
    return (total_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Return the top k songs ranked by score.
    Required by src/main.py
    """
    # Calculate scores for all songs using list comprehension
    scored_songs = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Return top k sorted by score descending
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
