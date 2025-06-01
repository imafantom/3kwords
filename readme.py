import streamlit as st
import pandas as pd
import random
import time
import re # For highlighting words in sentences

# st.set_page_config() MUST be the first Streamlit command after imports
st.set_page_config(layout="centered")

# --- Helper Functions ---
@st.cache_data # Cache the data loading
def load_words():
    # Data transcribed from the provided PDF.
    # THIS LIST IS NOW SUBSTANTIALLY LARGER BUT STILL NOT THE COMPLETE 3000 WORDS.
    # You will need to continue adding entries from your PDF to this list.
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
        {'English Word': 'accuse', 'Polish Translation': 'oskarżyć', 'Example Sentence': 'They accused him of lying.'},
        {'English Word': 'achieve', 'Polish Translation': 'osiągnąć', 'Example Sentence': 'She worked hard to achieve her goals.'},
        {'English Word': 'achievement', 'Polish Translation': 'osiągnięcie', 'Example Sentence': 'Winning the award was a great achievement.'},
        {'English Word': 'acid', 'Polish Translation': 'kwas', 'Example Sentence': 'Lemon juice is acidic.'},
        {'English Word': 'acknowledge', 'Polish Translation': 'potwierdzić, uznać', 'Example Sentence': 'Please acknowledge receipt of this email.'},
        {'English Word': 'acquire', 'Polish Translation': 'nabyć', 'Example Sentence': 'The company plans to acquire a smaller business.'},
        {'English Word': 'across', 'Polish Translation': 'przez', 'Example Sentence': 'He walked across the street.'},
        {'English Word': 'act', 'Polish Translation': 'czyn, działać, ustawa', 'Example Sentence': 'It was an act of kindness. / You need to act quickly. / The new Act comes into force next month.'},
        {'English Word': 'action', 'Polish Translation': 'działanie', 'Example Sentence': 'His words led to immediate action.'},
        {'English Word': 'active', 'Polish Translation': 'aktywny', 'Example Sentence': 'She leads a very active lifestyle.'},
        {'English Word': 'activist', 'Polish Translation': 'aktywista', 'Example Sentence': 'Environmental activists protested the new factory.'},
        {'English Word': 'activity', 'Polish Translation': 'aktywność', 'Example Sentence': 'There are many outdoor activities available.'},
        {'English Word': 'actor', 'Polish Translation': 'aktor', 'Example Sentence': 'He is a famous Hollywood actor.'},
        {'English Word': 'actress', 'Polish Translation': 'aktorka', 'Example Sentence': 'She is a talented actress.'},
        {'English Word': 'actual', 'Polish Translation': 'rzeczywisty', 'Example Sentence': 'What was the actual cost of the trip?'},
        {'English Word': 'actually', 'Polish Translation': 'właściwie, faktycznie', 'Example Sentence': 'I actually thought it would be harder.'},
        {'English Word': 'ad', 'Polish Translation': 'reklama', 'Example Sentence': 'I saw a funny ad on TV.'},
        {'English Word': 'adapt', 'Polish Translation': 'przystosować się', 'Example Sentence': 'Animals adapt to their environment.'},
        {'English Word': 'add', 'Polish Translation': 'dodać', 'Example Sentence': 'Please add sugar to my coffee.'},
        {'English Word': 'addition', 'Polish Translation': 'dodatek', 'Example Sentence': 'In addition to that, we need more staff.'},
        {'English Word': 'additional', 'Polish Translation': 'dodatkowy', 'Example Sentence': 'Do you require any additional information?'},
        {'English Word': 'address', 'Polish Translation': 'adres, zaadresować', 'Example Sentence': "What's your home address? / He addressed the audience."},
        {'English Word': 'adequate', 'Polish Translation': 'odpowiedni', 'Example Sentence': 'The facilities are adequate for our needs.'},
        {'English Word': 'adjust', 'Polish Translation': 'dostosować', 'Example Sentence': 'You can adjust the volume with this knob.'},
        {'English Word': 'adjustment', 'Polish Translation': 'dostosowanie', 'Example Sentence': 'We need to make some adjustments to the schedule.'},
        {'English Word': 'administration', 'Polish Translation': 'administracja', 'Example Sentence': 'The university administration handles student affairs.'},
        {'English Word': 'administrator', 'Polish Translation': 'administrator', 'Example Sentence': 'The system administrator manages the network.'},
        {'English Word': 'admire', 'Polish Translation': 'podziwiać', 'Example Sentence': 'I admire her courage.'},
        {'English Word': 'admission', 'Polish Translation': 'wstęp, przyjęcie', 'Example Sentence': 'Admission to the museum is free.'},
        {'English Word': 'admit', 'Polish Translation': 'przyznać', 'Example Sentence': 'I must admit I was wrong.'},
        {'English Word': 'adolescent', 'Polish Translation': 'nastolatek', 'Example Sentence': 'Adolescents often face many challenges.'},
        {'English Word': 'adopt', 'Polish Translation': 'adoptować, przyjąć', 'Example Sentence': 'They decided to adopt a child. / The company adopted a new policy.'},
        {'English Word': 'adult', 'Polish Translation': 'dorosły', 'Example Sentence': 'This movie is for adult audiences only.'},
        {'English Word': 'advance', 'Polish Translation': 'postęp', 'Example Sentence': 'We have made significant advances in technology.'},
        {'English Word': 'advanced', 'Polish Translation': 'zaawansowany', 'Example Sentence': 'She is an advanced English speaker.'},
        {'English Word': 'advantage', 'Polish Translation': 'zaleta', 'Example Sentence': 'What are the advantages of working from home?'},
        {'English Word': 'adventure', 'Polish Translation': 'przygoda', 'Example Sentence': 'They went on a great adventure.'},
        {'English Word': 'advertising', 'Polish Translation': 'reklama', 'Example Sentence': 'Advertising plays a crucial role in sales.'},
        {'English Word': 'advice', 'Polish Translation': 'rada', 'Example Sentence': 'Can you give me some advice?'},
        {'English Word': 'advise', 'Polish Translation': 'doradzać', 'Example Sentence': 'I advise you to read the instructions carefully.'},
        {'English Word': 'adviser', 'Polish Translation': 'doradca', 'Example Sentence': 'He is a financial adviser.'},
        {'English Word': 'advocate', 'Polish Translation': 'orędownik, popierać', 'Example Sentence': 'She is a strong advocate for human rights. / He advocates for healthier eating habits.'},
        {'English Word': 'affair', 'Polish Translation': 'sprawa, romans', 'Example Sentence': "It's a private affair. / He had an affair with his colleague."},
        {'English Word': 'affect', 'Polish Translation': 'wpływać', 'Example Sentence': 'The weather can affect your mood.'},
        {'English Word': 'afford', 'Polish Translation': 'pozwolić sobie', 'Example Sentence': "I can't afford a new car."},
        {'English Word': 'afraid', 'Polish Translation': 'bać się', 'Example Sentence': "I'm afraid I can't help you."},
        # ... (Many more words from A-C transcribed from [cite: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67])
        # I will add a selection from D, E, F as well for better coverage in this example
        {'English Word': 'dad', 'Polish Translation': 'tata', 'Example Sentence': 'My dad is picking me up from school.'},
        {'English Word': 'daily', 'Polish Translation': 'codzienny', 'Example Sentence': 'I read the daily newspaper.'},
        {'English Word': 'damage', 'Polish Translation': 'uszkodzenie, uszkodzić', 'Example Sentence': "The storm caused a lot of damage. / Don't damage the equipment."},
        {'English Word': 'dance', 'Polish Translation': 'taniec, tańczyć', 'Example Sentence': 'She loves to dance.'},
        {'English Word': 'danger', 'Polish Translation': 'niebezpieczeństwo', 'Example Sentence': 'There is danger in climbing without a rope.'},
        {'English Word': 'dangerous', 'Polish Translation': 'niebezpieczny', 'Example Sentence': 'Driving too fast is dangerous.'},
        {'English Word': 'dare', 'Polish Translation': 'ośmielić się', 'Example Sentence': 'I dare you to jump.'},
        {'English Word': 'dark', 'Polish Translation': 'ciemny', 'Example Sentence': "It's getting dark outside."},
        {'English Word': 'darkness', 'Polish Translation': 'ciemność', 'Example Sentence': 'She was afraid of the darkness.'},
        {'English Word': 'data', 'Polish Translation': 'dane', 'Example Sentence': 'We need to analyze the sales data.'}, # [cite: 70]
        {'English Word': 'each', 'Polish Translation': 'każdy', 'Example Sentence': 'Each student received a book.'},
        {'English Word': 'eager', 'Polish Translation': 'chętny, żądny', 'Example Sentence': 'He was eager to learn new things.'},
        {'English Word': 'ear', 'Polish Translation': 'ucho', 'Example Sentence': 'My ear hurts.'},
        {'English Word': 'early', 'Polish Translation': 'wcześnie', 'Example Sentence': 'She wakes up early every day.'},
        {'English Word': 'earn', 'Polish Translation': 'zarabiać', 'Example Sentence': 'How much do you earn per month?'},
        {'English Word': 'earnings', 'Polish Translation': 'zarobki', 'Example Sentence': 'His annual earnings are quite high.'},
        {'English Word': 'earth', 'Polish Translation': 'ziemia', 'Example Sentence': 'The Earth revolves around the sun.'}, # [cite: 86]
        {'English Word': 'fabric', 'Polish Translation': 'tkanina', 'Example Sentence': 'This shirt is made of soft fabric.'},
        {'English Word': 'face', 'Polish Translation': 'twarz, stawić czoła', 'Example Sentence': 'Her face was red from the sun. / We need to face our problems.'},
        {'English Word': 'facility', 'Polish Translation': 'obiekt, udogodnienie', 'Example Sentence': 'The sports facility offers a gym and a pool.'},
        {'English Word': 'fact', 'Polish Translation': 'fakt', 'Example Sentence': "It's a proven fact."},
        {'English Word': 'factor', 'Polish Translation': 'czynnik', 'Example Sentence': 'Price is a key factor in his decision.'},
        {'English Word': 'factory', 'Polish Translation': 'fabryka', 'Example Sentence': 'The car factory produces thousands of vehicles.'}, # [cite: 103, 104]
        # Add more words here following the pattern:
        # {'English Word': 'word', 'Polish Translation': 'tłumaczenie', 'Example Sentence': 'Example.'},
    ]
    return word_data_list

