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
    # THIS IS A PLACEHOLDER - REPLACE WITH YOUR ACTUAL DATA LOADING
    # For example, load from a CSV file you created from your document.
    # Ensure you have 'English Word', 'Polish Translation', and 'Example Sentence' columns.
    # The sample data below is minimal and needs to be expanded for the app to work well.
    data = {
        'English Word': ['a', 'abandon', 'ability', 'able', 'abortion', 'about', 'above', 'abroad', 'absence', 'absolute',
                         'accept', 'access', 'accident', 'accompany', 'achieve', 'act', 'action', 'active', 'actor', 'add',
                         'address', 'administration', 'adult', 'advance', 'advantage', 'advice', 'affect', 'afford', 'afraid', 'after',
                         'again', 'age', 'agency', 'agree', 'air', 'all', 'allow', 'almost', 'alone', 'along',
                         'already', 'also', 'always', 'amazing', 'American', 'among', 'amount', 'analysis', 'animal', 'another',
                         'answer', 'any', 'anyone', 'anything', 'appear', 'apple', 'apply', 'approach', 'area', 'argue',
                         'arm', 'army', 'around', 'arrive', 'art', 'article', 'artist', 'as', 'ask', 'assume',
                         'at', 'attack', 'attention', 'attorney', 'audience', 'author', 'authority', 'available', 'average', 'avoid',
                         'award', 'away', 'baby', 'back', 'bad', 'bag', 'balance', 'ball', 'ban', 'band',
                         'bank', 'bar', 'base', 'basic', 'battle', 'be', 'beat', 'beautiful', 'because', 'become',
                         'bed', 'before', 'begin', 'behavior', 'behind', 'believe', 'benefit', 'best', 'better', 'between',
                         'big', 'bill', 'bird', 'black', 'blood', 'blue', 'board', 'body', 'book', 'born', 'both', 'bother', 'bottle', 'box', 'boy',
                         'brain', 'break', 'bring', 'brother', 'build', 'burn', 'bus', 'business', 'but', 'buy', 'by'
                        ],
        'Polish Translation': ['a', 'porzucić', 'zdolność', 'zdolny', 'aborcja', 'o, około', 'powyżej', 'za granicą', 'nieobecność', 'absolutny',
                               'akceptować', 'dostęp', 'wypadek', 'towarzyszyć', 'osiągnąć', 'czyn', 'działanie', 'aktywny', 'aktor', 'dodać',
                               'adres', 'administracja', 'dorosły', 'postęp', 'zaleta', 'rada', 'wpływać', 'pozwolić sobie', 'bać się', 'po',
                               'ponownie', 'wiek', 'agencja', 'zgadzać się', 'powietrze', 'wszyscy', 'pozwolić', 'prawie', 'sam', 'wzdłuż',
                               'już', 'także', 'zawsze', 'niesamowity', 'amerykański', 'wśród', 'ilość', 'analiza', 'zwierzę', 'inny',
                               'odpowiedź', 'jakikolwiek', 'ktokolwiek', 'cokolwiek', 'pojawić się', 'jabłko', 'zastosować', 'podejście', 'obszar', 'kłócić się',
                               'ramię', 'armia', 'wokół', 'przybyć', 'sztuka', 'artykuł', 'artysta', 'jako', 'pytać', 'zakładać',
                               'przy', 'atak', 'uwaga', 'adwokat', 'publiczność', 'autor', 'władza', 'dostępny', 'średni', 'unikać',
                               'nagroda', 'daleko', 'dziecko', 'plecy', 'zły', 'torba', 'równowaga', 'piłka', 'zakaz', 'zespół',
                               'bank', 'bar', 'baza', 'podstawowy', 'bitwa', 'być', 'bić', 'piękny', 'ponieważ', 'stać się',
                               'łóżko', 'przed', 'zacząć', 'zachowanie', 'za', 'wierzyć', 'korzyść', 'najlepszy', 'lepszy', 'pomiędzy',
                               'duży', 'rachunek', 'ptak', 'czarny', 'krew', 'niebieski', 'tablica', 'ciało', 'książka', 'urodzony', 'oboje', 'przeszkadzać', 'butelka', 'pudełko', 'chłopiec',
                               'mózg', 'przerwa', 'przynieść', 'brat', 'budować', 'palić', 'autobus', 'biznes', 'ale', 'kupić', 'przez'
                              ],
        'Example Sentence': [
            'I need a pen.', 'They had to abandon their car in the snow.', 'She has the ability to learn new languages quickly.', 'He is able to lift heavy boxes.', 'The debate around abortion is highly controversial.', 'What are you talking about?', 'The bird flew above the trees.', 'He decided to study abroad for a year.', 'His absence was noted.', 'It is an absolute necessity.',
            'I accept your offer.', 'Do you have access?', 'It was an accident.', 'I will accompany you.', 'She achieved her goal.', 'It was an act of kindness.', 'Take action now.', 'He is very active.', 'He is an actor.', 'Add more sugar.',
            'What is your address?', 'The administration is new.', 'He is an adult.', 'This is a great advance.', 'There is an advantage.', 'I need your advice.', 'It will affect you.', 'I cannot afford it.', 'I am afraid of spiders.', 'Come after 5 PM.',
            'Try again later.', 'What is your age?', 'The agency is open.', 'I agree with you.', 'Fresh air is good.', 'All of them came.', 'Please allow me.', 'I am almost done.', 'She lives alone.', 'Walk along the path.',
            'He has already left.', 'She is also coming.', 'He is always late.', 'That is amazing!', 'He is an American.', 'He is among friends.', 'A large amount of food.', 'The analysis is complete.', 'The cat is an animal.', 'Can I have another one?',
            'What is the answer?', 'Do you have any questions?', 'Anyone can do it.', 'Is there anything I can do?', 'A ship appeared.', 'An apple a day.', 'Apply for the job.', 'A new approach.', 'This is a restricted area.', 'Don\'t argue with me.',
            'He broke his arm.', 'The army is strong.', 'Look around you.', 'When did you arrive?', 'This is modern art.', 'Read the article.', 'She is an artist.', 'He works as a teacher.', 'May I ask a question?', 'I assume you know.',
            'Meet me at the station.', 'The attack failed.', 'Pay attention now.', 'Consult your attorney.', 'The audience applauded.', 'The author is famous.', 'She has authority.', 'Is this seat available?', 'The average score was 70.', 'Avoid that road.',
            'She won an award.', 'Go away now.', 'The baby is sleeping.', 'My back hurts.', 'This is a bad idea.', 'Carry your bag.', 'Find your balance.', 'Throw the ball.', 'There is a ban on smoking.', 'The band is playing.',
            'I need to go to the bank.', 'Meet me at the bar.', 'This is the base.', 'These are basic rules.', 'The battle was long.', 'To be or not to be.', 'He beat his record.', 'She is beautiful.', 'I am here because of you.', 'He became a doctor.',
            'Go to bed now.', 'Wash before eating.', 'Let\'s begin the lesson.', 'His behavior was odd.', 'Look behind you.', 'I believe in you.', 'This will benefit you.', 'This is the best option.', 'I feel better now.', 'It is between us.',
            'This is a big house.', 'Pay the bill.', 'A bird is singing.', 'The cat is black.', 'Blood is red.', 'The sky is blue.', 'Write on the board.', 'Take care of your body.', 'Read this book.', 'She was born in May.', 'Both are correct.', 'Don\'t bother him.', 'A bottle of water.', 'Open the box.', 'A young boy.',
            'Use your brain.', 'Take a break.', 'Bring it here.', 'He is my brother.', 'They will build a house.', 'The fire will burn.', 'Take the bus.', 'This is my business.', 'I like it, but...', 'I will buy it.', 'Come by my office.'
            ]
    }
    min_len = min(len(data['English Word']), len(data['Polish Translation']), len(data['Example Sentence']))
    for key_val in data:
        data[key_val] = data[key_val][:min_len]

    df = pd.DataFrame(data)
    return df.to_dict('records')

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

