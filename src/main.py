"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Three distinct user preference profiles
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.3,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "likes_acoustic": False,
        },
        "Nostalgic Jazz": {
            "genre": "jazz",
            "mood": "nostalgic",
            "energy": 0.4,
        },
        # --- Adversarial / Edge Case Profiles ---
        "Sad but Hyper (Contradictory)": {
            # High energy + sad mood: tests if mood weight overpowers energy
            "genre": "pop",
            "mood": "melancholic",
            "energy": 0.95,
            "likes_acoustic": False,
        },
        "Ghost Genre (Nonexistent)": {
            # Genre not in dataset: tests graceful fallback to mood/energy
            "genre": "k-pop",
            "mood": "happy",
            "energy": 0.7,
            "likes_acoustic": False,
        },
        "Zero Energy Rocker (Conflicting)": {
            # Rock/intense typically high energy, but user wants near-zero
            "genre": "rock",
            "mood": "intense",
            "energy": 0.05,
            "likes_acoustic": True,
        },
        "Wants Everything (Greedy)": {
            # Acoustic + high energy + happy: very few songs match all at once
            "genre": "folk",
            "mood": "happy",
            "energy": 0.95,
            "likes_acoustic": True,
        },
    }

    for profile_name, user_prefs in user_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  {profile_name.upper()} RECOMMENDATIONS")
        print(f"  Genre: {user_prefs['genre']} | Mood: {user_prefs['mood']} | Energy: {user_prefs['energy']}")
        print("=" * 50 + "\n")

        for i, rec in enumerate(recommendations, 1):
            song, score, reasons = rec
            print(f"  #{i}")
            print(f"  Title:   {song['title']}")
            print(f"  Artist:  {song['artist']}")
            print(f"  Score:   {score:.2f}")
            print(f"  Reasons: {reasons}")
            print()


if __name__ == "__main__":
    main()
