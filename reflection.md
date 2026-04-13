# Reflection: Comparing User Profile Outputs

Below are comparisons between pairs of user profiles, explaining what changed in the recommendations and why. Written in plain language so anyone — programmer or not — can follow along.

---

## High-Energy Pop vs. Chill Lofi

These two profiles are almost opposites. The Pop listener wants upbeat, loud, danceable songs (energy 0.9), while the Lofi listener wants quiet, relaxed background music (energy 0.3) and prefers acoustic sounds. The results reflect this perfectly: High-Energy Pop gets "Sunrise City" and "Gym Hero" — both fast, poppy tracks with high danceability. Chill Lofi gets "Library Rain" and "Midnight Coding" — soft, acoustic tracks you might study to. There is zero overlap in their top 5, which makes sense because these listeners want completely different vibes. This is the system working as intended.

---

## High-Energy Pop vs. Sad but Hyper (Contradictory)

Both profiles list "pop" as their genre and have high energy (0.9 vs. 0.95), but the Sad but Hyper profile asks for a "melancholic" mood instead of "happy." You would expect a very different list — sad pop songs instead of party anthems. But the results are almost the same: "Gym Hero" and "Sunrise City" dominate both lists. Why? Because the system gives 40% of the score to genre alone, so any pop song gets a huge head start regardless of mood. "Gym Hero" is not a sad song at all — it is an intense workout track — but it keeps showing up because it checks the "pop" box and has high energy. The one melancholic song that appears (Forest Lullaby) only scores 43.35, ranking third. This shows the system does not take the "sad" preference seriously enough when the genre match is strong.

---

## High-Energy Pop vs. Ghost Genre (Nonexistent)

The Ghost Genre profile asks for "k-pop" — a genre that does not exist in our song catalog. Both profiles want happy, energetic music, but the Ghost Genre user's top score is only 56.40 compared to 97.00 for High-Energy Pop. That is a massive drop. The reason is simple: since no song matches "k-pop," the entire 40% genre weight is wasted — it contributes zero points for every single song. The system does not crash or show an error, but it silently ignores the user's main preference and just recommends whatever happens to be happy and energetic. In a real app, this would be frustrating — the user would get generic results with no explanation that their favorite genre is missing from the catalog.

---

## Chill Lofi vs. Nostalgic Jazz

Both profiles want low-energy, mellow music (0.3 and 0.4), but in different genres and moods. The Lofi listener gets a focused set of lofi tracks with high acousticness (Library Rain, Midnight Coding), while the Jazz listener's top pick is "Coffee Shop Stories" — the only jazz song in the catalog — at just 63.50. After that, the Jazz results become random: lofi tracks appear not because the user wants lofi, but because they happen to have similar energy levels. This highlights a dataset problem. Lofi has 3 songs to choose from, so the system can build a solid list. Jazz has only 1 song, so once that one is recommended, the system has nothing relevant left and just fills in whatever is closest in energy.

---

## Deep Intense Rock vs. Zero Energy Rocker (Conflicting)

These two profiles both want rock and intense mood, but their energy preferences are polar opposites: 0.85 vs. 0.05. You would expect very different songs — one wants headbangers, the other wants something like a slow, brooding rock ballad. But both get "Storm Runner" as their number one pick. For the regular Rock profile, this makes perfect sense — Storm Runner is high energy (0.91) and matches everything. For the Zero Energy Rocker, it makes no sense at all. The user specifically said they want near-silent energy, yet the loudest rock song in the catalog is still recommended at a score of 86.70. This happens because genre (40%) plus mood (30%) give Storm Runner 70 points before energy is even considered, and energy is only worth 15% of the total. The system essentially says: "You like rock and intense? Here is the only rock song we have — your energy preference does not matter."

---

## Deep Intense Rock vs. High-Energy Pop

Both want high-energy music (0.85 and 0.9), but in completely different genres and moods. The Rock listener gets Storm Runner at 98.20, while the Pop listener gets Sunrise City at 97.00 — both nearly perfect scores. Interestingly, "Gym Hero" appears in both top 5 lists. For the Pop fan, it matches on genre (pop). For the Rock fan, it matches on mood (intense). Gym Hero is like a chameleon in the system — it is a pop song tagged as intense, so it scores well for anyone who wants either pop or intense. This reveals that songs with popular tags can show up across very different user profiles, not because they truly fit, but because they happen to share one high-weight attribute.

---

## Nostalgic Jazz vs. Wants Everything (Greedy)

The Jazz profile is modest — just jazz, nostalgic mood, and mid-low energy. The Greedy profile wants folk, happy, high energy, AND acoustic all at once. The Jazz user gets a reasonable top pick (Coffee Shop Stories at 63.50), but the Greedy user's top pick (Forest Lullaby at 57.95) is actually a low-energy, melancholic folk song — not happy or high-energy at all. The system recommended it because it matched on genre (folk) and acousticness, ignoring the fact that the user also wanted happiness and high energy. This shows that when a user wants many things at once, the system satisfies the highest-weighted preferences (genre at 40%) and quietly drops the rest. A real listener would be confused to receive a sad lullaby when they asked for an upbeat acoustic folk song.

---

## Sad but Hyper vs. Zero Energy Rocker

Both are adversarial profiles with contradictory preferences, but they contradict in different ways. Sad but Hyper wants pop and melancholic mood with extreme energy — like crying on a dance floor. Zero Energy Rocker wants rock and intense mood with almost no energy — like a whispered scream. In both cases, the system ignores the contradiction and just picks songs that match genre and mood. The Sad but Hyper user gets "Gym Hero" (an upbeat workout song, not sad at all). The Zero Energy Rocker gets "Storm Runner" (one of the loudest songs in the catalog). Neither result honors the unusual energy request. This tells us the system has no way to handle conflicting preferences — it just defaults to genre and mood every time, which are the heaviest weights. Energy, danceability, and acousticness are essentially tiebreakers, not real preferences.

---

## Ghost Genre vs. Wants Everything (Greedy)

Both profiles expose edge cases, but differently. The Ghost Genre user's problem is that their favorite genre does not exist, so 40% of the scoring potential is permanently zeroed out — their best score is only 56.40. The Greedy user's problem is the opposite: their genre does exist (folk), but no single song satisfies all their preferences at once. Forest Lullaby matches folk and acoustic but has low energy and a sad mood. The Ghost Genre user at least gets recommendations that match their mood (happy), while the Greedy user gets a folk song that only satisfies 2 out of 4 preferences. Both cases show that the system does not warn users when it cannot find a good match — it just quietly returns the least-bad options and presents them as if they were solid recommendations.

---

## Summary

Across all these comparisons, a clear pattern emerges: genre is king. It controls 40% of the score and is a simple yes-or-no check, so any song in the right genre gets an enormous advantage regardless of whether it actually fits the user's other preferences. Mood (30%) is the runner-up. Together, these two categorical features decide the outcome for almost every profile. The numerical features — energy, danceability, acousticness — barely move the needle. This means the system is really a genre filter with some light mood matching on top, not a true preference-based recommender. A song like "Gym Hero" keeps appearing across wildly different profiles (Happy Pop, Sad but Hyper, Deep Intense Rock, Zero Energy Rocker) simply because it is tagged as pop and intense — two of the most requested attributes. In a real music app, this would mean certain popular-tagged songs get recommended to everyone while niche songs get buried, regardless of how well they actually match what the listener wants to hear.
