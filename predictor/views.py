from django.shortcuts import render

import joblib
import json
import pandas as pd
from django.shortcuts import render

model = joblib.load('disease_model.pkl')

with open('symptoms_list.json') as f:
    symptoms_list = json.load(f)

desc_df = pd.read_csv('symptom_Description.csv')
prec_df = pd.read_csv('symptom_precaution.csv')

def index(request):
    result = None
    description = None
    precautions = []

    if request.method == 'POST':
        selected = request.POST.getlist('symptoms')
        input_row = {col: 'none' for col in [f'Symptom_{i}' for i in range(1, 18)]}
        for i, s in enumerate(selected[:17]):
            input_row[f'Symptom_{i+1}'] = s

        input_df = pd.DataFrame([input_row])

        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        all_symptoms = symptoms_list + ['none']
        le.fit(all_symptoms)
        for col in input_df.columns:
            input_df[col] = le.transform(input_df[col])

        result = model.predict(input_df)[0]

        desc_row = desc_df[desc_df['Disease'] == result]
        if not desc_row.empty:
            description = desc_row.iloc[0]['Description']

        prec_row = prec_df[prec_df['Disease'] == result]
        if not prec_row.empty:
            precautions = [prec_row.iloc[0][f'Precaution_{i}'] for i in range(1, 5)]

    return render(request, 'predictor/index.html', {
        'symptoms_list': symptoms_list,
        'result': result,
        'description': description,
        'precautions': precautions
    })
    from django.core.mail import send_mail
from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        send_mail(  # pyright: ignore[reportUndefinedVariable]
            subject=f'MediTriage Message from {name}',
            message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
            from_email='sagarkumarj446@gmail.com',
            recipient_list=['sagarkumarj446@gmail.com'],
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})# Create your views here.
