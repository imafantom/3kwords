import streamlit as st
import pandas as pd
import random
import time
import re # For highlighting words in sentences

# st.set_page_config() MUST be the first Streamlit command after imports
st.set_page_config(layout="centered", page_title="Vocabulary Practice")

# --- Helper Functions ---
@st.cache_data # Cache the data loading
def load_words():
    # Using the substantial placeholder from previous interactions.
    # User should continue to populate this list from their PDF.
    word_data_list = [
        {'English Word': 'a', 'Polish Translation': 'a', 'Example Sentence': 'I need a pen.'},
        {'English Word': 'abandon', 'Polish Translation': 'porzucić', 'Example Sentence': 'They had to abandon their car in the snow.'},
        {'English Word': 'ability', 'Polish Translation': 'zdolność', 'Example Sentence': 'She has the ability to learn new languages quickly.'},
        {'English Word': 'able', 'Polish Translation': 'zdolny', 'Example Sentence': 'He is able to lift heavy boxes.'},
        {'English Word': 'abortion', 'Polish Translation': 'aborcja', 'Example Sentence': 'The debate around abortion is highly controversial.'},
        {'English Word': 'about', 'Polish Translation': 'o, około', 'Example Sentence': "What are you talking about? It's about five o'clock."},
        {'English Word': 'above', 'Polish Translation': 'powyżej', 'Example Sentence': 'The bird flew above the trees.'},
        {'English Word': 'abroad', 'Polish Translation': 'za granicą', 'Example Sentence': 'He decided to study abroad for a year.'},
        {'English Word': 'absence', 'Polish Translation': 'nieobecność', 'Example Sentence': 'His absence from the meeting was noted.'},
        {'English Word': 'absolute', 'Polish Translation': 'absolutny', 'Example Sentence': "It's an absolute necessity."},
        {'English Word': 'absolutely', 'Polish Translation': 'absolutnie', 'Example Sentence': 'Are you sure? Absolutely!'},
        {'English Word': 'absorb', 'Polish Translation': 'wchłaniać', 'Example Sentence': 'The sponge can absorb a lot of water.'},
        {'English Word': 'abuse', 'Polish Translation': 'nadużycie', 'Example Sentence': 'Child abuse is a serious crime.'},
        {'English Word': 'academic', 'Polish Translation': 'akademicki', 'Example Sentence': 'She excels in academic subjects.'},
        {'English Word': 'accept', 'Polish Translation': 'zaakceptować', 'Example Sentence': 'I accept your offer.'},
        {'English Word': 'access', 'Polish Translation': 'dostęp', 'Example Sentence': 'Do you have access to the internet here?'},
        {'English Word': 'accident', 'Polish Translation': 'wypadek', 'Example Sentence': 'He was involved in a car accident.'},
        {'English Word': 'accompany', 'Polish Translation': 'towarzyszyć', 'Example Sentence': 'I will accompany you to the station.'},
        {'English Word': 'accomplish', 'Polish Translation': 'osiągnąć', 'Example Sentence': 'We need to accomplish this task by Friday.'},
        {'English Word': 'according', 'Polish Translation': 'według', 'Example Sentence': "According to the map, we're almost there."},
        {'English Word': 'account', 'Polish Translation': 'konto', 'Example Sentence': 'Please deposit the money into my bank account.'},
        {'English Word': 'accurate', 'Polish Translation': 'dokładny', 'Example Sentence': 'We need accurate data for this report.'},
        # ... (Continue adding ALL words from your PDF here)
        # For brevity, I am keeping the example list short for this code block.
        # Ensure you have at least 5-10 unique words for the distractor logic to work without issues.
        {'English Word': 'dad', 'Polish Translation': 'tata', 'Example Sentence': 'My dad is picking me up from school.'},
        {'English Word': 'daily', 'Polish Translation': 'codzienny', 'Example Sentence': 'I read the daily newspaper.'},
        {'English Word': 'damage', 'Polish Translation': 'uszkodzenie, uszkodzić', 'Example Sentence': "The storm caused a lot of damage. / Don't damage the equipment."},
        {'English Word': 'dance', 'Polish Translation': 'taniec, tańczyć', 'Example Sentence': 'She loves to dance.'},
        {'English Word': 'danger', 'Polish Translation': 'niebezpieczeństwo', 'Example Sentence': 'There is danger in climbing without a rope.'},
        {'English Word': 'each', 'Polish Translation': 'każdy', 'Example Sentence': 'Each student received a book.'},
        {'English Word': 'eager', 'Polish Translation': 'chętny, żądny', 'Example Sentence': 'He was eager to learn new things.'},
        {'English Word': 'ear', 'Polish Translation': 'ucho', 'Example Sentence': 'My ear hurts.'},
        {'English Word': 'early', 'Polish Translation': 'wcześnie', 'Example Sentence': 'She wakes up early every day.'},
        {'English Word': 'earn', 'Polish Translation': 'zarabiać', 'Example Sentence': 'How much do you earn per month?'},
    ]
    if len(word_data_list) < 5: # Need at least 5 for distractors + correct answer.
        st.warning("Word list is very small. Multiple choice questions might have repeated options or fewer than 5 options.")
    return word_data_list

