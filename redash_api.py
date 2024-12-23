import requests
import streamlit as st
import pandas as pd
import time
from config import REDASH_URL, API_KEY

def redash_query(query_id, params={}):
    try:
        url = f'{REDASH_URL}/api/queries/{query_id}/results'
        headers = {'Authorization': f'Key {API_KEY}'}
        body = {'max_age': 0, 'parameters': params}

        with st.spinner('Đang truy vấn dữ liệu...'):
            r = requests.post(url=url, headers=headers, json=body)
            r.raise_for_status()
            job_id = r.json()['job']['id']

        result_id = redash_job_check(job_id)
        res = redash_result_get(result_id)
        return res
    except Exception as e:
        st.error(f'Có lỗi xảy ra: {str(e)}')
        return None

def redash_job_check(job_id):
    url = f'{REDASH_URL}/api/jobs/{job_id}'
    headers = {'Authorization': f'Key {API_KEY}'}
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            r = requests.get(url=url, headers=headers)
            r.raise_for_status()
            response_json = r.json()
            status = response_json['job']['status']

            if status == 4:
                error_message = response_json['job'].get('error', 'Unknown error')
                st.error(f'Query failed! Error message: {error_message}')
                raise Exception(error_message)
            elif status == 3:
                return response_json['job']['query_result_id']

            retry_count += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            st.error(f'Network error: {str(e)}')
            raise Exception(f'Network error: {str(e)}')

    raise Exception('Query timeout - exceeded maximum retries')

def redash_result_get(query_result_id):
    url = f'{REDASH_URL}/api/query_results/{query_result_id}'
    headers = {'Authorization': f'Key {API_KEY}'}
    try:
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        return pd.DataFrame(r.json()['query_result']['data']['rows'])
    except requests.exceptions.RequestException as e:
        st.error(f'Error fetching results: {str(e)}')
        raise Exception(f'Error fetching results: {str(e)}')