# Apply global styles for font and specific orange highlights
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
        st.session_state.round_number += 1
        st.session_state.stage = "learning_individual"
        st.session_state.current_word_set = get_new_word_set(st.session_state.all_words, 10, st.session_state.seen_words_indices)
        if not st.session_state.current_word_set:
            st.error("Could not load words. Please ensure the word list is populated.")
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
        st.markdown(f"📖 Example: {highlighted_sentence}", unsafe_allow_html=True)
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
    st.info("Match the Polish word with its English translation. You have 1 minute for the whole test.")

    time_elapsed_test = time.time() - st.session_state.timer_start_time
    time_remaining_test = max(0, 60 - int(time_elapsed_test))

    progress_bar_test_placeholder = st.empty()
    timer_text_test_placeholder = st.empty()
    progress_bar_test_placeholder.progress(time_remaining_test / 60)
    timer_text_test_placeholder.markdown(f"<p class='timer-text'>Test time remaining: {time_remaining_test}s</p>", unsafe_allow_html=True)

    if time_remaining_test <= 0 and 'submitted_test' not in st.session_state:
        st.warning("Time's up! Moving to results with current selections (if any).")
        st.session_state.submitted_test = True # Mark as submitted due to timeout
        # Try to capture whatever is in the form if time runs out.
        # This part is tricky as st.form values are usually only available on explicit submit.
        # For now, we'll assume it moves to results and processes what might have been submitted or empty.
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
    elif 'submitted_test' in st.session_state and st.session_state.stage != "results": # Clean up if submitted but not yet in results
        del st.session_state.submitted_test