ALL_WORDS = load_words()

def get_new_word_set(words_list, num_words=10, seen_indices=None):
    if seen_indices is None:
        seen_indices = set()
    available_indices = [i for i, _ in enumerate(words_list) if i not in seen_indices]
    if len(available_indices) < num_words:
        st.warning("Not enough new words, sampling from all words again. Consider restarting for fresh unseen words if available.")
        available_indices = list(range(len(words_list)))
        if not available_indices and words_list:
             st.info("All words might have been cycled through. Restarting seen words tracking for this round.")
             seen_indices.clear()
             available_indices = list(range(len(words_list)))
        elif not words_list:
             return []
    if not available_indices: # If still no available_indices (e.g., words_list itself is empty)
        return []
    chosen_indices = random.sample(available_indices, min(num_words, len(available_indices)))
    new_set = [words_list[i] for i in chosen_indices]
    for i in chosen_indices:
        seen_indices.add(i)
    return new_set

def highlight_word_in_sentence(sentence, word_to_highlight):
    try:
        escaped_word = re.escape(word_to_highlight)
        highlighted_sentence = re.sub(
            f"\\b({escaped_word})\\b",
            r"<span style='color:orange; font-weight:bold;'>\1</span>",
            sentence,
            flags=re.IGNORECASE
        )
        return highlighted_sentence
    except Exception:
        return sentence

