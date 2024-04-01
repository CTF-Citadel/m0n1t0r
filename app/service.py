from fastapi import FastAPI, HTTPException
from model.database import DBSession
from model.models import Submission, Initiated_Flag, Flagged, Poisoned, Solved
import json, socket, time, threading, uuid, datetime, re
import uvicorn
from sqlalchemy import or_, and_

app = FastAPI()

flag_prefix = 'TH'

# Configuration for suspicious amount of challenges being submitted in the same order
min_order_streak = 5

# Check Flag-Sharing based on poisoned flag being submitted by a team
def check_poisoned(team, user, challenge, flag, time):
    db = DBSession()

    # Check if team submitted a poisoned flag
    poisoned_flag_check = db.query(Poisoned).filter(Poisoned.flag == flag).all()

    if poisoned_flag_check:
        flagged = Flagged(
            flag=flag, team_id=team, user_id=user, challenge_id=challenge, flagging_time=time, reason='Poisoned flag submitted.'
        )
        db.add(flagged)
        db.commit()
        db.refresh(flagged)
        db.close()
        return True

# Check Flag-Sharing based on flag being submitted from opposite team
def same_flag_check(team, user, challenge, flag, time):
    db = DBSession()

    # Check if team submitted flag from opposite team (from flag initiation)
    initiated_flags_check = db.query(Initiated_Flag).filter(Initiated_Flag.flag == flag).all()

    if initiated_flags_check:
        for initiated_flag in initiated_flags_check:
            if initiated_flag.team_id != team:
                flagged = Flagged(
                    flag=flag, team_id=team, user_id=user, challenge_id=challenge, flagging_time=time, flag_share_team=initiated_flag.team_id, reason='Flag from other team submitted.'
                )
                db.add(flagged)
                db.commit()
                db.refresh(flagged)

                flagged_provider = Flagged(
                    flag=flag, team_id=initiated_flag.team_id, challenge_id=challenge, flagging_time=time, flag_share_team=team, reason='Provided a flag to another team.'
                )
                db.add(flagged_provider)
                db.commit()
                db.refresh(flagged_provider)

        db.close()
        return
    
    # Check if team submitted flag from opposite team (from flag submission)
    submitted_flags_check = db.query(Submission).filter(Submission.flag == flag).all()

    if submitted_flags_check:
        for submitted_flag in submitted_flags_check:
            if submitted_flag.team_id != team:
                flagged = Flagged(
                    flag=flag, team_id=team, user_id=user, challenge_id=challenge, flagging_time=time, reason='Flag from other team submitted.'
                )
                db.add(flagged)
                db.commit()
                db.refresh(flagged)

    db.close()

def check_solving_order(check_team_id, user):
    global current_streak
    db = DBSession()

    try:
        check_team_solves_arr = []
        check_team_solves = db.query(Solved).filter(Solved.team_id == check_team_id).order_by(Solved.timestamp).all()
        
        if check_team_solves:
            for solve in check_team_solves:
                check_team_solves_arr.append(solve.challenge_id)

        teams = db.query(Solved.team_id).distinct().filter(Solved.team_id != check_team_id).all()

        if teams:
            for team_id in teams:
                solves = db.query(Solved).filter(Solved.team_id == team_id[0]).order_by(Solved.timestamp).all()

                team_solves = []

                for solve in solves:
                    team_solves.append(solve.challenge_id)

                max_streak = 0 
                current_streak = 0
                for start_check_team in range(len(check_team_solves_arr)):
                    for start_team in range(len(team_solves)):
                        i = start_check_team
                        j = start_team
                        while i < len(check_team_solves_arr) and j < len(team_solves) and check_team_solves_arr[i] == team_solves[j]:
                            current_streak += 1
                            i += 1
                            j += 1
                        max_streak = max(max_streak, current_streak)
                        current_streak = 0  # Reset current_streak for new streak
                
                if max_streak >= min_order_streak:
                    
                    flag_entry_1 = db.query(Flagged).filter(
                        and_(Flagged.team_id == check_team_id, Flagged.flag_share_team == team_id[0])
                    ).filter(Flagged.reason.startswith("Streak")).first()

                    flag_entry_2 = db.query(Flagged).filter(
                        and_(Flagged.team_id == team_id[0], Flagged.flag_share_team == check_team_id)
                    ).filter(Flagged.reason.startswith("Streak")).first()

                    if flag_entry_1:
                        existing_streak_number_1 = int(re.search(r'\d+', flag_entry_1.reason).group())
                        if max_streak > existing_streak_number_1:
                            flag_entry_1.reason = f"Streak of {max_streak} found"
                            flag_entry_1.flagging_time = datetime.datetime.now().timestamp()

                    if flag_entry_2:
                        existing_streak_number_2 = int(re.search(r'\d+', flag_entry_2.reason).group())
                        if max_streak > existing_streak_number_2:
                            flag_entry_2.reason = f"Streak of {max_streak} found"
                            flag_entry_2.flagging_time = datetime.datetime.now().timestamp()
                        
                    if not flag_entry_1:
                        flag_entry_1 = Flagged(
                            team_id=check_team_id,
                            flagging_time=datetime.datetime.now().timestamp(),
                            reason=f"Streak of {max_streak} found",
                            flag_share_team=team_id[0],
                        )
                        db.add(flag_entry_1)

                    if not flag_entry_2:
                        flag_entry_2 = Flagged(
                            team_id=team_id[0],
                            flagging_time=datetime.datetime.now().timestamp(),
                            reason=f"Streak of {max_streak} found",
                            flag_share_team=check_team_id,
                        )
                        db.add(flag_entry_2)
                    
                    db.commit()

    except Exception as e:
        print(e)

    finally:
        db.close()


