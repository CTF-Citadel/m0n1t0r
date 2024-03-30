import requests, uuid, datetime

baseURL = 'http://127.0.0.1:9999/'

# Testing Setup
team_1 = f'{uuid.uuid4()}'
team_2 = f'{uuid.uuid4()}'
team_3 = f'{uuid.uuid4()}'
team_4 = f'{uuid.uuid4()}'
team_5 = f'{uuid.uuid4()}'

challenge_1 = f'{uuid.uuid4()}'
challenge_2 = f'{uuid.uuid4()}'
challenge_3 = f'{uuid.uuid4()}'
challenge_4 = f'{uuid.uuid4()}'
challenge_5 = f'{uuid.uuid4()}'


# Team 1 Starts challenge
flag_1 = f'TH{uuid.uuid4()}'
start_time = datetime.datetime.now().timestamp()

flag_initiation_1 = {
    'team_id': team_1,
    'flag': flag_1,
    'challenge_id': challenge_1,
    'initiation_time': start_time
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation_1)


# Team 2 Starts challenge
flag_2 = f'{uuid.uuid4()}'

flag_initiation_2 = {
    'team_id': team_2,
    'flag': flag_2,
    'challenge_id': challenge_1,
    'initiation_time': start_time + 4
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation_2)


# Team 3 Starts challenge
flag_3 = f'{uuid.uuid4()}'

flag_initiation_3 = {
    'team_id': team_3,
    'flag': flag_3,
    'challenge_id': challenge_2,
    'initiation_time': start_time + 7
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation_3)


# Team 4 Starts challenge
flag_4 = f'{uuid.uuid4()}'

flag_initiation_4 = {
    'team_id': team_4,
    'flag': flag_4,
    'challenge_id': challenge_2,
    'initiation_time': start_time + 12
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation_4)


# Team 4 Starts challenge
flag_5 = f'{uuid.uuid4()}'

flag_initiation_5 = {
    'team_id': team_5,
    'flag': flag_5,
    'challenge_id': challenge_3,
    'initiation_time': start_time + 20
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation_5)


# Team 1 solves challenge
flag_submission_1 = {
    'flag': flag_1,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_1,
    'submission_time': start_time + 301,
    'static': False
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_1)


# Team 2 tries to solve challenge with flag from team 1 
flag_submission_2 = {
    'flag': flag_1,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_1,
    'submission_time': start_time + 417,
    'static': False
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_2)


# Team 3 tries to solve challenge with poisoned flag
flag_submission_3 = {
    'flag': flag_3,
    'team_id': team_3,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_2,
    'submission_time': start_time + 417,
    'static': False
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_3)

# Team 4 tries to solve challenge with poisoned flag
flag_submission_4 = {
    'flag': "TH{you_fell_for_it}",
    'team_id': team_4,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_2,
    'submission_time': start_time + 417,
    'static': False
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_4)

# Team 1 tries to solve OSINT challenge
flag_submission_6 = {
    'flag': "TH{Austria_Linz}",
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 782,
    'static': True
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_6)

# Team 5 tries to solve OSINT challenge
flag_submission_7 = {
    'flag': "TH{Austria_Linz}",
    'team_id': team_5,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 845,
    'static': True
}
res = requests.post(f'{baseURL}submissions', json=flag_submission_7)