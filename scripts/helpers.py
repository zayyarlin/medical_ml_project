# -*- coding: utf-8 -*-

from scripts import tabledef
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt

class Patient():
    def __init__(self, id, name, case_type, case, intro, gender, free=False):
        self.id = id
        self.name = name
        self.case_type = case_type
        self.case = case
        self.intro = intro
        self.gender = gender
        self.free = free

name1 = "Leigh Jonella"
case_type1 = "Obstetrics"
case1 = """
HPC: You are Leigh Jonella, a 29 year old lady presenting with vaginal bleeding. You are 32 weeks pregnant and this is your first pregnancy. You have been feeling increasingly dizzy since this morning, when you first noticed the bleeding. You have severe abdominal pain which suddenly started this morning and has been gradually getting worse over the past couple of hours. You are quite excited about the pregnancy. You can feel the baby kicking! However, you are becoming increasingly worried about losing the baby. You can’t put your finger on why: it’s just a sense of trepidation that you can’t explain. You don’t have any visual disturbances and you don’t feel nauseous. You don’t have any abnormal urinary or bowel symptoms. You feel lethargic and little short of breath but put this down to being pregnant. You have attended both the 12 and 20 week scans which have been normal however a recent growth scan did suggest the pregnancy was small for dates. Other than that, it has been an uncomplicated pregnancy but you have been advised to stop smoking and lose weight.
ICE: You are very happy about the pregnancy, you and your partner had been trying to get pregnant for at least 6 months and you feel like your hopes and dreams of having a family are finally materialising. You aren’t that concerned about your symptoms as you have had migraines in the past that have resolved but your partner thought you should be seen by a doctor.
Past obstetric history: You’ve never been pregnant before. Isn’t this exciting!
Past gynae history: You have never had any sexually transmitted infections in the past and have regularly attended your cervical smear tests that have all come back negative. You used to have the copper coil however recently have been using barrier methods only.
PMH: You have asthma and a snazzy blood problem called factor V leiden thrombophilia. You get lots of points for that on scrabble!
DH: Salbutamol and Betamethasone inhalers. No drug allergies.
FH: Your mother has high blood pressure and your dad unfortunately died of a stroke last year.
SH: You live with your partner who has been very supportive during the pregnancy. You are unemployed and your husband is a sales assistant. You stopped drinking alcohol during the pregnancy but continue to smoke 5-10 cigarettes/day.
"""
intro1 = """
You are an FY1 doctor working in the obstetric and gynaecology department. Leigh Jonella is a 29 year old lady who has presented with a problem with her pregnancy. This is her first pregnancy, and therefore she is quite worried about this presentation.
Please take an obstetric history and explore Leigh’s concerns about this presentation. You will be asked to perform the appropriate examination and discuss the case with the examiner.
"""
gender1 = "F"
patient1 = Patient(123, name1, case_type1, case1,  intro1, gender1, free=True)

name2 = "Liz Inoprill"
case_type2 = "Infectious Diseases"
case2 = """
You are Liz Inoprill, a 76 year old lady with a sore leg.
HPC: Over the past four days, you have noticed your left leg has gotten very sore and swollen. It looks very red and feels hot to the touch. It’s almost as if you have put your leg in the fire! It started off simply covering your big toe, but has since spread up to the middle of your calf. It is now really painful and you cannot put any weight on it at all. You also feel generally unwell and your daughter noticed that you felt very warm to the touch. You haven’t actually taken your temperature, though – you’re afraid of what you will find!
You have an ulcer on your left big toe because of “bad vein” in your leg. You think that it might have started from there. The nurse who normally comes to your house to sort out the dressing noticed a bit of redness a few days ago and told you to keep an eye on it. You have done so, but not really done anything about it!
Your legs are usually quite swollen anyway, but your left leg is now larger and redder than the right.
PMH: You have always been overweight and have had problems with your blood pressure for many years. You had a mini-stroke two years ago where your right arm went very numb for a while, but your arm is fine now. Your usual GP has also found out that you have high cholesterol, although you are quite proud because your blood sugar has never been high, despite you being overweight. You suffer with “vein problems” in both legs. You have lots of big veins and often get ulcers, which the nurse comes to your house to help dress.
Your usual GP has also diagnosed you with angina because you get chest pain. This comes on when you walk up the road to the corner shop. You have a spray which helps with this.FH: Your father died age 75 of a heart attack and your mother died of brain cancer when you were a teenager.
DH: Losartan, simvastatin, aspirin, paracetamol. You have no allergies but ramipril gave you a cough.
SH: You live alone in a bungalow following the death of your husband 6 years ago. Your daughter lives locally and visits twice a week; sometimes with the grandchildren who you adore. You manage fairly well on your own, although it’s been getting harder the past few months. You use a stick to get around the house and can get up to the corner shop if you need anything, although you rely on your daughter to get to the supermarket. You are able to cook for yourself although this is getting more difficult and you often just have a ready meal for your dinner. You have a cleaner who comes in once a week to do the housework.
You’re feeling quite lonely at the moment. You used to paint a lot, and would donate your paintings to the local hospital. However, they’ve stopped taking your paintings because of ‘infection control’ – which you think is a shame. Now you can’t go out of the house to go to your painting class, which makes you sad.
You are an ex-smoker but quit when your grandchildren were born 10 years ago. Before this, you had smoked 20 a day for 50 years. You rarely drink nowadays, only on special occasions where you might have a glass of sherry. You have never worked.
ICE: You think that this might have spread from the ulcer on your toe. You are worried because your mobility had been getting worse anyway and you don’t want to lose the independence you have left. You are also worried in case it is something really serious as you want to see your grandchildren grow up. You are expecting to find out what is wrong and receive treatment.
"""
intro2 = """
You are a Foundation doctor undertaking a taster week in General Practice. Your first patient is Liz Inoprill, a 76 year old lady who has come in to see you about a sore leg. You can see from your GP records system that her medications include losartan, simvastatin, aspirin and GTN spray.
Please take a history from Liz, focusing on her history of presenting complaint. Undertake the appropriate examination and consider your differential diagnosis. You will then be asked to discuss the acute management of this presentation.
"""
gender2 = "F"
patient2 = Patient(456, name2, case_type2, case2,  intro2, gender2)

