from flask import Flask, render_template, request
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import cx_Oracle

app = Flask(__name__)

# Load the fine-tuned SBERT model
model = SentenceTransformer('Nashhz/SBERT_KFOLD_User_Portfolio_to_Job_Descriptions')

@app.route("/")
@app.route('/index')
def page1():
    return render_template('index.html')

@app.route('/dashboard')
def page2():
    return render_template('dashboard.html')

@app.route('/portfolio', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        portfolio_description = request.form.get('portfolioContent')  # Get the content from the form
        
        # Connect to the Oracle database and load job descriptions
        try:
            dsn = cx_Oracle.makedsn('localhost', 1521, service_name='XE')
            connection = cx_Oracle.connect(user='FYP_01', password='system', dsn=dsn)

            with connection.cursor() as cursor:
                query = "SELECT id, title, description FROM projects"
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                df = pd.DataFrame(rows, columns=columns)

                # Convert LOBs to strings
                df['DESCRIPTION'] = df['DESCRIPTION'].apply(lambda x: x.read() if hasattr(x, 'read') else str(x))

            connection.close()
        except Exception as e:
            return f"Error loading data from Oracle database: {e}"

        # Encode job descriptions
        job_descriptions = df['description'].astype(str).tolist()
        job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

        # Encode the portfolio description
        portfolio_embedding = model.encode(portfolio_description, convert_to_tensor=True)

        # Compute cosine similarity scores
        similarity_scores = util.pytorch_cos_sim(portfolio_embedding, job_embeddings)

        # Sort job descriptions by similarity score
        top_results = similarity_scores[0].topk(6)  # Get top 6 results

        # Prepare the output for rendering
        matched_jobs = []
        for score, idx in zip(top_results[0], top_results[1]):
            matched_jobs.append({
                'id': df['id'][idx],
                'title': df['title'][idx],
                'description': job_descriptions[idx],
                'similarity_score': score.item()
            })

        return render_template('portfolio.html', matched_jobs=matched_jobs, portfolio_description=portfolio_description)

    return render_template('portfolio.html')  # Handle GET request

@app.route('/jobmatching')
def page4():
    return render_template('jobmatching.html')

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