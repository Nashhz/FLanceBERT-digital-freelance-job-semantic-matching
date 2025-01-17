from flask import Flask, render_template, request, redirect, url_for 
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import cx_Oracle
import numpy as np

from backend.oracleconnection import fetch_job_descriptions, create_matched_jobs_table
from backend.SBERT_load import load_sbert_model
from backend.job_matching import match_jobs
from backend.matched_jobs import save_matched_jobs  # Existing save logic


app = Flask(__name__)

@app.route("/")
@app.route('/index')
def page1():
    return render_template('index.html')

@app.route('/dashboard')
def page2():
    return render_template('dashboard.html')

@app.route('/portfolio', methods=['GET', 'POST'])  # Allow both GET and POST
def page3():
    if request.method == 'POST':
        content = request.form.get('portfolioContent')  # Get the content from the form
        # Redirect to the job matching route with the portfolio content
        return redirect(url_for('page4', portfolioContent=content))  # Redirect to /jobmatching with the content
    return render_template('portfolio.html')  # Handle GET request

@app.route('/jobmatching', methods=['GET', 'POST'])
def page4():
    matched_jobs = []  # Initialize an empty list for matched jobs

    if request.method == 'POST' or 'portfolioContent' in request.args:
        # Get the portfolio description and user ID
        portfolio_description = request.form.get('portfolioContent') or request.args.get('portfolioContent')
        #user_id = request.form.get('userID') or request.args.get('userID')  # Assume user ID is passed

        #if not user_id:
        #    return "User ID is required to save matched jobs."

        # Load the SBERT model
        model = load_sbert_model()

        # Fetch job descriptions from the database
        df = fetch_job_descriptions()

        # Match jobs using the portfolio description
        job_descriptions = df['DESCRIPTION'].astype(str).tolist()
        top_results = match_jobs(portfolio_description, job_descriptions, model, top_k=20)

        # Prepare the output for rendering
        for score, idx in zip(top_results[0], top_results[1]):
            matched_jobs.append({
                'id': df['ID'][int(idx)],
                'title': df['TITLE'][int(idx)],
                'description': job_descriptions[int(idx)],
                'time_submitted': df['TIME_SUBMITTED'][int(idx)],
                'currency': df['CURRENCY'][int(idx)],
                'budget': df['BUDGET'][int(idx)],
                'status': df['STATUS'][int(idx)],
                'posted_date': df['POSTED_DATE'][int(idx)].strftime('%Y-%m-%d'),
                'similarity_score': score.item()
            })

        # Save matched jobs into the user's table
        #save_message = save_matched_jobs(user_id, matched_jobs)
        #print(save_message)

    return render_template('jobmatching.html', matched_jobs=matched_jobs)

@app.route('/profit')
def page5():
    return render_template('profit.html')

@app.route('/calendar')
def page6():
    return render_template('calendar.html')

@app.route('/playground')
def page7():
    return render_template('playground.html')

if __name__ == '__main__':
    app.run(debug=True)