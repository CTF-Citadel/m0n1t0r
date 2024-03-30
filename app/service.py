from fastapi import FastAPI, HTTPException
from model.database import DBSession
from model.models import Submission, Initiated_Flag, Flagged, Poisoned
import os, json, socket, time, threading, uuid
from datetime import timedelta
import uvicorn

app = FastAPI()

flag_prefix = 'TH'

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
    server_socket.bind(('0.0.0.0', 8888)) 
    
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

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit flag: {str(e)}")
    
    finally:
        db.close()

    # Check if submitted flag is poisoned
    if check_poisoned(flag_submission.get('team_id'), flag_submission.get('user_id'), flag_submission.get('challenge_id'), flag_submission.get('flag'), flag_submission.get('submission_time')) == True:
        return {"message": "Poisoned flag detected"}

    # Check if submitted flag can be found in another teams submission/initiation
    if flag_submission.get('static') == False:
        same_flag_check(flag_submission.get('team_id'), flag_submission.get('user_id'), flag_submission.get('challenge_id'), flag_submission.get('flag'), flag_submission.get('submission_time'))

    return {"message": "Flag submitted successfully"}

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
        flagged = db.query(Flagged).distinct(Flagged.team_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract flagged accounts: {str(e)}")

    finally:
        db.close()

    flagged_entries = []

    for entry in flagged:
        if entry.flag_share_team:
            entry_data = {
                'team_id': entry.team_id,
                'user_id': entry.user_id,
                'flag_share_team': entry.flag_share_team,
                'reason': entry.reason
            }
        else:
            entry_data = {
                'team_id': entry.team_id,
                'user_id': entry.user_id,
                'flag_share_team': entry.flag_share_team,
                'reason': entry.reason
            }

        flagged_entries.append(entry_data)

    return flagged_entries


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
    uvicorn.run(app, host="0.0.0.0", port=9999)