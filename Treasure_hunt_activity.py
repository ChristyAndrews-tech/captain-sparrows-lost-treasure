import streamlit as st
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Captain Sparrow's Lost Treasure",
    page_icon="🏴‍☠️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "started" not in st.session_state:
    st.session_state.started = False

if "pirate_name" not in st.session_state:
    st.session_state.pirate_name = ""

if "step" not in st.session_state:
    st.session_state.step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "clues_used" not in st.session_state:
    st.session_state.clues_used = {}

if "progress" not in st.session_state:
    st.session_state.progress = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False
    }

if "error" not in st.session_state:
    st.session_state.error = ""

if "console" not in st.session_state:
    st.session_state.console = ">>> Ready..."


# ---------------- CLUE SYSTEM ----------------

def use_clue(challenge_id, clue_text):
    if not st.session_state.clues_used.get(challenge_id, False):
        st.session_state.clues_used[challenge_id] = True
        st.session_state.score -= 5

    st.session_state.console = f"""💡 CLUE:

{clue_text}
"""

def save_score():
    file = "scores.csv"

    new_data = pd.DataFrame([{
        "Pirate": st.session_state.pirate_name,
        "Score": st.session_state.score
    }])

    if os.path.exists(file):
        old = pd.read_csv(file)
        old = pd.concat([old, new_data], ignore_index=True)
        old.to_csv(file, index=False)
    else:
        new_data.to_csv(file, index=False)    

# ---------------- PIRATE THEME CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #0B1F3A;
    color: white;
}

.main-title {
    text-align: center;
    font-size: 40px;
    color: #D4AF37;
    font-weight: bold;
    margin-bottom: 10px;
}

.card {
    background-color: #F5E8C7;
    color: black;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}

.console {
    background-color: black;
    color: #00FF66;
    padding: 15px;
    border-radius: 10px;
    font-family: monospace;
    height: 300px;
    overflow-y: auto;
}

.map {
    background-color: #162544;
    padding: 15px;
    border-radius: 10px;
}

button {
    background-color: #D4AF37 !important;
    color: black !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🏴‍☠️ Captain Sparrow\'s Lost Treasure</div>', unsafe_allow_html=True)