ALL_WORDS = load_words()

def get_new_word_set(words_list, num_words=10, seen_indices=None):
    if seen_indices is None: seen_indices = set()
    available_indices = [i for i, _ in enumerate(words_list) if i not in seen_indices]
    if len(available_indices) < num_words:
        st.warning("Not enough new unique words for this round. Words may repeat or be fewer than requested.")
        if not available_indices and words_list: # If all words seen, allow repeating
            seen_indices.clear()
            available_indices = list(range(len(words_list)))
        elif not words_list: return []
    if not available_indices: return []
    chosen_indices = random.sample(available_indices, min(num_words, len(available_indices)))
    new_set = [words_list[i] for i in chosen_indices]
    for i in chosen_indices: seen_indices.add(i)
    return new_set

def highlight_word_in_sentence(sentence, word_to_highlight):
    try:
        escaped_word = re.escape(word_to_highlight)
        return re.sub(f"\\b({escaped_word})\\b", r"<span class='orange-text'>\1</span>", sentence, flags=re.IGNORECASE)
    except: return sentence

motivational_quotes = [
    "Great job! Keep learning!", "Excellent! Every step counts.", "You're doing great!",
    "Awesome! Practice makes perfect.", "Fantastic! Keep it up!"
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
        .example-sentence { font-size: 1.1em !important; font-style: italic; color: #555; }
        /* Ensure radio buttons are styled well */
        .stRadio > label > div:first-child { /* Target the radio button circle/box */
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🇬🇧 English Vocabulary Practice 🇵🇱")

# Initialize session state variables
default_session_state = {
    "stage": "welcome", "all_words": ALL_WORDS, "score": 0, "current_word_set": [],
    "test_answers": {}, "timer_start_time": 0, "round_number": 0, "seen_words_indices": set(),
    "current_learning_word_index": 0, "learning_word_start_time": 0,
    "quiz_direction": "Polish to English", "overall_correct_streak": 0
}
for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.stage == "welcome":
    st.header("Welcome to the Vocabulary Trainer!")
    st.session_state.quiz_direction = st.radio(
        "Select Quiz Direction:",
        ("Polish to English", "English to Polish"),
        index=("Polish to English", "English to Polish").index(st.session_state.quiz_direction),
        key="quiz_direction_selector"
    )
    if st.button("🚀 Start Learning"):
        if not ALL_WORDS:
            st.error("Word list is empty. Please populate the `load_words()` function.")
        else:
            st.session_state.round_number += 1
            st.session_state.stage = "learning_individual"
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words, 10, st.session_state.seen_words_indices)
            if not st.session_state.current_word_set:
                st.error("Could not load words. Ensure the list is populated and has enough variety.")
                st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0
                st.session_state.learning_word_start_time = time.time()
            st.rerun()

elif st.session_state.stage == "learning_individual":
    if not st.session_state.current_word_set:
        st.error("Word set is empty."); st.session_state.stage = "welcome"; st.rerun()
    elif st.session_state.current_learning_word_index >= len(st.session_state.current_word_set):
        st.session_state.stage = "test"; st.session_state.timer_start_time = time.time(); st.session_state.test_answers = {}; st.rerun()
    else:
        word_data = st.session_state.current_word_set[st.session_state.current_learning_word_index]
        st.header(f"🧠 Round {st.session_state.round_number}: Learn Word {st.session_state.current_learning_word_index + 1}/{len(st.session_state.current_word_set)}")
        time_elapsed_word = time.time() - st.session_state.learning_word_start_time
        time_remaining_word = max(0, 5 - int(time_elapsed_word))
        st.empty().markdown(f"<p class='timer-text'>Time for this word: {time_remaining_word}s</p>", unsafe_allow_html=True)
        st.markdown(f"## <span class='orange-text'>{word_data['English Word']}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🇵🇱 {word_data['Polish Translation']}")
        highlighted_sentence = highlight_word_in_sentence(word_data['Example Sentence'], word_data['English Word'])
        st.markdown(f"<p class='example-sentence'>📖 Example: {highlighted_sentence}</p>", unsafe_allow_html=True)
        st.markdown("---")
        if time_remaining_word <= 0:
            st.session_state.current_learning_word_index += 1
            if st.session_state.current_learning_word_index < len(st.session_state.current_word_set):
                st.session_state.learning_word_start_time = time.time()
            st.rerun()
        else:
            time.sleep(1); st.rerun()

elif st.session_state.stage == "test":
    st.header(f"✏️ Round {st.session_state.round_number}: Test your knowledge!")
    st.info(f"Translate from {st.session_state.quiz_direction.split(' ')[0]} to {st.session_state.quiz_direction.split(' ')[2]}. You have 2 minutes.")
    time_elapsed_test = time.time() - st.session_state.timer_start_time
    time_remaining_test = max(0, 120 - int(time_elapsed_test))
    st.empty().progress(time_remaining_test / 120)
    st.empty().markdown(f"<p class='timer-text'>Test time remaining: {time_remaining_test}s</p>", unsafe_allow_html=True)

    if time_remaining_test <= 0 and 'submitted_test' not in st.session_state:
        st.warning("Time's up!"); st.session_state.submitted_test = True; st.session_state.stage = "results"; st.rerun()
    if not st.session_state.current_word_set:
        st.error("No words for test."); st.session_state.stage = "welcome"; st.rerun()

    question_lang_key = 'Polish Translation' if st.session_state.quiz_direction == "Polish to English" else 'English Word'
    answer_lang_key = 'English Word' if st.session_state.quiz_direction == "Polish to English" else 'Polish Translation'

    with st.form(key=f"test_form_r{st.session_state.round_number}"):
        temp_answers = {}
        for i, word_data in enumerate(st.session_state.current_word_set):
            question_word = word_data[question_lang_key]
            correct_answer = word_data[answer_lang_key]
            
            options = {correct_answer} # Use a set to ensure uniqueness initially
            
            # Generate distractors
            distractor_pool = [w[answer_lang_key] for w in ALL_WORDS if w[answer_lang_key] != correct_answer and w[question_lang_key] != question_word]
            
            # Ensure enough unique distractors (need 4)
            while len(options) < 5 and distractor_pool:
                distractor = random.choice(distractor_pool)
                options.add(distractor)
                distractor_pool.remove(distractor) # Avoid reusing the same distractor for this question
            
            # If still not enough options (e.g. ALL_WORDS is too small), pad with placeholders or fewer options
            final_options_list = list(options)
            while len(final_options_list) < 5 and len(final_options_list) < len(ALL_WORDS): # Add more generic distractors if needed
                 # Try to pick any other word from ALL_WORDS not already in options
                 potential_padding = [w[answer_lang_key] for w in ALL_WORDS if w[answer_lang_key] not in final_options_list]
                 if potential_padding:
                     final_options_list.append(random.choice(potential_padding))
                 else: # Absolute fallback
                     final_options_list.append(f"Option {len(final_options_list)+1}")


            random.shuffle(final_options_list)
            
            # Ensure correct answer is always in the options if it got shuffled out by unique constraint logic with small ALL_WORDS
            if correct_answer not in final_options_list:
                if len(final_options_list) >= 5: final_options_list[random.randint(0,4)] = correct_answer
                else: final_options_list.append(correct_answer)
                random.shuffle(final_options_list)


            selected_option = st.radio(
                f"**{i+1}. {question_word}** is:",
                options=final_options_list[:5], # Ensure only 5 options
                key=f"q_r{st.session_state.round_number}_{i}",
                index=None # No default selection
            )
            temp_answers[question_word] = {"selected": selected_option if selected_option else "Not Answered", "correct": correct_answer}
        
        if st.form_submit_button("✅ Submit Answers"):
            st.session_state.test_answers = temp_answers
            st.session_state.submitted_test = True
            st.session_state.stage = "results"
            st.rerun()

    if time_remaining_test > 0 and 'submitted_test' not in st.session_state:
        time.sleep(1); st.rerun()
    elif 'submitted_test' in st.session_state and st.session_state.stage != "results":
        del st.session_state.submitted_test

elif st.session_state.stage == "results":
    st.header(f"📊 Round {st.session_state.round_number}: Results!")
    round_score = 0
    current_round_all_correct = True

    if not st.session_state.get('test_answers'):
        st.warning("No answers processed.")
    else:
        for question_word_key, data in st.session_state.test_answers.items(): # question_word_key is actually the question word string
            selected = str(data.get('selected', "Not Answered"))
            correct = str(data.get('correct', "N/A"))
            
            if selected == correct:
                st.markdown(f"✅ **{question_word_key}**: Your answer <span class='orange-text'>{selected}</span> was CORRECT! 🎉", unsafe_allow_html=True)
                round_score += 1
                st.session_state.overall_correct_streak +=1
            else:
                current_round_all_correct = False
                st.session_state.overall_correct_streak = 0 # Reset streak on any incorrect answer
                if selected == "Not Answered":
                    st.markdown(f"ℹ️ **{question_word_key}**: Not answered. Correct was: <span class='orange-text'>{correct}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"❌ **{question_word_key}**: Your answer <span class='orange-text'>{selected}</span> INCORRECT. Correct: <span class='orange-text'>{correct}</span> 🙁", unsafe_allow_html=True)
        
        if st.session_state.current_word_set:
            st.subheader(f"You scored {round_score}/{len(st.session_state.current_word_set)} this round.")
            round_scored_key = f"round_{st.session_state.round_number}_main_score" # More specific key
            if not st.session_state.get(round_scored_key, False):
                 st.session_state.score += round_score
                 st.session_state[round_scored_key] = True
    
    st.metric(label="Total Score", value=st.session_state.score)
    st.metric(label="🔥 Overall Correct Streak", value=st.session_state.overall_correct_streak)
    st.info(f"✨ {random.choice(motivational_quotes)} ✨")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Set of Words ➡️", use_container_width=True):
            st.session_state.round_number += 1; st.session_state.stage = "learning_individual"
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words, 10, st.session_state.seen_words_indices)
            if not st.session_state.current_word_set:
                st.error("No new words."); st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0; st.session_state.learning_word_start_time = time.time()
            st.session_state.test_answers = {}; 
            if 'submitted_test' in st.session_state: del st.session_state.submitted_test
            st.rerun()
    with col2:
        if st.button("Restart Game 🔄", use_container_width=True):
            keys_to_del = [k for k in st.session_state.keys() if k != 'all_words' and k != 'quiz_direction'] # Keep quiz_direction
            for key in keys_to_del: del st.session_state[key]
            # Re-initialize
            for key, value in default_session_state.items():
                if key != 'all_words' and key != 'quiz_direction': # quiz_direction is kept from user selection
                     st.session_state[key] = value
            st.session_state.all_words = ALL_WORDS # Ensure all_words is reset if it was changed
            st.rerun()
else:
    st.error("Unknown stage. Resetting."); st.session_state.stage = "welcome"; st.rerun()
