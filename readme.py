import streamlit as st
import pandas as pd
import random
import time
import re # For highlighting words in sentences

# st.set_page_config() MUST be the first Streamlit command after imports
st.set_page_config(layout="centered", page_title="Vocabulary Practice")

# --- START AGGRESSIVE DEBUGGING ---
st.sidebar.subheader("Session State Inspector")
# Sort items for consistent display, filter out the large word list
sorted_session_state_items = sorted(st.session_state.items())
for key, value in sorted_session_state_items:
    if key not in ['all_words_loaded', 'test_questions_cache'] or not st.session_state[key]: # Avoid printing huge lists/dicts if empty
        if isinstance(value, list) and len(value) > 5: # Truncate long lists
             st.sidebar.text(f"{key}: {str(value[:5])}...")
        elif isinstance(value, dict) and len(value) > 5:
             st.sidebar.text(f"{key}: Dict with {len(value)} items (keys: {list(value.keys())[:5]}...)")
        else:
            st.sidebar.text(f"{key}: {value}")
    elif key == 'test_questions_cache' and st.session_state[key]:
        st.sidebar.text(f"{key}: Contains {len(st.session_state[key])} cached question sets.")

st.sidebar.markdown("---")
# --- END AGGRESSIVE DEBUGGING ---


# --- Helper Functions ---
@st.cache_data # Cache the data loading
def load_words():
    # PASTE YOUR FULL word_data_list HERE
    # Example structure:
    # word_data_list = [
    #     {'English Word': 'example', 'Polish Translation': 'przykład', 'Example Sentence': 'This is an example.'},
    #     {'English Word': 'apple', 'Polish Translation': 'jabłko', 'Example Sentence': 'An apple a day.'},
    #     # ... add all your words ...
    # ]
    word_data_list = [
        # For testing purposes, including a few words.
        # Replace this with your extensive list.
        {'English Word': 'a', 'Polish Translation': 'a', 'Example Sentence': 'I need a pen.'},
        {'English Word': 'abandon', 'Polish Translation': 'porzucić', 'Example Sentence': 'They had to abandon their car in the snow.'},
        {'English Word': 'ability', 'Polish Translation': 'zdolność', 'Example Sentence': 'She has the ability to learn new languages quickly.'},
        {'English Word': 'able', 'Polish Translation': 'zdolny', 'Example Sentence': 'He is able to lift heavy boxes.'},
        {'English Word': 'about', 'Polish Translation': 'o, około', 'Example Sentence': "What are you talking about? It's about five o'clock."},
        {'English Word': 'above', 'Polish Translation': 'powyżej', 'Example Sentence': 'The bird flew above the trees.'},
        {'English Word': 'accept', 'Polish Translation': 'zaakceptować', 'Example Sentence': 'I accept your offer.'},
        {'English Word': 'accident', 'Polish Translation': 'wypadek', 'Example Sentence': 'He was involved in a car accident.'},
        {'English Word': 'act', 'Polish Translation': 'czyn', 'Example Sentence': 'It was an act of kindness.'},
        {'English Word': 'address', 'Polish Translation': 'adres', 'Example Sentence': "What's your home address?"},
        {'English Word': 'dad', 'Polish Translation': 'tata', 'Example Sentence': 'My dad is picking me up from school.'},
        {'English Word': 'daily', 'Polish Translation': 'codzienny', 'Example Sentence': 'I read the daily newspaper.'},
        {'English Word': 'dance', 'Polish Translation': 'taniec', 'Example Sentence': 'She loves to dance.'},
        {'English Word': 'each', 'Polish Translation': 'każdy', 'Example Sentence': 'Each student received a book.'},
        {'English Word': 'eager', 'Polish Translation': 'chętny', 'Example Sentence': 'He was eager to learn new things.'},
        {'English Word': 'earn', 'Polish Translation': 'zarabiać', 'Example Sentence': 'How much do you earn per month?'},
    ]

    if not word_data_list:
        st.error("CRITICAL: The word_data_list in load_words() is empty! Please add your vocabulary.")
        return []
    if len(word_data_list) < 10: # Increased minimum for better distractor pool and round variety.
        st.warning(f"Warning: Word list is very small ({len(word_data_list)} words). Multiple choice questions might have repeated options or fewer than 5 options. Please add more words for a better experience.")
    return word_data_list