# --- Results Stage ---
elif st.session_state.stage == "results":
    st.header(f"📊 Round {st.session_state.round_number}: Results!")
    round_score = 0
    if not st.session_state.test_answers:
        st.warning("No answers were processed for the test.")
    else:
        for pl_word, answers_data in st.session_state.test_answers.items():
            selected_answer = str(answers_data.get('selected', "Not Answered"))
            correct_answer = str(answers_data.get('correct', ""))
            pl_word_str = str(pl_word)

            if selected_answer == correct_answer:
                st.success(f"**{pl_word_str}**: Your answer <span class='orange-text'>{selected_answer}</span> was CORRECT! 🎉", unsafe_allow_html=True)
                round_score += 1
            elif selected_answer == "Not Answered":
                st.info(f"**{pl_word_str}**: Not answered. Correct was: <span class='orange-text'>{correct_answer}</span>", unsafe_allow_html=True)
            else:
                st.error(f"**{pl_word_str}**: Your answer <span class='orange-text'>{selected_answer}</span> was INCORRECT. Correct was: <span class='orange-text'>{correct_answer}</span> 🙁", unsafe_allow_html=True)

        if st.session_state.current_word_set: # Check if word set exists
            st.subheader(f"You scored {round_score} out of {len(st.session_state.current_word_set)} in this round.")
            # Ensure score is added only once per round
            round_scored_key = f"round_{st.session_state.round_number}_scored"
            if not st.session_state.get(round_scored_key, False): # Check if this round was already scored
                 st.session_state.score += round_score
                 st.session_state[round_scored_key] = True # Mark as scored
        else:
            st.subheader("No words in this round to score against.")

    st.metric(label="Total Score", value=st.session_state.score)

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
            if 'submitted_test' in st.session_state: del st.session_state.submitted_test # Clean up for next round
            st.rerun()
    with col2:
        if st.button("Restart Game 🔄", use_container_width=True):
            keys_to_keep = ['all_words'] # Preserve the loaded word list
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            # Re-initialize essential states
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
    st.session_state.score = 0 # Reset score on unknown stage
    st.session_state.round_number = 0 # Reset round number
    st.rerun()