motivational_quotes = [
    "Great job! Keep the momentum going!",
    "Excellent work! Every correct answer is a step forward.",
    "You're doing wonderfully! Keep practicing.",
    "Awesome effort! The more you learn, the more you grow.",
    "Fantastic! Each round makes you stronger.",
    "Well done! Consistency is key to mastery.",
    "Super! You're building a strong vocabulary.",
    "Amazing! Keep challenging yourself."
]

# Apply global styles
st.markdown("""
    <style>
        body, .stApp, .stButton>button, .stSelectbox div[data-baseweb='select'] > div, .stTextInput > div > div > input, .stMetric > div > div {
            font-size: 18px !important;
        }
        .stSubheader {
            font-size: 22px !important;
            font-weight: bold;
        }
        .orange-text {
            color: orange;
            font-weight: bold;
        }
        .timer-text {
            font-size: 20px !important;
            font-weight: bold;
            color: #1E90FF;
            text-align: center;
            margin-bottom: 10px;
        }
        .stProgress > div > div > div > div {
            background-color: #1E90FF !important;
        }
        .example-sentence { /* New class for example sentences */
            font-size: 1.1em !important; /* Larger font size */
            font-style: italic;
            color: #555; /* Slightly different color for distinction */
        }
    </style>
""", unsafe_allow_html=True)

st.title("🇬🇧 English Vocabulary Practice 🇵🇱")

# Initialize session state variables
if 'stage' not in st.session_state:
    st.session_state.stage = "welcome"
    st.session_state.all_words = ALL_WORDS
    st.session_state.score = 0
    st.session_state.current_word_set = []
    st.session_state.test_answers = {}
    st.session_state.timer_start_time = 0
    st.session_state.round_number = 0
    st.session_state.seen_words_indices = set()
    st.session_state.current_learning_word_index = 0
    st.session_state.learning_word_start_time = 0