# ---------------- START SCREEN ----------------
if not st.session_state.started:

    st.markdown("""
    <div class="card">
    <h3>📜 Prologue</h3>
   Captain Sparrow, the most feared pirate to ever sail the seas, hid a treasure worth millions on a mysterious island.<br><br>
    He tore his treasure map into five pieces and hid each one at a different location.<br><br>
    Only those who can solve the island's Python challenges will recover every map piece.<br><br>
    Will you succeed where every pirate before you has failed...<br>
    ...and become the next Pirate Legend?
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Enter Pirate Name")

    if st.button("🏴‍☠️ Begin Adventure"):
        if name.strip() != "":
            st.session_state.pirate_name = name
            st.session_state.started = True
            st.session_state.console = f">>> Welcome aboard, Captain {name}!"
            st.rerun()
        else:
            st.warning("Enter your pirate name first!")

# ---------------- MAIN GAME LAYOUT ----------------
else:

    col1, col2, col3 = st.columns([1, 2, 1])

    # ---------------- LEFT PANEL (MAP) ----------------
    with col1:
        st.markdown("### 🗺 Treasure Map")

        for i in range(1, 6):
            if st.session_state.progress[i]:
                st.write(f"✅ Location {i}")
            else:
                st.write(f"⬜ Location {i}")

        st.write("---")

        st.markdown("### 🧩 Pieces Collected")
        pieces = sum(st.session_state.progress.values())
        st.write("🧩 " * pieces + "⬜ " * (5 - pieces))

        st.write("---")
        st.markdown("### ⭐ Score")
        st.write(st.session_state.score)

    # ---------------- CENTER PANEL ----------------
    with col2:
        st.markdown(f"### ⚓ Welcome, Captain {st.session_state.pirate_name}")
        st.info("Your adventure begins. Solve challenges to recover the lost treasure map.")

        
        # ---------------- CHALLENGE 1 STATE ----------------
        if "c1_done" not in st.session_state:
            st.session_state.c1_done = False
        if "c2_done" not in st.session_state:
            st.session_state.c2_done = False
        # ---------------- HELPER FUNCTION ----------------
        def update_console(msg):
            st.session_state.console = msg
        # ---------------- CHALLENGE 1 ----------------
        if not st.session_state.c1_done:
            st.markdown("### ⚓ Challenge 1 – The Dock")

            st.markdown("""
                Captain Sparrow's legendary ship **Midnight Pearl** is hidden among docked ships.  
                Find it to recover the first map piece.
                """)

            st.code("""
                ships = [
                    "Sea Wolf",
                    "Ocean Queen",
                    "Midnight Pearl",
                    "Crimson Tide"
                ]

                captain_ship = ships[____]

                print(__________)
                """, language="python")

            c1_blank1 = st.text_input("Blank 1", key="c1b1")
            c1_blank2 = st.text_input("Blank 2", key="c1b2")

            st.button(
                    "💡 Need a Clue (-5 points)",
                    key="clue1",
                    on_click=use_clue,
                    args=(1, "Think about how lists are indexed in Python." )
                )    

            if st.button("Submit Challenge 1"):
                if c1_blank1.strip() == "2" and c1_blank2.strip() == "captain_ship":
                    st.session_state.c1_done = True
                    st.session_state.progress[1] = True
                    st.session_state.score += 20

                    update_console(f""">>> Correct!

                    🧩 Map Piece Acquired
                    Score +20

                    Captain {st.session_state.pirate_name}, the map reveals the Abandoned Camp...
                    """)

                    st.rerun()

                else:
                    update_console("""Traceback (most recent call last):
                    File "<challenge1>", line 2

                    NameError:
                    Incorrect answer. Try again.
                    """)

        # ---------------- CHALLENGE 2 ----------------
        elif not st.session_state.c2_done:
            st.markdown("### 🧭 Challenge 2 – Abandoned Camp")

            st.markdown("""
                Old supplies are scattered across the camp.  
                Count the number of compasses left behind.
                """)

            st.code("""
                supplies = [
                    "Lantern",
                    "Compass",
                    "Sword",
                    "Compass",
                    "Map"
                ]

                compass_count = supplies.____________

                print(____________)
                """, language="python")

            c2_blank1 = st.text_input("Blank 1", key="c2b1")
            c2_blank2 = st.text_input("Blank 2", key="c2b2")

            st.button(
                    "💡 Need a Clue (-5 points)",
                    key="clue2",
                    on_click=use_clue,
                    args=(2, "Look at the list method used to find repeated items.")
                   )    

            if st.button("Submit Challenge 2"):

                if c2_blank1.strip() == "count('Compass')" and c2_blank2.strip() == "compass_count":
                    st.session_state.c2_done = True
                    st.session_state.progress[2] = True
                    st.session_state.score += 20

                    update_console(f""">>> Correct!

                        🧩 Map Piece Acquired
                        Score +20

                        Captain {st.session_state.pirate_name}, the jungle trail awaits...
                        """)

                    st.rerun()

                else:
                    update_console("""Traceback (most recent call last):

                       File "<challenge2>", line 2

                       NameError:
                       Incorrect answer. Try again.
                       """)

        # ---------------- CHALLENGE 3 ----------------
        elif st.session_state.progress[1] and st.session_state.progress[2] and not st.session_state.progress[3]:

            st.markdown("### 🔑 Challenge 3 – Pirate Hideout")

            st.markdown("""
                Deep inside the hideout, only one pirate holds the **Golden Key**.
                Find it from the pirate records.
                """)

            st.code("""
                pirates = {
                    "Finn":{"item":"Sword","gold":120},
                    "Henry":{"item":"Golden Key","gold":80},
                    "Jack":{"item":"Compass","gold":50}
                }

                key = pirates[________][________]

                print(________)
                """, language="python")

            c3b1 = st.text_input("Blank 1", key="c3b1")
            c3b2 = st.text_input("Blank 2", key="c3b2")
            c3b3 = st.text_input("Blank 3", key="c3b3")


            st.button(
                    "💡 Need a Clue (-5 points)",
                    key="clue3",
                    on_click=use_clue,
                    args=(3, "You first select a pirate, then access their stored information.")
                    )    

            if st.button("Submit Challenge 3"):

                if c3b1.strip() == "Henry" and c3b2.strip() == "item" and c3b3.strip() == "key":
                    st.session_state.progress[3] = True
                    st.session_state.score += 20

                    st.session_state.console = f""">>> Correct!

                                 🧩 Map Piece Acquired
                                 Score +20

                                 Captain {st.session_state.pirate_name}, the jungle trail awaits...
                                 """

                    st.rerun()

                else:
                    st.session_state.console = """Traceback (most recent call last):

                                 File "<challenge3>", line 2

                                 NameError:
                                 Incorrect answer. Try again.
                                 """

        # ---------------- CHALLENGE 4 ----------------
        elif st.session_state.progress[3] and not st.session_state.progress[4]:

            st.markdown("### 🌴 Challenge 4 – Jungle Trail")

            st.markdown("""
                Three paths lie ahead. Only one leads safely forward.
                """)

            st.code("""
                paths = [
                    {"name":"Path A","danger":"Crocodiles"},
                    {"name":"Path B","danger":"Quicksand"},
                    {"name":"Path C","danger":"Safe"}
                ]

                for path in paths:
                    if _________________________:
                        print("Ancient Temple Found")
                """, language="python")

            c4b1 = st.text_input("Blank 1", key="c4b1")
    


            st.button(
                    "💡 Need a Clue (-5 points)",
                    key="clue4",
                    on_click=use_clue,
                    args=(4, "Check the condition that identifies the safe path.")
                     )    

            if st.button("Submit Challenge 4"):
                if c4b1.strip() == 'path["danger"] == "Safe"':

                    st.session_state.progress[4] = True
                    st.session_state.score += 20

                    st.session_state.console = f""">>> Correct!

                         🧩 Map Piece Acquired
                         Score +20

                         Captain {st.session_state.pirate_name}, the final temple awaits...
                         """

                    st.rerun()

                else:

                    st.session_state.console = """Traceback (most recent call last):

                         File "<challenge4>", line 3

                         NameError:
                         Incorrect answer. Try again.
                         """

        # ---------------- CHALLENGE 5 ----------------
        elif st.session_state.progress[4] and not st.session_state.progress[5]:

            st.markdown("### 🏛 Final Challenge – Ancient Temple")

            st.markdown("""
                  Two ancient scrolls reveal treasure chests.
                  Only the common chest holds the final treasure.
                  """)

            st.code("""
                  all_chests = {
                     "Wooden Chest",
                     "Silver Chest",
                     "Golden Chest",
                     "Iron Chest"
                 }

                     treasure_chests = {
                     "Golden Chest",
                     "Crystal Chest"
                 }

                  final_chest = ______________

                  print(____________)
                  """, language="python")

            c5b1 = st.text_input("Blank 1", key="c5b1")
            c5b2 = st.text_input("Blank 2", key="c5b2")

            st.button(
                      "💡 Need a Clue (-5 points)",
                      key="clue5",
                      on_click=use_clue,
                      args=(5, "Think about the operation used to combine or compare sets.")
                     )    

            if st.button("🏛 Unlock Treasure"):

                if (c5b1.strip() in ["all_chests & treasure_chests", "all_chests.intersection(treasure_chests)"]) and c5b2.strip() == "final_chest":

                    st.session_state.progress[5] = True
                    st.session_state.score += 20

                    st.session_state.console = ">>> Correct!\n\n🧩 Map Fully Restored!"

                    st.rerun()

                else:

                    st.session_state.console = """Traceback (most recent call last):

                      File "<challenge5>", line 2

                      NameError:
                      Incorrect answer. Try again.
                      """

        # ---------------- FINAL SCREEN ----------------
        elif st.session_state.progress[5]:

            save_score()

            st.balloons()

            st.markdown("## 🏴‍☠️ The Treasure is Revealed!")

            st.markdown(f"""
                🎉 Congratulations, Captain {st.session_state.pirate_name}!

                🧩 You recovered all five pieces of Captain Sparrow's treasure map.

                💰 You uncovered the legendary treasure.

                ⭐ **Final Score: {st.session_state.score} / 100**

                👑 **You have become the next Pirate Legend!**
                """)            

    # ---------------- RIGHT PANEL (CONSOLE) ----------------
    with col3:

        st.markdown("### 🐍 Console")

        st.markdown(f'<div class="console">{st.session_state.console}</div>', unsafe_allow_html=True)
