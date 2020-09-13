import base64
import cv2
import numpy as np
import os
import PIL
import datetime

from flask import Response

import torch
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog

import face_recognition.api as face_recognition
from facenet_pytorch import MTCNN

import config
import models
import db
import enums

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)

def get_current_datetime():
    return dt.datetime.now().strftime('%Y-%m-%d_%H_%M_%S.%f')

def decode_base64_to_img(encoded_img):
    decoded_img = base64.standard_b64decode(encoded_img)
    img = np.frombuffer(decoded_img, dtype='uint8')
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

def load_detectron2_config():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg.freeze()
    return cfg

detectron2_config = load_detectron2_config()
predictor = DefaultPredictor(detectron2_config)

def process_detectron2_predictions(predictions):
    result_json = []
    outputs = predictions["instances"].to('cpu').get_fields()
    pred_classes = outputs['pred_classes'].numpy()
    pred_boxes = outputs['pred_boxes'].tensor.numpy().astype(int)
    scores = outputs['scores'].numpy()

    for idx in range(len(pred_boxes)):
        if pred_classes[idx] == 67:
            obj = {
                'class': int(pred_classes[idx]),
                'score': float(scores[idx]),
                'label': 'phone',
                'bbox': list(pred_boxes[idx,...])
            }
            result_json.append(obj)
    return result_json

def get_phones_predictions(img):
    predictions = predictor(img)
    return process_detectron2_predictions(predictions)

def get_person_prediction(cv_img, known_students, known_encodings, bboxes, tolerance=0.6):
    img_encodings = face_recognition.face_encodings(cv_img, bboxes)
    res = None
    for enc in img_encodings:
        distances = face_recognition.face_distance(known_encodings, enc)
        result = list(distances <= tolerance)
        if any(result):
            res, _ = sorted(zip(known_students, distances), key=lambda x: x[1])[0]
    return res

def process_frame(data):
    encoded_img = data['frame']
    student_id =  db.db_session.query(models.Student.id).filter_by(email=data['email']).first()

    img = decode_base64_to_img(encoded_img)
    cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    processed_frame = PIL.Image.fromarray(cv_img)
    
    phone_bboxes = get_phones_predictions(img)
    face_bboxes, _ = mtcnn.detect(processed_frame)

    filename = os.path.join(os.getcwd(), config.MONITORING_FOLDER, f'student_{student_id}_frame_{get_current_datetime()}')
    cv2.imwrite(filename, img)

    img_metadata = {}
    is_warning = False
    alert_id = enums.AlertTypes.NO_WARNING

    face_bboxes_list = []
    if face_bboxes is not None:
        for b in face_bboxes:
            face_json = dict(x0=int(b[0]), y0=int(b[1]), x1=int(b[2]), y1=int(b[3]))
            detected_student = get_person_prediction(cv_img, known_students, known_encodings, face_bboxes)
            if detected_student is not None:
                face_json['student'] = detected_student
            else:
                face_json['student'] = 'UNKNOWN_STUDENT'
                is_warning = True
                alert_id = enums.AlertTypes.UNKNOWN_STUDENT
            face_bboxes_list.append(face_json)
        
        if len(face_bboxes) > 1:
            is_warning = True
            alert_id = enums.AlertTypes.SEVERAL_PEOPLE
    else:
        is_warning = True
        alert_id = enums.AlertTypes.NO_PERSON

    if len(phone_bboxes) > 0:
        is_warning = True
        alert_id = enums.AlertTypes.PHONE

    img_metadata['face_bboxes'] = face_bboxes_list
    img_metadata['phone_bboxes'] = phone_bboxes
    img_metadata['is_warning'] = is_warning
    img_metadata['alert_id'] = alert_id

    event = models.Event(student_id=student_id, img_path=filename, img_metadata=img_metadata)
    db.db_session.add(event)
    db.db_session.commit()

    return img_metadata

def process_learn_images(data):
    global known_students, known_encodings, mtcnn
    student_id = db.db_session.query(models.Student.id).filter_by(email=data['email']).scalar()
    if student_id is not None:
        for idx, encoded_image in enumerate(data['frames']):
            img = main.decode_base64_to_img(encoded_image)
            filename = f'student_{student_id}_frame_{idx}.jpg'
            cv2.imwrite(os.path.join(os.getcwd(), config.LEARNING_FOLDER, filename), img)
            known_students, known_encodings = learning(config.LEARNING_FOLDER, mtcnn)
            return Response(response=None, status=200, headers={})

def learning(model, folder=config.LEARNING_FOLDER):
    known_encodings = []
    known_students = []
    # filename example 'student_{student_id}_frame_{idx}.jpg'
    for img_file in os.listdir(os.path.join(os.getcwd(), folder)):
        student_id = int(img_file.split('_')[1])
        student = db.db_session.query(models.Student).filter_by(id=student_id).first()
        img = face_recognition.load_image_file(img_file)
        bboxes, _ = model.detect(img)
        encodings = face_recognition.face_endocdings(img, bboxes)
        if len(encodings) == 1:
            known_students.append(student.first_name + '_' +  student.last_name)
            known_encodings.append(encodings[0])
    return known_students, known_encodings

known_students, known_encodings = learning(mtcnn, config.LEARNING_FOLDER)