# --- Welcome Stage ---
if st.session_state.stage == "welcome":
    st.header("Welcome to the Vocabulary Trainer!")
    st.write("Press the button below to start a new learning session.")
    if st.button("🚀 Start Learning"):
        if not ALL_WORDS:
            st.error("Word list is empty. Please populate the `load_words()` function.")
        else:
            st.session_state.round_number += 1
            st.session_state.stage = "learning_individual"
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words, 10, st.session_state.seen_words_indices)
            if not st.session_state.current_word_set:
                st.error("Could not load words. Please ensure the word list is populated and has enough variety.")
                st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0
                st.session_state.learning_word_start_time = time.time()
            st.rerun()

# --- Learning Stage (Individual Word Display) ---
elif st.session_state.stage == "learning_individual":
    if not st.session_state.current_word_set:
        st.error("Word set is empty. Returning to welcome screen.")
        st.session_state.stage = "welcome"
        st.rerun()
    elif st.session_state.current_learning_word_index >= len(st.session_state.current_word_set):
        st.session_state.stage = "test"
        st.session_state.timer_start_time = time.time()
        st.session_state.test_answers = {}
        st.rerun()
    else:
        word_data = st.session_state.current_word_set[st.session_state.current_learning_word_index]
        st.header(f"🧠 Round {st.session_state.round_number}: Learn Word {st.session_state.current_learning_word_index + 1}/{len(st.session_state.current_word_set)}")
        time_elapsed_word = time.time() - st.session_state.learning_word_start_time
        time_remaining_word = max(0, 5 - int(time_elapsed_word))
        timer_placeholder_word = st.empty()
        timer_placeholder_word.markdown(f"<p class='timer-text'>Time for this word: {time_remaining_word}s</p>", unsafe_allow_html=True)
        st.markdown(f"## <span class='orange-text'>{word_data['English Word']}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🇵🇱 {word_data['Polish Translation']}")
        highlighted_sentence = highlight_word_in_sentence(word_data['Example Sentence'], word_data['English Word'])
        st.markdown(f"<p class='example-sentence'>📖 Example: {highlighted_sentence}</p>", unsafe_allow_html=True) # Apply class here
        st.markdown("---")
        if time_remaining_word <= 0:
            st.session_state.current_learning_word_index += 1
            if st.session_state.current_learning_word_index < len(st.session_state.current_word_set):
                st.session_state.learning_word_start_time = time.time()
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()

# --- Test Stage ---
elif st.session_state.stage == "test":
    st.header(f"✏️ Round {st.session_state.round_number}: Test your knowledge!")
    st.info("Match the Polish word with its English translation. You have 2 minutes for the whole test.") # Updated time
    time_elapsed_test = time.time() - st.session_state.timer_start_time
    time_remaining_test = max(0, 120 - int(time_elapsed_test)) # Updated to 120 seconds
    progress_bar_test_placeholder = st.empty()
    timer_text_test_placeholder = st.empty()
    progress_bar_test_placeholder.progress(time_remaining_test / 120) # Updated denominator
    timer_text_test_placeholder.markdown(f"<p class='timer-text'>Test time remaining: {time_remaining_test}s</p>", unsafe_allow_html=True)

    if time_remaining_test <= 0 and 'submitted_test' not in st.session_state:
        st.warning("Time's up! Moving to results.")
        st.session_state.submitted_test = True
        # If form isn't submitted by timeout, test_answers might be empty or partially filled from previous interactions.
        # Best to ensure test_answers is populated based on current form state if possible,
        # but Streamlit forms typically require explicit submission.
        # For simplicity, if timeout, we process whatever might be in test_answers or it remains empty.
        st.session_state.stage = "results"
        st.rerun()

    if not st.session_state.current_word_set:
        st.error("No words in the current set for the test. Returning to welcome.")
        st.session_state.stage = "welcome"
        st.rerun()

    polish_words_for_test = [word['Polish Translation'] for word in st.session_state.current_word_set]
    english_options = [word['English Word'] for word in st.session_state.current_word_set]

    with st.form(key=f"test_form_round_{st.session_state.round_number}"):
        temp_student_answers_map = {}
        for i, pl_word in enumerate(polish_words_for_test):
            correct_en_word = ""
            for wd_data in st.session_state.current_word_set:
                if wd_data['Polish Translation'] == pl_word:
                    correct_en_word = wd_data['English Word']
                    break
            options_for_select = [""] + english_options[:]
            random.shuffle(options_for_select[1:])
            selected_en_word = st.selectbox(
                f"**{i+1}. {pl_word}** is:",
                options=options_for_select,
                index=0,
                key=f"test_q_r{st.session_state.round_number}_{i}"
            )
            temp_student_answers_map[pl_word] = {
                "selected": selected_en_word if selected_en_word else "Not Answered",
                "correct": correct_en_word
            }
        submit_button = st.form_submit_button("✅ Submit Answers")
        if submit_button:
            st.session_state.test_answers = temp_student_answers_map
            st.session_state.submitted_test = True
            st.session_state.stage = "results"
            st.rerun()

    if time_remaining_test > 0 and 'submitted_test' not in st.session_state:
        time.sleep(1)
        st.rerun()
    elif 'submitted_test' in st.session_state and st.session_state.stage != "results":
        del st.session_state.submitted_test