ALL_WORDS = load_words()

def get_new_word_set(words_list, num_words=10, seen_indices=None):
    if seen_indices is None: seen_indices = set()
    if not words_list: return [] # Handle empty initial list

    available_indices = [i for i, _ in enumerate(words_list) if i not in seen_indices]

    if len(available_indices) < num_words:
        st.sidebar.warning("Not enough new unique words for this round. Words may repeat if all have been seen.")
        if not available_indices and words_list: # If all words seen, allow repeating
            seen_indices.clear()
            st.sidebar.info("All words seen, cleared seen_words_indices for repetition.")
            available_indices = list(range(len(words_list)))
        # If still not enough (e.g. num_words > len(words_list)), sample what's available
    
    if not available_indices: return [] # No words to sample from
    
    actual_num_words_to_sample = min(num_words, len(available_indices))
    if actual_num_words_to_sample == 0: return []

    chosen_indices = random.sample(available_indices, actual_num_words_to_sample)
    new_set = [words_list[i] for i in chosen_indices]
    for i in chosen_indices: seen_indices.add(i)
    return new_set

def highlight_word_in_sentence(sentence, word_to_highlight):
    if not sentence or not word_to_highlight: return sentence
    try:
        escaped_word = re.escape(word_to_highlight)
        return re.sub(f"\\b({escaped_word})\\b", r"<span class='orange-text'>\1</span>", sentence, flags=re.IGNORECASE)
    except: return sentence

motivational_quotes = [
    "Great job! Keep learning!", "Excellent! Every step counts.", "You're doing great!",
    "Awesome! Practice makes perfect.", "Fantastic! Keep it up!", "Progress, not perfection!",
    "You're making strides!", "Each correct answer builds your knowledge!"
]

