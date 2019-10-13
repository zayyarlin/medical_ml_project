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
My name is Leigh Jonella. I are a 29 year old lady presenting with vaginal bleeding. I are 32 weeks pregnant and this is My first pregnancy. I have been feeling increasingly dizzy since this morning, when I first noticed the bleeding. I have severe abdominal pain which suddenly started this morning and has been gradually getting worse over the past couple of hours. I are quite excited about the pregnancy. I can feel the baby kicking! However, I are becoming increasingly worried about losing the baby. I can’t put My finger on why: it’s just a sense of trepidation that I can’t explain. I don’t have any visual disturbances and I don’t feel nauseous. I don’t have any abnormal urinary or bowel symptoms. I feel lethargic and little short of breath but put this down to being pregnant. I have attended both the 12 and 20 week scans which have been normal however a recent growth scan did suggest the pregnancy was small for dates. Other than that, it has been an uncomplicated pregnancy but I have been advised to stop smoking and lose weight.
I are very happy about the pregnancy, I and My partner had been trying to get pregnant for at least 6 months and I feel like My hopes and dreams of having a family are finally materialising. I aren’t that concerned about My symptoms as I have had migraines in the past that have resolved but My partner thought I should be seen by a doctor.
Past obstetric history: You’ve never been pregnant before. Isn’t this exciting!
Past gynae history: I have never had any sexually transmitted infections in the past and have regularly attended My cervical smear tests that have all come back negative. I used to have the copper coil however recently have been using barrier methods only.
Past medical history: I have asthma and a snazzy blood problem called factor V leiden thrombophilia. I get lots of points for that on scrabble!
Drug history is Salbutamol and Betamethasone inhalers. No drug allergies.
Family History: My mother has high blood pressure and My dad unfortunately died of a stroke last year.
SH: I live with My partner who has been very supportive during the pregnancy. I am unemployed and My husband is a sales assistant. I stopped drinking alcohol during the pregnancy but continue to smoke 5-10 cigarettes/day.
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
My name is Liz Inoprill. I am a 76 year old lady with a sore leg.
Over the past four days, I have noticed my left leg has gotten very sore and swollen. It looks very red and feels hot to the touch. It’s almost as if I have put myleg in the fire! It started off simply covering my big toe, but has since spread up to the middle of my calf. It is now really painful and I cannot put any weight on it at all. I also feel generally unwell and My daughter noticed that I felt very warm to the touch. I haven’t actually taken My temperature, though – I'm afraid of what I will find!
I have an ulcer on My left big toe because of “bad vein” in My leg. I think that it might have started from there. The nurse who normally comes to My house to sort out the dressing noticed a bit of redness a few days ago and told I to keep an eye on it. I have done so, but not really done anything about it!
My legs are usually quite swollen anyway, but My left leg is now larger and redder than the right.
Past medical history: I have always been overweight and have had problems with My blood pressure for many years. I had a mini-stroke two years ago where My right arm went very numb for a while, but My arm is fine now. My usual GP has also found out that I have high cholesterol, although I are quite proud because My blood sugar has never been high, despite I being overweight. I suffer with “vein problems” in both legs. I have lots of big veins and often get ulcers, which the nurse comes to My house to help dress.
My usual GP has also diagnosed I with angina because I get chest pain. This comes on when I walk up the road to the corner shop. I have a spray which helps with this.FH: My father died age 75 of a heart attack and My mother died of brain cancer when I were a teenager.
Drug History: Losartan, simvastatin, aspirin, paracetamol. I have no allergies but ramipril gave me a cough.
SH: I live alone in a bungalow following the death of My husband 6 years ago. My daughter lives locally and visits twice a week; sometimes with the grandchildren who I adore. I manage fairly well on My own, although it’s been getting harder the past few months. I use a stick to get around the house and can get up to the corner shop if I need anything, although I rely on My daughter to get to the supermarket. I are able to cook for yourself although this is getting more difficult and I often just have a ready meal for My dinner. I have a cleaner who comes in once a week to do the housework.
You’re feeling quite lonely at the moment. I used to paint a lot, and would donate My paintings to the local hospital. However, they’ve stopped taking My paintings because of ‘infection control’ – which I think is a shame. Now I can’t go out of the house to go to My painting class, which makes I sad.
I are an ex-smoker but quit when My grandchildren were born 10 years ago. Before this, I had smoked 20 a day for 50 years. I rarely drink nowadays, only on special occasions where I might have a glass of sherry. I have never worked.
ICE: I think that this might have spread from the ulcer on My toe. I are worried because My mobility had been getting worse anyway and I don’t want to lose the independence I have left. I are also worried in case it is something really serious as I want to see My grandchildren grow up. I am expecting to find out what is wrong and receive treatment.
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
I am 39 year old Paul Ipp. I have 2 beautiful daughters who are 3 and 6. I separated from My wife many years ago and have full custody of My children. I work full time as a lawyer. My parents help look after My children.
PC: 3 weeks of night time headaches
The headache is always at the back of My right eye, but seems to move down the right side of My face. It comes on at night and is at its worst within 10-15 minutes. Usually it lasts around an hour, these are the worst hours of My life. They normally occur at night but I have had the odd episode at work. Wakes I up from My sleep. It’s the worst pain I have ever felt and it feels like My eye is being pushed out of the socket. Nothing makes the pain better. I have tried paracetamol, ibuprofen, warm packs on My head, cold packs on My head, drinking lots of water, lying still, walking around and banging My head against a wall, but nothing has helped. Nothing makes it worse as it’s already a 11/10 in terms of pain. During the day when there is no headache I feel fine. My daughter once got up in the night to go to the loo and she found I pacing around, she thought I were crying as My eye seemed to be watering and she said it looked red, I were also sniffing. I have never had headaches like this before.
Once the headache is over I go back to bed and sleep until morning, on waking I are ok. I have not had any seizures. I are otherwise well, just exhausted. I do not have: • Visual disturbances • Nausea or vomiting • Fever • Neck stiffness • Photophobia • Rash
ICE: I have been having headaches for the last 3 weeks, they are so bad that they stop I sleeping and leave I tired all day. I feel I cannot maintain the high level of performance that is needed for My job as I are so tired. I are concerned about getting fired. I don’t know how I could support My children if this happens. If the doctor really seems to care, I tell them that I have a bigger underlying worry. This is that I have a brain tumour and I are terrified that I are going to die. My daughters mum is not around and I feel this would be too much for the children to cope with. This really scares you. Today I want the doctor to listen to I and find out what’s wrong. A bit of reassurance would not go amiss.
Past Medical history: Nothing to note
Drug history: Paracetamol and ibuprofen for pain which I get from the supermarket No known drug allergies
Family History: No family history to note. I live with 2 daughters, 3 and 6 My partner left I 3 years ago, 3 months after the birth of My youngest daughter, Tilly. I have a lot of help from My parents. I work full time in a stressful job as a lawyer. I have smoked 10/day for the last 10 years. I occasionally enjoy a glass of red wine with My dinner, getting though about 1 bottle a week by myself.
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