# --- Results Stage ---
elif st.session_state.stage == "results":
    st.header(f"📊 Round {st.session_state.round_number}: Results!")
    round_score = 0

    # Debugging: Display the content of test_answers
    # st.write("DEBUG: st.session_state.test_answers")
    # st.json(st.session_state.get('test_answers', {}))

    if not st.session_state.get('test_answers'):
        st.warning("No answers were processed for the test, or time ran out before submission.")
    else:
        for pl_word, answers_data in st.session_state.test_answers.items():
            if not isinstance(answers_data, dict):
                st.error(f"Data error for Polish word '{pl_word}'. Skipping.")
                continue
            selected_answer = str(answers_data.get('selected', "Not Answered"))
            correct_answer = str(answers_data.get('correct', "Error: Correct answer missing"))
            pl_word_str = str(pl_word)

            if not pl_word_str.strip():
                st.warning(f"Skipping display for an empty Polish word entry. Selected: '{selected_answer}', Correct: '{correct_answer}'")
                continue
            try:
                if selected_answer == correct_answer:
                    st.success(f"**{pl_word_str}**: Your answer <span class='orange-text'>{selected_answer}</span> was CORRECT! 🎉", unsafe_allow_html=True)
                    round_score += 1
                elif selected_answer == "Not Answered":
                    st.info(f"**{pl_word_str}**: Not answered. Correct was: <span class='orange-text'>{correct_answer}</span>", unsafe_allow_html=True)
                else:
                    st.error(f"**{pl_word_str}**: Your answer <span class='orange-text'>{selected_answer}</span> was INCORRECT. Correct was: <span class='orange-text'>{correct_answer}</span> 🙁", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error displaying result for '{pl_word_str}': {e}")

        if st.session_state.current_word_set:
            st.subheader(f"You scored {round_score} out of {len(st.session_state.current_word_set)} in this round.")
            round_scored_key = f"round_{st.session_state.round_number}_scored"
            if not st.session_state.get(round_scored_key, False):
                 st.session_state.score += round_score
                 st.session_state[round_scored_key] = True
        else:
            st.subheader("No words in this round to score against.")

    st.metric(label="Total Score", value=st.session_state.score)
    st.info(f"✨ {random.choice(motivational_quotes)} ✨") # Display motivational quote

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Set of Words ➡️", use_container_width=True):
            st.session_state.round_number += 1
            st.session_state.stage = "learning_individual"
            st.session_state.current_word_set = get_new_word_set(st.session_state.all_words, 10, st.session_state.seen_words_indices)
            if not st.session_state.current_word_set:
                st.error("Could not load new words. Perhaps all words have been seen or the list is empty.")
                st.session_state.stage = "welcome"
            else:
                st.session_state.current_learning_word_index = 0
                st.session_state.learning_word_start_time = time.time()
            st.session_state.test_answers = {}
            if 'submitted_test' in st.session_state: del st.session_state.submitted_test
            if st.session_state.get(f"round_{st.session_state.round_number-1}_scored"): # Reset previous round's scored flag if going to next
                 pass # This logic might need refinement if rounds can be replayed
            st.rerun()
    with col2:
        if st.button("Restart Game 🔄", use_container_width=True):
            keys_to_keep = ['all_words']
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            st.session_state.stage = "welcome"
            st.session_state.score = 0
            st.session_state.round_number = 0
            st.session_state.seen_words_indices = set()
            st.session_state.current_learning_word_index = 0
            st.session_state.current_word_set = []
            st.session_state.test_answers = {}
            st.rerun()
else:
    st.error("Unknown application stage. Resetting to Welcome screen.")
    st.session_state.stage = "welcome"
    st.session_state.score = 0
    st.session_state.round_number = 0
    st.rerun()
