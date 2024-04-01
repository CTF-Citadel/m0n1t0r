import requests, uuid, datetime

baseURL = 'http://127.0.0.1:9999/'

# Testing Setup
team_1 = f'{uuid.uuid4()}'
team_2 = f'{uuid.uuid4()}'
team_3 = f'{uuid.uuid4()}'
team_4 = f'{uuid.uuid4()}'
team_5 = f'{uuid.uuid4()}'

print(f'Team-1: {team_1},\nTeam-2: {team_2},\nTeam-3: {team_3},\nTeam-4: {team_4},\nTeam-5: {team_5},\n')

challenge_1 = f'{uuid.uuid4()}'
challenge_2 = f'{uuid.uuid4()}'
challenge_3 = f'{uuid.uuid4()}'
challenge_4 = f'{uuid.uuid4()}'
challenge_5 = f'{uuid.uuid4()}'
challenge_6 = f'{uuid.uuid4()}'
challenge_7 = f'{uuid.uuid4()}'
challenge_8 = f'{uuid.uuid4()}'
challenge_9 = f'{uuid.uuid4()}'
challenge_10 = f'{uuid.uuid4()}'

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
res = requests.post(f'{baseURL}solved', json=flag_submission_1)


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


# Team 3 tries to solve challenge 
flag_submission_3 = {
    'flag': flag_3,
    'team_id': team_3,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_2,
    'submission_time': start_time + 417,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission_3)

# Team 4 tries to solve challenge with poisoned flag
flag_submission_4 = {
    'flag': "TH{you_fell_for_it}",
    'team_id': team_4,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_2,
    'submission_time': start_time + 417,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission_4)

# Team 1 tries to solve OSINT challenge
flag_submission_6 = {
    'flag': "TH{Austria_Linz}",
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 782,
    'static': True
}
res = requests.post(f'{baseURL}solved', json=flag_submission_6)

# Team 5 tries to solve OSINT challenge
flag_submission_7 = {
    'flag': "TH{Austria_Linz}",
    'team_id': team_5,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 845,
    'static': True
}
res = requests.post(f'{baseURL}solved', json=flag_submission_7)





# Team 1 starts challenge 6
flag_6 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_6,
    'challenge_id': challenge_6,
    'initiation_time': start_time + 900
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 6
flag_7 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_7,
    'challenge_id': challenge_6,
    'initiation_time': start_time + 913
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 6 
flag_submission = {
    'flag': flag_6,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_6,
    'submission_time': start_time + 1043,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 6 
flag_submission = {
    'flag': flag_7,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_6,
    'submission_time': start_time + 1056,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)





# Team 1 starts challenge 7
flag_8 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_8,
    'challenge_id': challenge_7,
    'initiation_time': start_time + 1060
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 7
flag_9 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_9,
    'challenge_id': challenge_7,
    'initiation_time': start_time + 1062
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 7
flag_submission = {
    'flag': flag_8,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_7,
    'submission_time': start_time + 1103,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 7 
flag_submission = {
    'flag': flag_9,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_7,
    'submission_time': start_time + 1204,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)





# Team 1 starts challenge 8
flag_10 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_10,
    'challenge_id': challenge_8,
    'initiation_time': start_time + 1305
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 8
flag_11 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_11,
    'challenge_id': challenge_8,
    'initiation_time': start_time + 1335
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 8
flag_submission = {
    'flag': flag_10,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_8,
    'submission_time': start_time + 1505,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 8
flag_submission = {
    'flag': flag_11,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_8,
    'submission_time': start_time + 1603,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)





# Team 1 starts challenge 9
flag_12 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_12,
    'challenge_id': challenge_9,
    'initiation_time': start_time + 1563
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 9
flag_13 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_13,
    'challenge_id': challenge_9,
    'initiation_time': start_time + 1623
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 9
flag_submission = {
    'flag': flag_12,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_9,
    'submission_time': start_time + 1724,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 9
flag_submission = {
    'flag': flag_13,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_9,
    'submission_time': start_time + 1789,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)





# Team 1 starts challenge 10
flag_14 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_14,
    'challenge_id': challenge_10,
    'initiation_time': start_time + 1756
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 10
flag_15 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_15,
    'challenge_id': challenge_10,
    'initiation_time': start_time + 1805
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 10
flag_submission = {
    'flag': flag_14,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_10,
    'submission_time': start_time + 1907,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 10
flag_submission = {
    'flag': flag_15,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_10,
    'submission_time': start_time + 1920,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)





# Team 1 starts challenge 4
flag_16 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_1,
    'flag': flag_16,
    'challenge_id': challenge_4,
    'initiation_time': start_time + 1965
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 2 starts challenge 4
flag_17 = f'{uuid.uuid4()}'

flag_initiation = {
    'team_id': team_2,
    'flag': flag_17,
    'challenge_id': challenge_4,
    'initiation_time': start_time + 1930
}
res = requests.post(f'{baseURL}initiate_flag', json=flag_initiation)

# Team 1 solves challenge 4
flag_submission = {
    'flag': flag_14,
    'team_id': team_1,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 2095,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)

# Team 2 solves challenge 4
flag_submission = {
    'flag': flag_17,
    'team_id': team_2,
    'user_id': f'{uuid.uuid4()}',
    'challenge_id': challenge_4,
    'submission_time': start_time + 1999,
    'static': False
}
res = requests.post(f'{baseURL}solved', json=flag_submission)