from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import  database_connect
from  utils.get_models import get_model
import utils.text_preprocessing as tp
from numpy import round
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InputData(BaseModel):
    comment: str


class InputData2(BaseModel):
    comment: str
    tone:int


app = FastAPI()
model = get_model()


@app.get('/get_all_comments')
def comments_from_bd():
    data = database_connect.get_comments()
    # print("data"+data)
    logger.error(f"data:{data}")
    result_dict = {"id": [], 'comment': [], "tone_id": []}
    for row in data:
        comment_id = row[0]
        comment_text = row[1]
        tone_id = row[2]
        logger.error(row)
        if tone_id is None:
            logger.info("tone id is none")
            tone_id = prediction(comment_text)
            logger.info(f"new tone_id:{tone_id}")
            database_connect.update_comment_tone({"comment_tone":tone_id, "comment_id":comment_id})

        result_dict['id'].append(comment_id)
        result_dict['comment'].append(comment_text)
        result_dict['tone_id'].append(tone_id)

    return data


@app.post('/predict_tonality_comment')
def predict_tonality_comment(request: InputData):
    clean_comment = tp.remove_punctuation(request.comment)
    clean_comment = tp.lemmatization_text(clean_comment)
    token_text = tp.token_pad(clean_comment)
    predict = model.predict([token_text])[0]
    tone = int(round(float(predict)))
    return {"tone":tone, "probs":float(predict)}


def prediction(text):
    clean_comment = tp.remove_punctuation(text)
    clean_comment = tp.lemmatization_text(clean_comment)
    token_text = tp.token_pad(clean_comment)
    predict = model.predict([token_text])[0]
    tone = int(round(float(predict)))
    return tone

@app.post('/save_comment')
def save_comment(request:InputData2):
    try:
        database_connect.add_new_comment({"comment_text":request.comment, "comment_tone":request.tone})
        return {"result":"Успешно сохранено"}
    except Exception as e:
        return {"result": "Ошибка"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)