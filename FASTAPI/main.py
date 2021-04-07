from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import json
app = FastAPI()


class File(BaseModel):
    audio_type: str
    audio_meta: dict


@app.get('/')
async def index():
    return {'Welcome'}


@app.post('/create')
async def create_file(file: File):
    try:
        conn = mysql.connector.connect(host="localhost", user="root",
                                       password="root",
                                       database="phase_two",
                                       auth_plugin='mysql_native_password')
        cur = conn.cursor()
        cur.execute('INSERT INTO app_table (audio_type, audio_meta) \
                    VALUES (%s,%s)',
                    [file.audio_type, json.dumps(file.audio_meta)])
        conn.commit()
        conn.close()
        return {'result': '200 OK'}
    except Exception as e:
        print("error: {0}".format(e))


@app.get('/{file_type}')
async def get_file(file_type):
    try:
        conn = mysql.connector.connect(host="localhost", user="root",
                                       password="root",
                                       database="phase_two",
                                       auth_plugin='mysql_native_password')
        cur = conn.cursor()
        # print(cur)
        cur.execute('SELECT * from app_table where audio_type=%s', [file_type])
        myresult = cur.fetchall()
        # cursor = cursor.fetchall()
        result = []
        for obj in myresult:
            user = {}
            user['type'] = obj[0]
            user['meta'] = json.loads(obj[1].replace("'", '"'))
            result.append(user)
        return result
    except Exception as e:
        print("error: {0}".format(e))


@app.get('/{file_type}/{file_id}')
async def get_unique_file(file_type, file_id):
    try:
        conn = mysql.connector.connect(host="localhost", user="root",
                                       password="root", database="phase_two",
                                       auth_plugin='mysql_native_password')
        cur = conn.cursor()
        cur.execute("SELECT * from app_table where audio_type=%s and \
                    json_extract(audio_meta,'$.ID') = %s",
                    [file_type, int(file_id)])
        myresult = cur.fetchall()
        result = []
        for obj in myresult:
            user = {}
            user['type'] = obj[0]
            user['meta'] = json.loads(obj[1].replace("'", '"'))
            result.append(user)
        return result
    except Exception as e:
        print("error: {0}".format(e))


@app.delete('/{file_type}/{file_id}')
async def delete(file_type, file_id):
    try:
        conn = mysql.connector.connect(host="localhost", user="root",
                                       password="root",
                                       database="phase_two",
                                       auth_plugin='mysql_native_password')
        cur = conn.cursor()
        cur.execute("DELETE FROM app_table where audio_type=%s and \
                    json_extract(audio_meta,'$.ID') = %s",
                    [file_type, int(file_id)])
        conn.commit()
        conn.close()
        return {'result': '200 OK'}
    except Exception as e:
        print("error: {0}".format(e))


@app.put('/{file_type}/{file_id}')
async def update(file_type, file_id, file: File):
    try:
        conn = mysql.connector.connect(host="localhost", user="root",
                                       password="root",
                                       database="phase_two",
                                       auth_plugin='mysql_native_password')
        cur = conn.cursor()
        cur.execute("UPDATE app_table SET audio_type=%s , audio_meta=%s where \
                    audio_type=%s and json_extract(audio_meta,'$.ID') = %s", [
                    file.audio_type, json.dumps(file.audio_meta), file_type,
                    int(file_id)])
        conn.commit()
        conn.close()
        return {'result': '200 OK'}
    except Exception as e:
        print("error: {0}".format(e))
