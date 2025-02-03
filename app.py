import pandas as pd
import scipy.stats
import streamlit as st
import time

# these are stateful variables which are preserved as Streamlit reruns this script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

if 'mean_list' not in st.session_state:  # Store mean values to plot
    st.session_state['mean_list'] = []

st.header('Tossing a Coin')

# Initialize the chart with the mean_list from session_state
chart = st.line_chart(st.session_state['mean_list'])  # Use session_state to store the chart data

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_1_count = 0
    outcome_no = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        st.session_state['mean_list'].append(mean)  # Append the mean to the list in session_state
        
        # Re-render the chart with updated data
        chart.line_chart(st.session_state['mean_list'])  
        time.sleep(0.05)  # Add delay to simulate coin toss

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0
    )
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
