from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import os
import csv

app = Flask(__name__,template_folder='templates')
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Path to your CSV file
csv_file_path = 'sample_data .csv'
df = pd.read_csv(csv_file_path, encoding='latin1')
# Load or initialize the DataFrame (improved)


def search_material(data, material_name):
  """
  Searches for a material name in a pandas DataFrame and returns all other columns' data for that material.

  Args:
      data: A pandas DataFrame containing material data.
      material_name (str): The name of the material to search for.

  Returns:
      pandas.DataFrame: A DataFrame containing all other columns' data for the searched material,
                         or an empty DataFrame if the material is not found.
  """

  filtered_data = data[data['material_name'] == material_name]

  if not filtered_data.empty:
    return filtered_data.drop('material_name', axis=1)
  else:
    return pd.DataFrame(columns=data.columns[1:])

@app.route('/')
def home():
    return render_template('index.html', tables=[df.to_html(classes='data', header="true")])

@app.route('/new')
def show_new_page():
    return render_template('new.html')

@app.route('/predict')
def show_new():
    return render_template('predit.html')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    try:
        material_name = request.form['material_name']
        material_type = request.form['material_type']
        thickness = request.form['thickness']
        density = request.form['density']
        flammability_rating = request.form['flammability_rating']
        ignition_temp = request.form['ignition_temp']
        burn_time = request.form['burn_time']
        heat_release_rate = request.form['heat_release_rate']
        smoke_production = request.form['smoke_production']
        toxicity = request.form['toxicity']
        regulations = request.form['regulations']
        use_case = request.form['use_case']
        manufacturer = request.form['manufacturer']
        flammability_class = request.form['flammability_class']
        pass_fail = request.form['pass_fail']

        # Append the new entry to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([material_name, material_type, thickness, density, flammability_rating, ignition_temp, burn_time, heat_release_rate, smoke_production, toxicity, regulations, use_case, manufacturer, flammability_class, pass_fail])

        return redirect('/')
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            # Access the material_name from the form data
            material_name = request.form['material_name']
            print(f"Searching for material: {material_name}")  # Debug statement
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)
            
            # Search for the material name
            search_results = df[df['Material Name'].str.contains(material_name, case=False, na=False)]
            
            # Render the template with the search results
            return render_template('search.html', search_results=search_results)
        except KeyError:
            return "Error: 'material_name' not found in form data."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template('search.html')

if __name__ == '__main__':
  df = pd.read_csv(csv_file_path, encoding='latin1')  # Load DataFrame
  app.run(debug=True)

  # Call add_entry with the DataFrame as an argument
  add_entry(df) 