name3 = "Paul Ipp"
case_type3 = "Neurology"
case3 = """
You are 36 year old Paul Ipp. You have 2 beautiful daughters who are 3 and 6. You separated from your wife many years ago and have full custody of your children. You work full time as a lawyer. Your parents help look after your children.
PC: 3 weeks of night time headaches
HPC: The headache is always at the back of your right eye, but seems to move down the right side of your face. It comes on at night and is at its worst within 10-15 minutes. Usually it lasts around an hour, these are the worst hours of your life. They normally occur at night but you have had the odd episode at work. Wakes you up from your sleep. It’s the worst pain you have ever felt and it feels like your eye is being pushed out of the socket. Nothing makes the pain better. You have tried paracetamol, ibuprofen, warm packs on your head, cold packs on your head, drinking lots of water, lying still, walking around and banging your head against a wall, but nothing has helped. Nothing makes it worse as it’s already a 11/10 in terms of pain. During the day when there is no headache you feel fine. Your daughter once got up in the night to go to the loo and she found you pacing around, she thought you were crying as your eye seemed to be watering and she said it looked red, you were also sniffing. You have never had headaches like this before.
Once the headache is over you go back to bed and sleep until morning, on waking you are ok. You have not had any seizures. You are otherwise well, just exhausted. You do not have: • Visual disturbances • Nausea or vomiting • Fever • Neck stiffness • Photophobia • Rash
ICE: You have been having headaches for the last 3 weeks, they are so bad that they stop you sleeping and leave you tired all day. You feel you cannot maintain the high level of performance that is needed for your job as you are so tired. You are concerned about getting fired. You don’t know how you could support your children if this happens. If the doctor really seems to care, you tell them that you have a bigger underlying worry. This is that you have a brain tumour and you are terrified that you are going to die. Your daughters mum is not around and you feel this would be too much for the children to cope with. This really scares you. Today you want the doctor to listen to you and find out what’s wrong. A bit of reassurance would not go amiss.
PMH: Nothing to note
DH: Paracetamol and ibuprofen for pain which you get from the supermarket No known drug allergies
FH: No family history to note
SH: You live with 2 daughters, 3 and 6 Your partner left you 3 years ago, 3 months after the birth of your youngest daughter, Tilly You have a lot of help from your parents You work full time in a stressful job as a lawyer. You have smoked 10/day for the last 10 years You occasionally enjoy a glass of red wine with your dinner, getting though about 1 bottle a week by yourself
"""
intro3 = """
You are an FY1 doing a placement in a GP surgery. Mr Paul Ipp is a 39-year-old gentleman who has presented to your surgery with headaches. He is otherwise well and does not take any regular medications. This is his first such presentation and he is extremely concerned as this condition is severely impacting on his daily life.
Please take a history and perform the examination you feel is appropriate. Ensure that you address his concerns regarding this presentation.
"""
gender3 = "M"
patient3 = Patient(789, name3, case_type3, case3,  intro3, gender3)

patients = [patient1, patient2, patient3]

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    return sessionmaker(bind=tabledef.engine)()


def get_user():
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        return user


def add_user(username, password, email):
    with session_scope() as s:
        u = tabledef.User(username=username, password=password.decode('utf8'), email=email)
        s.add(u)
        s.commit()


def change_user(**kwargs):
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        for arg, val in kwargs.items():
            if val != "":
                setattr(user, arg, val)
        s.commit()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False

def credentials_valid_paid(username, password):
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')) and user.paid
        else:
            return False

def username_taken(username):
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()

def get_patients():
    return patients

def get_patient(patient_id):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    return None