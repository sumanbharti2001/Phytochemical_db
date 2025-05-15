from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Function to clean and normalize column names
def clean_df(df_):
    df_.columns = df_.columns.str.strip()
    df_ = df_.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    # Standardize column names for consistent filtering
    rename_map = {
        'Species name': 'Species',
        'Species_name': 'Species',
        'Botanical Name': 'Species',
        'DOI number': 'DOI',
        'DOI_number': 'DOI'
    }
    df_.rename(columns=rename_map, inplace=True)
    return df_

# Load and prepare data
try:
    df1 = pd.read_csv('Demo data.csv', encoding='latin1')
    df2 = pd.read_csv('Demo data new.csv', encoding='latin1')

    df1 = clean_df(df1)
    df2 = clean_df(df2)

    df = pd.concat([df1, df2], ignore_index=True)
    df = clean_df(df)  # Clean again after concatenation
    print("Columns in final dataframe:", df.columns.tolist())

except Exception as e:
    print("Error loading CSVs:", e)
    df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    page = int(request.args.get('page', 1))
    per_page = 20

    compound = request.args.get('compound', '').strip()
    species = request.args.get('species', '').strip()
    country = request.args.get('country', '').strip()
    doi = request.args.get('doi', '').strip()

    filtered = df.copy()

    if compound and 'Compounds' in filtered.columns:
        filtered = filtered[filtered['Compounds'].str.contains(compound, case=False, na=False)]

    if species and 'Species' in filtered.columns:
        filtered = filtered[filtered['Species'].str.contains(species, case=False, na=False)]

    if country and 'Country' in filtered.columns:
        filtered = filtered[filtered['Country'].str.contains(country, case=False, na=False)]

    if doi and 'DOI' in filtered.columns:
        filtered = filtered[filtered['DOI'].str.contains(doi, case=False, na=False)]

    total = len(filtered)
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    paginated_data = filtered.iloc[start:end]

    table = paginated_data.to_html(classes='table table-striped table-bordered', index=False)

    return render_template(
        'search.html',
        table=table,
        start=start,
        end=end,
        total=total,
        page=page,
        compound=compound,
        species=species,
        country=country,
        doi=doi,
        countries=df['Country'].dropna().unique() if 'Country' in df.columns else []
    )

@app.route('/download', methods=['GET'])
def download():
    compound = request.args.get('compound', '').strip()
    species = request.args.get('species', '').strip()
    country = request.args.get('country', '').strip()
    doi = request.args.get('doi', '').strip()

    filtered = df.copy()

    if compound and 'Compounds' in filtered.columns:
        filtered = filtered[filtered['Compounds'].str.contains(compound, case=False, na=False)]

    if species and 'Species' in filtered.columns:
        filtered = filtered[filtered['Species'].str.contains(species, case=False, na=False)]

    if country and 'Country' in filtered.columns:
        filtered = filtered[filtered['Country'].str.contains(country, case=False, na=False)]

    if doi and 'DOI' in filtered.columns:
        filtered = filtered[filtered['DOI'].str.contains(doi, case=False, na=False)]

    csv_bytes = filtered.to_csv(index=False).encode('utf-8')
    buffer = BytesIO(csv_bytes)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='filtered_data.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

