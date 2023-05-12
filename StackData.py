import requests
import sqlite3
import pandas as pd


def to_sql(db_con: sqlite3.connect) -> None:
    # get my recent answers and create a DataFrame
    answers = requests.get(
        'https://api.stackexchange.com/2.3/users/9177877/answers?order=desc&sort=activity&site=stackoverflow'
    ).json()
    df_answers = pd.json_normalize(answers['items'])[['answer_id', 'question_id', 'score', 'creation_date']]
    df_answers['link'] = 'https://stackoverflow.com/a/'+df_answers['answer_id'].astype(str)

    # get the questions for my answers
    q_ids = ';'.join(df_answers['question_id'].astype(str))
    questions = requests.get(
        f'https://api.stackexchange.com/2.3/questions/{q_ids}?order=desc&sort=activity&site=stackoverflow'
    ).json()
    df_questions = pd.json_normalize(questions['items'])[['question_id', 'title', 'link']]

    # merge frames together
    qa_df = df_questions.merge(df_answers, on='question_id', suffixes=['_q', '_a'])
    qa_df['creation_date'] = pd.to_datetime(qa_df['creation_date'], unit='s').dt.date
    qa_df['title'] = qa_df['title'].str.replace('&quot;', '"')

    # get my top answers and create a DataFrame
    top_answers = requests.get('https://api.stackexchange.com/2.3/users/9177877/tags/pandas/top-answers?order=desc'
                               '&sort=activity&site=stackoverflow').json()
    top_answer_df = pd.json_normalize(top_answers['items'])[['answer_id', 'question_id', 'score', 'creation_date']]
    top_answer_df['link'] = 'https://stackoverflow.com/a/' + top_answer_df['answer_id'].astype(str)

    # get the questions for my answers
    top_q_ids = ';'.join(top_answer_df['question_id'].astype(str))
    top_questions = requests.get(
        f'https://api.stackexchange.com/2.3/questions/{top_q_ids}?order=desc&sort=activity&site=stackoverflow'
    ).json()
    top_questions_df = pd.json_normalize(top_questions['items'])[['question_id', 'title', 'link']]
    top_qa_df = top_questions_df.merge(top_answer_df, on='question_id',  suffixes=['_q', '_a'])
    top_qa_df['creation_date'] = pd.to_datetime(top_qa_df['creation_date'], unit='s').dt.date
    top_qa_df['title'] = top_qa_df['title'].str.replace('&quot;', '"')

    # save df to sql db and replace
    # we do not need to keep all the data as I am just displaying the most recent
    qa_df.to_sql('recent_answers', db_con, index=False, if_exists='replace')
    top_qa_df.to_sql('top_answers', db_con, index=False, if_exists='replace')