# Used to define time-interval in which socket sends flagged accounts
socket_interval = 10

# Function to handle client connections
def handle_client(client_socket):
    try:
        while True:
            db = DBSession()

            flagged = db.query(Flagged).distinct(Flagged.team_id)

            db.close()  

            flagged_entries = []

            for entry in flagged:
                entry_data = {
                    'team_id': entry.team_id,
                    'user_id': entry.user_id,
                    'flag_share_team': entry.flag_share_team
                }

                flagged_entries.append(entry_data)
            
            serialized_entries = json.dumps(flagged_entries)
            client_socket.send(f'{serialized_entries}\n'.encode())

            time.sleep(socket_interval)
            
    except Exception as e:
        client_socket.close()
        print(f"Error occurred: {e}")

    finally:
        client_socket.close()
        print("Client connection closed")


# Function to start the socket server
def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 7777)) 
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Socket server is listening on port 8888")

    while True:
        # Accept incoming connection
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")
        
        # Create a new thread for each client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# Start the socket server in a separate thread
socket_server_thread = threading.Thread(target=start_socket_server)
socket_server_thread.start()



# Endpoint to store flag submissions
@app.post('/submissions', description='An endpoint to receive flag submissions of users.')
async def submit_flag(flag_submission: dict):
    db = DBSession()
    try:
        # Log submission in database
        db_flag_submission = Submission(**flag_submission)
        db.add(db_flag_submission)
        db.commit()
        db.refresh(db_flag_submission)

        # Check if challenge was solved
        flag_check = db.query(Initiated_Flag).filter(Initiated_Flag.flag == flag_submission.get('flag')).all()
        for entry in flag_check:
            if entry.team_id == flag_submission.get('team_id'):
                solved = Solved(
                    team_id=flag_submission.get('team_id'), challenge_id=flag_submission.get('challenge_id'), timestamp=flag_submission.get('submission_time')
                )
                db.add(solved)
                db.commit()
                db.refresh(solved)

        # Check if submitted flag is poisoned
        if check_poisoned(flag_submission.get('team_id'), flag_submission.get('user_id'), flag_submission.get('challenge_id'), flag_submission.get('flag'), flag_submission.get('submission_time')) == True:
            return {"message": "Poisoned flag detected"}
        
        # Only check for wrong flag submissions if challenge is
        if flag_submission.get('static') == False:
            same_flag_check(flag_submission.get('team_id'), flag_submission.get('user_id'), flag_submission.get('challenge_id'), flag_submission.get('flag'), flag_submission.get('submission_time'))

        return {"message": "Flag submitted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit flag: {str(e)}")
    
    finally:
        db.close()

