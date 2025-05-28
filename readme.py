import streamlit as st
import pandas as pd
import random
import time
import re # For highlighting words in sentences

# --- Helper Functions ---
@st.cache_data # Cache the data loading
def load_words():
    # This function will parse your document content to extract words.
    # For now, let's use a placeholder.
    # Replace this with your actual data loading (e.g., from a CSV file you create from your document).
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
                        ], # Add at least 100 words for better random sampling
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
            ] # Add more examples
    }
    # Ensure all lists have the same length for DataFrame creation
    min_len = min(len(data['English Word']), len(data['Polish Translation']), len(data['Example Sentence']))
    for key in data:
        data[key] = data[key][:min_len]

    df = pd.DataFrame(data)
    return df.to_dict('records')

ALL_WORDS = load_words()

def get_new_word_set(words_list, num_words=10, seen_indices=None):
    if seen_indices is None:
        seen_indices = set()
    
    available_indices = [i for i, _ in enumerate(words_list) if i not in seen_indices]
    if len(available_indices) < num_words: # If not enough new words, allow repeats or reset
        # For simplicity, if we run out of new words, we'll just sample from all again
        # Or you could signal "all words learned" or allow repeats from seen words.
        st.warning("Not enough new words, sampling from all words again. Consider restarting for fresh unseen words if available.")
        available_indices = list(range(len(words_list)))
        if not available_indices: # Should not happen if ALL_WORDS is not empty
             return []


    chosen_indices = random.sample(available_indices, min(num_words, len(available_indices)))
    new_set = [words_list[i] for i in chosen_indices]
    
    # Update seen_indices with the newly chosen ones
    for i in chosen_indices:
        seen_indices.add(i)
        
    return new_set


def highlight_word_in_sentence(sentence, word_to_highlight):
    # Use regex for case-insensitive replacement and to handle whole words
    try:
        # Escape special characters in the word_to_highlight for regex
        escaped_word = re.escape(word_to_highlight)
        highlighted_sentence = re.sub(
            f"\\b({escaped_word})\\b",
            r"<span style='color:orange; font-weight:bold;'>\1</span>",
            sentence,
            flags=re.IGNORECASE
        )
        return highlighted_sentence
    except Exception:
        return sentence # Fallback if regex fails


# --- Streamlit App ---
st.set_page_config(layout="centered") # Centered layout often looks more appealing

