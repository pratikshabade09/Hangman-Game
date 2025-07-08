# streamlit_app.py

import streamlit as st
import requests
import random

# --- FUNCTION TO GET RANDOM WORD ---
def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            return response.json()[0].lower()
    except:
        pass
    return random.choice(["python", "streamlit", "hangman", "code", "magic"])

# --- SESSION STATE SETUP ---
if "word" not in st.session_state:
    st.session_state.word = get_random_word()
    st.session_state.guessed = ["_"] * len(st.session_state.word)
    st.session_state.tries = len(st.session_state.word) + 2
    st.session_state.guessed_letters = []

# --- TITLE ---
st.title("🎮 Hangman Game")
st.subheader("Guess the secret word, one letter at a time!")

# --- DISPLAY HINT ---
st.write("Word: " + " ".join(st.session_state.guessed))
st.write(f"Tries left: {st.session_state.tries}")
st.write("Guessed letters: " + ", ".join(st.session_state.guessed_letters))

# --- GUESS INPUT ---
guess = st.text_input("Enter a letter:").lower()

# --- HANDLE GUESS ---
if guess and st.session_state.tries > 0 and "_" in st.session_state.guessed:
    if len(guess) != 1 or not guess.isalpha():
        st.warning("Please enter a single letter.")
    elif guess in st.session_state.guessed_letters:
        st.warning("You already guessed that!")
    else:
        st.session_state.guessed_letters.append(guess)
        if guess in st.session_state.word:
            for i in range(len(st.session_state.word)):
                if st.session_state.word[i] == guess:
                    st.session_state.guessed[i] = guess
            st.success("Correct guess!")
        else:
            st.session_state.tries -= 1
            st.error("Wrong guess!")

# --- WIN / LOSE MESSAGES ---
if "_" not in st.session_state.guessed:
    st.success(f"🎉 You won! The word was: {st.session_state.word}")
elif st.session_state.tries == 0:
    st.error(f"💀 You lost! The word was: {st.session_state.word}")

# --- RESTART BUTTON ---
if st.button("🔁 Restart Game"):
    st.session_state.word = get_random_word()
    st.session_state.guessed = ["_"] * len(st.session_state.word)
    st.session_state.tries = len(st.session_state.word) + 2
    st.session_state.guessed_letters = []
    st.experimental_rerun()