@app.post('/solved', description='An endpoint to receive flag submissions of users which solved a challenge.')
async def solve_flag(flag_submission: dict):
    db = DBSession()
    
    try:
        solved = Solved(
            team_id=flag_submission.get('team_id'), challenge_id=flag_submission.get('challenge_id'), timestamp=flag_submission.get('submission_time')
        )
        db.add(solved)
        db.commit()
        db.refresh(solved)

        if check_poisoned(flag_submission.get('team_id'), flag_submission.get('user_id'), flag_submission.get('challenge_id'), flag_submission.get('flag'), flag_submission.get('submission_time')) == True:
            return {"message": "Poisoned flag detected"}
    
        check_solving_order(flag_submission.get('team_id'), flag_submission.get('user_id'))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit solution flag: {str(e)}")

    finally:
        db.close()

# Endpoint to store flag initiations
@app.post("/initiate_flag", description='An endpoint to receive the intitiated flags from all teams when challenges are deployed.')
async def initiate_flag(flag_initiation: dict):
    db = DBSession()
    try:
        db_flag_initiation = Initiated_Flag(**flag_initiation)
        db.add(db_flag_initiation)
        db.commit()
        db.refresh(db_flag_initiation)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate flag: {str(e)}")
    
    finally:
        db.close()

# Endpoint to retrieve flagged/suspicious users
@app.get('/flagged', description='An endpoint to return flagged users based on same flag submissions or time based analysis of submissions.')
async def flagged():
    db = DBSession()
    
    try:
        flagged = db.query(Flagged.team_id).distinct(Flagged.team_id)

        flagged_entries = []

        for flag in flagged:
            entries = db.query(Flagged).filter(Flagged.team_id == flag[0]).all()

            flagged_entry = {
                'team_id': flag[0], 
            }

            current_suspicion_lvl = 0
            for i, entry in enumerate(entries):

                match entry.reason:
                    case 'Flag from other team submitted.':
                        current_suspicion_lvl = 3
                        flagged_entry[f'mark_{i}'] = {
                            'flagged_user': entry.user_id,
                            'flag_share_team': entry.flag_share_team,
                            'reason': entry.reason
                        }
                    case 'Poisoned flag submitted.':
                        current_suspicion_lvl = 3
                        flagged_entry[f'mark_{i}'] = {
                            'flagged_user': entry.user_id,
                            'reason': entry.reason
                        }
                    case 'Provided a flag to another team.':
                        current_suspicion_lvl = 3
                        flagged_entry[f'mark_{i}'] = {
                            'flag_share_team': entry.flag_share_team,
                            'reason': entry.reason
                        }
                    case _:
                        streak = int(re.search(r'\d+', entry.reason).group())

                        if streak >= min_order_streak and streak < min_order_streak + 2:
                            current_suspicion_lvl = 1
                        elif streak >= min_order_streak + 2 and streak < min_order_streak + 4:
                            current_suspicion_lvl = 2
                        elif streak >= min_order_streak + 4:
                            current_suspicion_lvl = 3

                        flagged_entry[f'mark_{i}'] = {
                            'flag_share_team': entry.flag_share_team,
                            'reason': entry.reason
                        }
            
                if 'suspicion_lvl' not in flagged_entry or flagged_entry['suspicion_lvl'] < current_suspicion_lvl:
                    flagged_entry['suspicion_lvl'] = current_suspicion_lvl

            flagged_entries.append(flagged_entry)

        return flagged_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract flagged accounts: {str(e)}")

    finally:
        db.close()


@app.get('/poisoned', description='Get all poisonous flags from the database.')
async def get_poisoned():
    db = DBSession()

    try:
        poisoned_flags = db.query(Poisoned).all()
        flags_data = [flag.flag for flag in poisoned_flags]
        return flags_data
    
    finally:
        db.close()

@app.post('/poisoned', description='Pass a list of poisoned flags (in json format) which will be marked as poisonous by the system.')
async def pass_poisoned(flags: list[str]):
    db = DBSession()

    try:
        for flag in flags:
            db.add(Poisoned(flag=flag))
        db.commit()
        return {"message": f"{len(flags)} poisoned flags marked successfully."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    finally:
        db.close()

@app.post('/rndm_poisoned', description='Generate a certain amount of poisoned flags with UUIDs.')
async def gen_poisoned(amount: int):
    db = DBSession()

    try:
        for _ in range(0, amount + 1):
            db.add(Poisoned(flag=f'{flag_prefix}{{{uuid.uuid4()}}}'))
        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5555)