st.markdown("""
    <style>
        body, .stApp, .stButton>button, .stSelectbox div[data-baseweb='select'] > div, 
        .stTextInput > div > div > input, .stMetric > div > div, .stRadio > label {
            font-size: 18px !important;
        }
        .stSubheader { font-size: 22px !important; font-weight: bold; }
        .orange-text { color: orange; font-weight: bold; }
        .timer-text { font-size: 20px !important; font-weight: bold; color: #1E90FF; text-align: center; margin-bottom: 10px; }
        .stProgress > div > div > div > div { background-color: #1E90FF !important; }
        .example-sentence { font-size: 1.2em !important; font-style: italic; color: #444; margin-top: 5px; line-height: 1.4; }
        .stRadio > label > div:first-child { margin-right: 8px; }
        .stRadio { padding-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇬🇧 English Vocabulary Practice 🇵🇱")

# Initialize session state variables robustly
default_session_state = {
    "stage": "welcome", "all_words_loaded": ALL_WORDS if ALL_WORDS else [], "score": 0, "current_word_set": [],
    "test_answers": {}, "timer_start_time": 0, "round_number": 0, "seen_words_indices": set(),
    "current_learning_word_index": 0, "learning_word_start_time": 0,
    "quiz_direction": "Polish to English", "overall_correct_streak": 0,
    "test_questions_cache": {}
}
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value
# Ensure all_words_loaded is properly set if it was empty initially from a failed load_words()
if not st.session_state.all_words_loaded and ALL_WORDS:
    st.session_state.all_words_loaded = ALL_WORDS


# --- Main App Logic ---
if st.session_state.stage == "welcome":
    st.header("Welcome to the Vocabulary Trainer!")
    current_quiz_direction_index = ("Polish to English", "English to Polish").index(st.session_state.get("quiz_direction", "Polish to English"))
    st.session_state.quiz_direction = st.radio(
        "Select Quiz Direction:", ("Polish to English", "English to Polish"),
        index=current_quiz_direction_index, key="quiz_direction_selector"
    )
    if st.button("🚀 Start Learning"):
        if not st.session_state.all_words_loaded:
            st.error("Word list is empty or could not be loaded. Please add words to `load_words()` function in the script.")
        else:
            st.session_state.round_number += 1
            st.session_state.stage = "learning_individual"
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words_loaded, 10, st.session_state.seen_words_indices)
            st.session_state.test_questions_cache = {} # Clear cache for the new upcoming round
            if not st.session_state.current_word_set:
                st.error("Could not load new words for the round. Not enough unique words available or list is too small."); st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0; st.session_state.learning_word_start_time = time.time()
            st.rerun()

elif st.session_state.stage == "learning_individual":
    if not st.session_state.current_word_set: st.error("Word set is empty."); st.session_state.stage = "welcome"; st.rerun()
    elif st.session_state.current_learning_word_index >= len(st.session_state.current_word_set):
        st.session_state.stage = "test"; st.session_state.timer_start_time = time.time(); st.session_state.test_answers = {}; st.rerun()
    else:
        word_data = st.session_state.current_word_set[st.session_state.current_learning_word_index]
        st.header(f"🧠 Round {st.session_state.round_number}: Learn Word {st.session_state.current_learning_word_index + 1}/{len(st.session_state.current_word_set)}")
        time_elapsed_word = time.time() - st.session_state.learning_word_start_time
        time_remaining_word = max(0, 5 - int(time_elapsed_word))
        st.empty().markdown(f"<p class='timer-text'>Time for this word: {time_remaining_word}s</p>", unsafe_allow_html=True)
        english_display = word_data.get('English Word', 'N/A'); polish_display = word_data.get('Polish Translation', 'N/A'); sentence_display = word_data.get('Example Sentence', 'No example.')
        st.markdown(f"## <span class='orange-text'>{english_display}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🇵🇱 {polish_display}")
        st.markdown(f"<p class='example-sentence'>📖 Example: {highlight_word_in_sentence(sentence_display, english_display)}</p>", unsafe_allow_html=True)
        st.markdown("---")
        if time_remaining_word <= 0:
            st.session_state.current_learning_word_index += 1
            if st.session_state.current_learning_word_index < len(st.session_state.current_word_set): st.session_state.learning_word_start_time = time.time()
            st.rerun()
        else: time.sleep(1); st.rerun()

elif st.session_state.stage == "test":
    quiz_dir = st.session_state.get("quiz_direction", "Polish to English")
    test_cache_key = f"test_questions_round_{st.session_state.round_number}_{quiz_dir.replace(' ','_')}" # Ensure key is filesystem friendly

    if not st.session_state.get(test_cache_key):
        generated_questions = []
        question_lang_key = 'Polish Translation' if quiz_dir == "Polish to English" else 'English Word'
        answer_lang_key = 'English Word' if quiz_dir == "Polish to English" else 'Polish Translation'
        
        if not st.session_state.current_word_set :
            st.error("Test Error: Current word set is empty. Cannot generate questions."); st.session_state.stage="welcome"; st.rerun()

        for i, word_data in enumerate(st.session_state.current_word_set):
            question_word = word_data.get(question_lang_key, "N/A Question")
            correct_answer = word_data.get(answer_lang_key, "N/A Answer")
            options = {correct_answer}
            all_possible_answers = [w.get(answer_lang_key, "") for w in st.session_state.all_words_loaded if w] # Ensure w is not None
            distractor_pool = [ans for ans in all_possible_answers if ans and ans != correct_answer and ans != word_data.get(question_lang_key)]

            chosen_distractors = set()
            if distractor_pool:
                num_distractors_needed = 4
                # Ensure we don't try to sample more than available unique distractors
                num_to_sample = min(num_distractors_needed, len(set(distractor_pool)))
                if num_to_sample > 0:
                    chosen_distractors.update(random.sample(list(set(distractor_pool)), num_to_sample))
            
            options.update(chosen_distractors)
            final_options_list = list(options)
            
            idx = 0
            while len(final_options_list) < 5: # Pad if not enough options
                padding = f"Option {idx+1}" # More generic padding
                if padding not in final_options_list: final_options_list.append(padding)
                idx +=1
                if idx > 20 : break # Safety break for padding

            if correct_answer not in final_options_list:
                if len(final_options_list) >= 5 : final_options_list[random.randint(0,4)] = correct_answer
                elif len(final_options_list) < 5: final_options_list.append(correct_answer)
            
            final_options_list = list(set(final_options_list)) # Ensure uniqueness again after potential addition
            while len(final_options_list) < 5: # Re-pad if set operation reduced count
                padding = f"PadOpt{len(final_options_list)}_{random.randint(100,200)}"
                if padding not in final_options_list: final_options_list.append(padding)
                else: final_options_list.append(f"PadOpt_{random.randint(201,300)}")


            random.shuffle(final_options_list)
            generated_questions.append({
                "question_word": question_word, "correct_answer": correct_answer,
                "options": final_options_list[:5], "form_key": f"q_r{st.session_state.round_number}_{i}_{quiz_dir.replace(' ','_')}"
            })
        st.session_state[test_cache_key] = generated_questions

    st.header(f"✏️ Round {st.session_state.round_number}: Test your knowledge!")
    st.info(f"Translate from {quiz_dir.split(' ')[0]} to {quiz_dir.split(' ')[2]}. You have 2 minutes.")
    time_elapsed_test = time.time() - st.session_state.timer_start_time
    time_remaining_test = max(0, 120 - int(time_elapsed_test))
    st.empty().progress(time_remaining_test / 120)
    st.empty().markdown(f"<p class='timer-text'>Test time remaining: {time_remaining_test}s</p>", unsafe_allow_html=True)

    if time_remaining_test <= 0 and 'submitted_test' not in st.session_state:
        st.warning("Time's up!"); st.session_state.submitted_test = True; st.session_state.stage = "results"; st.rerun()

    with st.form(key=f"test_form_r{st.session_state.round_number}_{quiz_dir}_form"):
        temp_answers = {}
        retrieved_questions = st.session_state.get(test_cache_key, [])
        if not retrieved_questions :
             st.error("Error: Questions not loaded for test. Please try starting a new round."); st.stop()

        for i, q_data in enumerate(retrieved_questions):
            selected_option = st.radio(
                f"**{i+1}. {q_data['question_word']}** is:",
                options=q_data['options'], key=q_data['form_key'], index=None
            )
            temp_answers[q_data['question_word']] = {"selected": selected_option if selected_option else "Not Answered", "correct": q_data['correct_answer']}
        
        if st.form_submit_button("✅ Submit Answers"):
            st.session_state.test_answers = temp_answers
            st.session_state.submitted_test = True
            st.session_state.stage = "results"
            st.rerun()

    if time_remaining_test > 0 and 'submitted_test' not in st.session_state:
        time.sleep(1); st.rerun()

elif st.session_state.stage == "results":
    st.header(f"📊 Round {st.session_state.round_number}: Results!")
    round_score = 0
    if not st.session_state.get('test_answers'): st.warning("No answers processed.")
    else:
        for question_word, data in st.session_state.test_answers.items():
            selected = str(data.get('selected', "Not Answered")); correct = str(data.get('correct', "N/A"))
            if selected == correct:
                st.markdown(f"✅ **{question_word}**: Your answer <span class='orange-text'>{selected}</span> was CORRECT! 🎉", unsafe_allow_html=True)
                round_score += 1; st.session_state.overall_correct_streak +=1
            else:
                st.session_state.overall_correct_streak = 0
                if selected == "Not Answered": st.markdown(f"ℹ️ **{question_word}**: Not answered. Correct: <span class='orange-text'>{correct}</span>", unsafe_allow_html=True)
                else: st.markdown(f"❌ **{question_word}**: Your answer <span class='orange-text'>{selected}</span> INCORRECT. Correct: <span class='orange-text'>{correct}</span> 🙁", unsafe_allow_html=True)
        if st.session_state.current_word_set:
            st.subheader(f"You scored {round_score}/{len(st.session_state.current_word_set)} this round.")
            round_scored_key = f"round_{st.session_state.round_number}_main_score"
            if not st.session_state.get(round_scored_key, False): st.session_state.score += round_score; st.session_state[round_scored_key] = True
    st.metric(label="Total Score", value=st.session_state.score)
    st.metric(label="🔥 Overall Correct Streak", value=st.session_state.overall_correct_streak)
    st.info(f"✨ {random.choice(motivational_quotes)} ✨")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Set of Words ➡️", use_container_width=True, key=f"next_round_btn_{st.session_state.round_number}"):
            st.sidebar.info("DEBUG: 'Next Set' Clicked.")
            quiz_dir_of_completed_round = st.session_state.get("quiz_direction", "Polish to English")
            completed_round_cache_key = f"test_questions_round_{st.session_state.round_number}_{quiz_dir_of_completed_round.replace(' ','_')}"
            if completed_round_cache_key in st.session_state.get('test_questions_cache', {}): # Check if key is in the cache dict
                 del st.session_state['test_questions_cache'][completed_round_cache_key] # If cache is dict of dicts
                 st.sidebar.info(f"DEBUG: Cleared specific cache: {completed_round_cache_key}")
            elif completed_round_cache_key in st.session_state: # If cache keys are top-level in session_state
                 del st.session_state[completed_round_cache_key]
                 st.sidebar.info(f"DEBUG: Cleared top-level cache: {completed_round_cache_key}")
            else:
                 st.sidebar.warning(f"DEBUG: Cache key not found for clearing: {completed_round_cache_key}")


            st.session_state.round_number += 1; st.sidebar.info(f"DEBUG: New round: {st.session_state.round_number}")
            st.session_state.stage = "learning_individual"; st.sidebar.info(f"DEBUG: Stage set to: {st.session_state.stage}")
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words_loaded, 10, st.session_state.seen_words_indices)
            if not st.session_state.current_word_set:
                st.error("No new words for the next round."); st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0; st.session_state.learning_word_start_time = time.time()
            st.session_state.test_answers = {}; 
            if 'submitted_test' in st.session_state: del st.session_state.submitted_test
            st.rerun()
    with col2:
        if st.button("Restart Game 🔄", use_container_width=True, key=f"restart_game_btn_{st.session_state.round_number}"):
            current_quiz_dir = st.session_state.get("quiz_direction", "Polish to English")
            loaded_words = st.session_state.get("all_words_loaded", []) # Preserve loaded words
            
            # Clear all session state keys except for a few essential ones or re-initialize
            keys_to_preserve = ['all_words_loaded', 'quiz_direction']
            for key in list(st.session_state.keys()):
                if key not in keys_to_preserve:
                    del st.session_state[key]
            
            # Re-initialize to default values
            for key, value in default_session_state.items():
                if key not in st.session_state: # Only set if deleted
                    st.session_state[key] = value
            
            # Restore preserved values if they were deleted by the loop above
            st.session_state.quiz_direction = current_quiz_dir 
            st.session_state.all_words_loaded = loaded_words if loaded_words else ALL_WORDS # Ensure it's reloaded if became empty
            
            st.rerun()
else:
    st.error("Unknown application stage. Resetting to Welcome screen.")
    st.session_state.stage = "welcome"
    st.session_state.score = 0
    st.session_state.round_number = 0
    st.session_state.overall_correct_streak = 0
    st.rerun()
