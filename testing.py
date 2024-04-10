import requests, uuid, datetime, unittest

class TestFlagSystem(unittest.TestCase):
    
    
    def setUp(self):
        self.baseURL = 'http://127.0.0.1:9999/'

        self.teams = [str(uuid.uuid4()) for _ in range(5)]
        self.challenges = [str(uuid.uuid4()) for _ in range(10)]


    def test_poisoned_flag_initiation(self):
        poisoned_flags = ['TH{Th1s_1s_a_fak3_fl@g}', 'TH{cant_stop_flag_sharing}']

        res = requests.post(f'{self.baseURL}poisoned', json=poisoned_flags)
        self.assertEqual(res.status_code, 200, msg="Successfully added poisoned flags via endpoint '/poisoned'.")


    def test_initiate_flags_and_solve_challenges(self):

        # Team 1 Starts challenge
        flag_1 = f'TH{uuid.uuid4()}'
        start_time = datetime.datetime.now().timestamp()

        flag_initiation_1 = {
            'team_id': self.teams[0],
            'flag': flag_1,
            'challenge_id': self.challenges[0],
            'initiation_time': start_time
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation_1)
        self.assertEqual(res.status_code, 200)

        # Team 2 Starts challenge
        flag_2 = f'{uuid.uuid4()}'

        flag_initiation_2 = {
            'team_id': self.teams[1],
            'flag': flag_2,
            'challenge_id': self.challenges[0],
            'initiation_time': start_time + 4
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation_2)
        self.assertEqual(res.status_code, 200)

        # Team 3 Starts challenge
        flag_3 = f'{uuid.uuid4()}'

        flag_initiation_3 = {
            'team_id': self.teams[2],
            'flag': flag_3,
            'challenge_id': self.challenges[1],
            'initiation_time': start_time + 7
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation_3)
        self.assertEqual(res.status_code, 200)

        # Team 4 Starts challenge
        flag_4 = f'{uuid.uuid4()}'

        flag_initiation_4 = {
            'team_id': self.teams[3],
            'flag': flag_4,
            'challenge_id': self.challenges[1],
            'initiation_time': start_time + 12
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation_4)
        self.assertEqual(res.status_code, 200)

        # Team 4 Starts challenge
        flag_5 = f'{uuid.uuid4()}'

        flag_initiation_5 = {
            'team_id': self.teams[4],
            'flag': flag_5,
            'challenge_id': self.challenges[2],
            'initiation_time': start_time + 20
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation_5)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge
        flag_submission_1 = {
            'flag': flag_1,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[0],
            'submission_time': start_time + 301,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission_1)
        self.assertEqual(res.status_code, 200)

        # Team 2 tries to solve challenge with flag from team 1 
        flag_submission_2 = {
            'flag': flag_1,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[0],
            'submission_time': start_time + 417,
            'static': False
        }
        res = requests.post(f'{self.baseURL}submissions', json=flag_submission_2)
        self.assertEqual(res.status_code, 200)

        # Team 3 tries to solve challenge 
        flag_submission_3 = {
            'flag': flag_3,
            'team_id': self.teams[2],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[1],
            'submission_time': start_time + 417,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission_3)
        self.assertEqual(res.status_code, 200)

        # Team 4 tries to solve challenge with poisoned flag
        flag_submission_4 = {
            'flag': "TH{you_fell_for_it}",
            'team_id': self.teams[3],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[1],
            'submission_time': start_time + 417,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission_4)
        self.assertEqual(res.status_code, 200)

        # Team 1 tries to solve OSINT challenge
        flag_submission_6 = {
            'flag': "TH{Austria_Linz}",
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[3],
            'submission_time': start_time + 782,
            'static': True
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission_6)
        self.assertEqual(res.status_code, 200)

        # Team 5 tries to solve OSINT challenge
        flag_submission_7 = {
            'flag': "TH{Austria_Linz}",
            'team_id': self.teams[4],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[3],
            'submission_time': start_time + 845,
            'static': True
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission_7)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 6
        flag_6 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_6,
            'challenge_id': self.challenges[5],
            'initiation_time': start_time + 900
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 6
        flag_7 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_7,
            'challenge_id': self.challenges[5],
            'initiation_time': start_time + 913
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 6 
        flag_submission = {
            'flag': flag_6,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[5],
            'submission_time': start_time + 1043,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 6 
        flag_submission = {
            'flag': flag_7,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[5],
            'submission_time': start_time + 1056,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 7
        flag_8 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_8,
            'challenge_id': self.challenges[6],
            'initiation_time': start_time + 1060
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 7
        flag_9 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_9,
            'challenge_id': self.challenges[6],
            'initiation_time': start_time + 1062
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 7
        flag_submission = {
            'flag': flag_8,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[6],
            'submission_time': start_time + 1103,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 7 
        flag_submission = {
            'flag': flag_9,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[6],
            'submission_time': start_time + 1204,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 8
        flag_10 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_10,
            'challenge_id': self.challenges[7],
            'initiation_time': start_time + 1305
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 8
        flag_11 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_11,
            'challenge_id': self.challenges[7],
            'initiation_time': start_time + 1335
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 8
        flag_submission = {
            'flag': flag_10,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[7],
            'submission_time': start_time + 1505,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 8
        flag_submission = {
            'flag': flag_11,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[7],
            'submission_time': start_time + 1603,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 9
        flag_12 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_12,
            'challenge_id': self.challenges[8],
            'initiation_time': start_time + 1563
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 9
        flag_13 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_13,
            'challenge_id': self.challenges[8],
            'initiation_time': start_time + 1623
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 9
        flag_submission = {
            'flag': flag_12,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[8],
            'submission_time': start_time + 1724,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 9
        flag_submission = {
            'flag': flag_13,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[8],
            'submission_time': start_time + 1789,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 10
        flag_14 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_14,
            'challenge_id': self.challenges[9],
            'initiation_time': start_time + 1756
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 10
        flag_15 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_15,
            'challenge_id': self.challenges[9],
            'initiation_time': start_time + 1805
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 10
        flag_submission = {
            'flag': flag_14,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[9],
            'submission_time': start_time + 1907,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 10
        flag_submission = {
            'flag': flag_15,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[9],
            'submission_time': start_time + 1920,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)




        # Team 1 starts challenge 4
        flag_16 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[0],
            'flag': flag_16,
            'challenge_id': self.challenges[3],
            'initiation_time': start_time + 1965
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 2 starts challenge 4
        flag_17 = f'{uuid.uuid4()}'

        flag_initiation = {
            'team_id': self.teams[1],
            'flag': flag_17,
            'challenge_id': self.challenges[3],
            'initiation_time': start_time + 1930
        }
        res = requests.post(f'{self.baseURL}initiate_flag', json=flag_initiation)
        self.assertEqual(res.status_code, 200)

        # Team 1 solves challenge 4
        flag_submission = {
            'flag': flag_14,
            'team_id': self.teams[0],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[3],
            'submission_time': start_time + 2095,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200)

        # Team 2 solves challenge 4
        flag_submission = {
            'flag': flag_17,
            'team_id': self.teams[1],
            'user_id': f'{uuid.uuid4()}',
            'challenge_id': self.challenges[3],
            'submission_time': start_time + 1999,
            'static': False
        }
        res = requests.post(f'{self.baseURL}solved', json=flag_submission)
        self.assertEqual(res.status_code, 200, msg="Successfully ran test events for user submissions & initiations.")


    def test_rndm_poisoned_flags(self):
        res = requests.post(f'{self.baseURL}rndm_poisoned', params={'amount': 10})
        self.assertEqual(res.status_code, 200, msg="Successfully generated random poisoned flags(UUIDs) via endpoint '/rndm_poisoned'.")


    def test_poisoned_flags(self):
        res = requests.get(f'{self.baseURL}poisoned')
        self.assertEqual(res.status_code, 200, msg="Successfully retrieved poisoned flags via endpoint '/poisoned'.")


    def test_flagged_users_and_teams(self):
        res = requests.get(f'{self.baseURL}flagged')
        self.assertEqual(res.status_code, 200, msg="Successfully retrieved flagged teams & users via endpoint '/flagged'.")


if __name__ == '__main__':
    unittest.main()