# Apply global styles for font and specific orange highlights
st.markdown("""
    <style>
        body, .stApp, .stButton>button, .stSelectbox div[data-baseweb='select'] > div, .stTextInput > div > div > input, .stMetric > div > div {
            font-size: 18px !important; /* Consistent font size */
        }
        .stSubheader { /* Target st.subheader */
            font-size: 22px !important;
            font-weight: bold;
        }
        .orange-text {
            color: orange;
            font-weight: bold; /* Make orange text bold for emphasis */
        }
        /* Style for the timer text */
        .timer-text {
            font-size: 20px !important;
            font-weight: bold;
            color: #1E90FF; /* DodgerBlue */
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
    st.session_state.seen_words_indices = set() # Store indices of words shown for the session
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
        if not st.session_state.current_word_set: # Handle case where no words could be fetched
            st.error("Could not load words. Please check the word list.")
            st.session_state.stage = "welcome" # Go back to welcome
        else:
            st.session_state.current_learning_word_index = 0
            st.session_state.learning_word_start_time = time.time()
        st.rerun()

# --- Learning Stage (Individual Word Display) ---
elif st.session_state.stage == "learning_individual":
    if not st.session_state.current_word_set or st.session_state.current_learning_word_index >= len(st.session_state.current_word_set):
        st.session_state.stage = "test"
        st.session_state.timer_start_time = time.time() # Timer for the whole test
        st.session_state.test_answers = {}
        st.rerun()
    else:
        word_data = st.session_state.current_word_set[st.session_state.current_learning_word_index]
        st.header(f"🧠 Round {st.session_state.round_number}: Learn Word {st.session_state.current_learning_word_index + 1}/{len(st.session_state.current_word_set)}")

        time_elapsed_word = time.time() - st.session_state.learning_word_start_time
        time_remaining_word = max(0, 5 - int(time_elapsed_word))

        timer_placeholder_word = st.empty()
        timer_placeholder_word.markdown(f"<p class='timer-text'>Time for this word: {time_remaining_word}s</p>", unsafe_allow_html=True)

        # Display current word
        st.markdown(f"## <span class='orange-text'>{word_data['English Word']}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🇵🇱 {word_data['Polish Translation']}")
        highlighted_sentence = highlight_word_in_sentence(word_data['Example Sentence'], word_data['English Word'])
        st.markdown(f"📖 Example: {highlighted_sentence}", unsafe_allow_html=True)
        st.markdown("---")

        if time_remaining_word <= 0:
            st.session_state.current_learning_word_index += 1
            if st.session_state.current_learning_word_index < len(st.session_state.current_word_set):
                st.session_state.learning_word_start_time = time.time() # Reset timer for next word
            st.rerun()
        else:
            # Force a rerun every second to update the timer display
            time.sleep(1)
            st.rerun()


# --- Test Stage ---
elif st.session_state.stage == "test":
    st.header(f"✏️ Round {st.session_state.round_number}: Test your knowledge!")
    st.info("Match the Polish word with its English translation. You have 1 minute for the whole test.")

    time_elapsed_test = time.time() - st.session_state.timer_start_time
    time_remaining_test = max(0, 60 - int(time_elapsed_test))

    progress_bar_test = st.progress(time_remaining_test / 60)
    timer_text_test = st.markdown(f"<p class='timer-text'>Test time remaining: {time_remaining_test}s</p>", unsafe_allow_html=True)


    if time_remaining_test <= 0 and not st.session_state.test_answers: # If time ran out and no submission yet
        st.warning("Time's up! Moving to results.")
        st.session_state.stage = "results" # Will process with potentially empty answers
        st.rerun()

    polish_words_for_test = [word['Polish Translation'] for word in st.session_state.current_word_set]
    english_options = [word['English Word'] for word in st.session_state.current_word_set]
    # random.shuffle(polish_words_for_test) # Shuffling questions can be good

    # Create a dictionary to hold selections for the form
    if 'form_selections' not in st.session_state:
        st.session_state.form_selections = {pl_word: None for pl_word in polish_words_for_test}

    with st.form(key="test_form"):
        temp_student_answers_map = {}
        for i, pl_word in enumerate(polish_words_for_test):
            correct_en_word = ""
            for wd in st.session_state.current_word_set:
                if wd['Polish Translation'] == pl_word:
                    correct_en_word = wd['English Word']
                    break
            
            options_for_select = english_options[:]
            random.shuffle(options_for_select)

            # Use a unique key for each selectbox
            selection_key = f"test_q_{st.session_state.round_number}_{i}"
            selected_en_word = st.selectbox(
                f"**{i+1}. {pl_word}** is:",
                options=[""] + options_for_select, # Add an empty option for "not answered"
                index=0, # Default to empty
                key=selection_key
            )
            if selected_en_word: # Only map if an actual option was selected
                 temp_student_answers_map[pl_word] = {
                    "selected": selected_en_word,
                    "correct": correct_en_word
                }
            else: # Handle case where user doesn't select anything (or selects the blank)
                temp_student_answers_map[pl_word] = {
                    "selected": "Not Answered",
                    "correct": correct_en_word
                }


        submit_button = st.form_submit_button("✅ Submit Answers")

        if submit_button:
            st.session_state.test_answers = temp_student_answers_map
            st.session_state.stage = "results"
            st.rerun()

    if time_remaining_test > 0: # Only allow forced rerun if time is left
        time.sleep(1) # Refresh the timer display
        st.rerun()


# --- Results Stage ---
elif st.session_state.stage == "results":
    st.header(f"📊 Round {st.session_state.round_number}: Results!")
    round_score = 0
    if not st.session_state.test_answers:
        st.warning("No answers were processed for the test.")
    else:
        for pl_word, answers_data in st.session_state.test_answers.items():
            selected = answers_data['selected']
            correct = answers_data['correct']
            if selected == correct:
                st.success(f"**{pl_word}**: Your answer <span class='orange-text'>{selected}</span> was CORRECT! 🎉", unsafe_allow_html=True)
                round_score += 1
            elif selected == "Not Answered":
                st.info(f"**{pl_word}**: Not answered. Correct was: <span class='orange-text'>{correct}</span>", unsafe_allow_html=True)
            else:
                st.error(f"**{pl_word}**: Your answer <span class='orange-text'>{selected}</span> was INCORRECT. Correct was: <span class='orange-text'>{correct}</span> 🙁", unsafe_allow_html=True)
        
        if st.session_state.current_word_set: # Avoid division by zero if word set is empty
            st.subheader(f"You scored {round_score} out of {len(st.session_state.current_word_set)} in this round.")
            st.session_state.score += round_score # Add round score to total score
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
            st.session_state.test_answers = {} # Clear for next round
            st.rerun()
    with col2:
        if st.button("Restart Game 🔄", use_container_width=True):
            # Reset relevant session state variables
            st.session_state.stage = "welcome"
            st.session_state.score = 0
            st.session_state.round_number = 0
            st.session_state.seen_words_indices = set()
            st.session_state.current_learning_word_index = 0
            st.session_state.current_word_set = []
            st.session_state.test_answers = {}
            st.rerun()

else:
    st.error("Unknown application stage. Resetting.")
    if st.button("Reset to Welcome"):
        st.session_state.stage = "welcome" # Minimal reset
        st.rerun()
