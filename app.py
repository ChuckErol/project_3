import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from flask import Flask, jsonify
from flask_cors import CORS
import geopandas as gpd

# Connect to database
database_path = Path("data.sqlite")
engine = create_engine(f"sqlite:///{database_path}")

#################################################
# Get GeoJSON data for state and county boundaries
#################################################
states = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_state_500k.zip")
counties = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_county_500k.zip")

# Keep only main states data
states = states[states["GEOID"].astype(int) <= 56]
counties = counties[counties["STATEFP"].astype(int) <= 56]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        '<a href="/api/v1.0/get_states">/api/v1.0/get_states</a> - return list of states<br/>'
        '<a href="/api/v1.0/get_industries">/api/v1.0/get_industries</a> - return list of industries<br/>'
        '<a href="/api/v1.0/get_employment_map/US/1011/15">'
        '/api/v1.0/get_employment_map/&lt;string:state_code&gt;/&lt;int:industry_code&gt;/&lt;int:reduction&gt;</a> - return employment map<br/>'
        '<a href="/api/v1.0/get_employment_trend/US/1011/15">'
        '/api/v1.0/get_employment_trend/&lt;string:state_code&gt;/&lt;int:industry_code&gt;/&lt;int:reduction&gt;</a> - return employment trend<br/>'
        '<a href="/api/v1.0/get_unemployment_rate/US/1011/15">'
        '/api/v1.0/get_unemployment_rate/&lt;string:state_code&gt;/&lt;int:industry_code&gt;/&lt;int:reduction&gt;</a> - return unemployment rate<br/>'
        '<a href="/api/v1.0/get_income_map/US/1011/15">'
        '/api/v1.0/get_income_map/&lt;string:state_code&gt;/&lt;int:industry_code&gt;/&lt;int:reduction&gt;</a> - return income map<br/>'
    )

@app.route("/api/v1.0/get_states")
def get_states():
    select_statement = """
    SELECT state_code,
           state_name
    FROM state
    """
    
    with engine.connect() as connection:
        query = text(select_statement)
        result = connection.execute(query)
        columns = result.keys()
        result_list = [dict(zip(columns, row)) for row in result]
    
    return jsonify(result_list)

@app.route("/api/v1.0/get_industries")
def get_industries():
    select_statement = """
    SELECT industry_code,
           industry_name
    FROM industry
    """
    
    with engine.connect() as connection:
        query = text(select_statement)
        result = connection.execute(query)
        columns = result.keys()
        result_list = [dict(zip(columns, row)) for row in result]
    
    return jsonify(result_list)


@app.route("/api/v1.0/get_employment_map/<string:state_code>/<int:industry_code>/<int:reduction>")
def get_employment_map(state_code, industry_code, reduction):
    select_statement = ""

    if state_code == "US":
        select_statement = f"""
        WITH 
        industry_employment 
        AS
        (
            SELECT c.state_code, 
                    SUM(bls_annual_employment) AS industry_employment
                FROM county_industry_metric cim
                        INNER JOIN
                        county c ON c.county_fips = cim.county_fips
                WHERE industry_code = {industry_code}
                    AND year = (SELECT MAX(year) FROM county_industry_metric)
            GROUP BY c.state_code
        ),
        state_employment 
        AS
        (
            SELECT c.state_code, 
                    SUM(bls_annual_employment) AS total_employment
                FROM county_industry_metric cim
                        INNER JOIN
                        county c ON c.county_fips = cim.county_fips
                WHERE year = (SELECT MAX(year) FROM county_industry_metric)
            GROUP BY c.state_code
        )
        SELECT se.state_code,
                se.total_employment,
                ie.industry_employment
            FROM state_employment se
                    INNER JOIN
                    industry_employment ie ON ie.state_code = se.state_code
        """
    else:
        select_statement = f"""
        WITH 
        industry_employment
        AS
        (
            SELECT c.county_name,
                    c.state_code,
                    bls_annual_employment AS industry_employment
                FROM county_industry_metric cim
                        INNER JOIN
                        county c ON c.county_fips = cim.county_fips
                WHERE industry_code = {industry_code}
                    AND year = (SELECT MAX(year) FROM county_industry_metric)
                    AND state_code = '{state_code}'
        ),
        county_employment
        AS
        (
            SELECT c.county_name,
                    c.state_code,
                    SUM(bls_annual_employment) AS total_employment
                FROM county_industry_metric cim
                        INNER JOIN
                        county c ON c.county_fips = cim.county_fips
                WHERE year = (SELECT MAX(year) FROM county_industry_metric)
                    AND state_code = '{state_code}'
            GROUP BY c.county_name, c.state_code
        )
        SELECT ce.county_name,
                ce.state_code,
                ce.total_employment,
                ie.industry_employment
            FROM county_employment ce
                    INNER JOIN
                    industry_employment ie ON ie.county_name = ce.county_name
        """

    # Execute the query
    with engine.connect() as connection:
        query = text(select_statement)
        result = connection.execute(query)
        columns = result.keys()
        result_list = [dict(zip(columns, row)) for row in result]

    # Convert result to DataFrame 
    df = pd.DataFrame(result_list)

    # Check if the DataFrame contains the necessary columns after merging
    if "industry_employment" not in df.columns:
        return jsonify({"error": "industry_employment column not found in the DataFrame."}), 500

    # Calculate current share of industry by employment
    df["current_industry_share"] = 100 * df["industry_employment"] / df["total_employment"]

    # Calculate reduced share of industry by employment
    reduction_rate = (100 - reduction) / 100
    df["reduced_industry_share"] = 100 * (reduction_rate * df["industry_employment"]) / (df["total_employment"] - ((reduction / 100) * df["industry_employment"]))

    # Adding geo data
    if state_code == "US":
        # Create a copy of states GeoPandas DataFrame
        geoPandas = states.copy()

        # Merge states geoJSON with a metric
        geoPandas = geoPandas.merge(df, how="inner", left_on="STUSPS", right_on="state_code")

        # Drop unnecessary column
        geoPandas.drop(columns="state_code", inplace=True)
    else:
        # Create a copy of counties GeoPandas DataFrame
        geoPandas = counties.copy()

        # Merge counties geoJSON with a metric
        geoPandas = geoPandas.merge(df, how="inner", left_on=["STUSPS", "NAME"], right_on=["state_code", "county_name"])

        # Drop unnecessary column
        geoPandas.drop(columns=["state_code", "county_name"], inplace=True)

    # Convert results to GeoJSON
    return geoPandas.to_json()

# Example call to the function
#geojson_result = get_employment_map(state_code="US", industry_code=1011, reduction=15)
#print(geojson_result)

@app.route("/api/v1.0/get_employment_trend/<string:state_code>/<int:industry_code>/<int:reduction>")
def get_employment_trend_api(state_code, industry_code, reduction):
    try:
        # Call the function to get employment trend
        employment_trend_data = get_employment_trend(state_code, industry_code, reduction)
        return jsonify(employment_trend_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_employment_trend(state_code, industry_code, reduction):
    # Check the area level
    if state_code == "US":
        select_statement = f"""
        SELECT year,
               SUM(bls_annual_employment) AS metric
            FROM 
                county_industry_metric
            WHERE industry_code = {industry_code}
        GROUP BY year
        """
    else:
        select_statement = f"""
        SELECT m.year,
               SUM(bls_annual_employment) AS metric
            FROM 
                county_industry_metric m
            JOIN
                county c 
            ON 
                c.county_fips = m.county_fips
            WHERE c.state_code = '{state_code}'
              AND industry_code = {industry_code}
        GROUP BY m.year
        """

    # Execute the query
    with engine.connect() as connection:
        query = text(select_statement) 
        result = connection.execute(query)
        
        # Convert result to a list of dictionaries
        result_list = [{'year': row[0], 'metric': row[1]} for row in result]

    # Get employment from the latest year
    latest_employment = result_list[-1]["metric"]

    # Calculate forecasted employment based on the latest employment and reduction
    employment2030 = latest_employment * (100 - reduction) / 100

    # Append the forecasted employment to the result
    result_list.append({'year': 2030, 'metric': employment2030})

    return result_list

# Example call to the function
#result = get_employment_trend_api(state_code="US", industry_code=1011, reduction=15)
#print(result)


# Helper function to calculate unemployment rate
def get_unemployment_rate(state_code, industry_code, reduction):
    def check_area_name_presence(df1, df2):
        return 'area_name' in df1.columns and 'area_name' in df2.columns

    if state_code == "US":
        select_industry_employment = f"""
        SELECT s.state_name AS area_name,
               SUM(bls_annual_employment) AS industry_employment
        FROM county_industry_metric cim
        JOIN county c ON c.county_fips = cim.county_fips
        JOIN state s ON s.state_code = c.state_code
        WHERE industry_code = {industry_code}
          AND year = 2022
        GROUP BY s.state_name
        """
        
        select_state_employment = f"""
        SELECT s.state_name AS area_name,
               SUM(bls_labor_force) AS labor_force,
               SUM(bls_employed) AS employment
        FROM county_metric m
        JOIN county c ON c.county_fips = m.county_fips
        JOIN state s ON s.state_code = c.state_code
        WHERE m.year = 2022
        GROUP BY s.state_name
        """
    else:
        select_industry_employment = f"""
        SELECT c.county_name AS area_name,
               bls_annual_employment AS industry_employment
        FROM county_industry_metric cim
        JOIN county c ON c.county_fips = cim.county_fips
        WHERE industry_code = {industry_code}
          AND year = 2022
          AND state_code = '{state_code}'
        """

        select_county_employment = f"""
        SELECT c.county_name AS area_name,
               bls_labor_force AS labor_force,
               bls_employed AS employment
        FROM county_metric m
        JOIN county c ON c.county_fips = m.county_fips
        WHERE m.year = 2022
          AND state_code = '{state_code}'
        """

    with engine.connect() as connection:
        query = text(select_industry_employment)
        result = connection.execute(query)
        result_list_industry_employment = [{'area_name': row[0], 'industry_employment': row[1]} for row in result]
        df_industry_employment = pd.DataFrame(result_list_industry_employment)
        
        query = text(select_state_employment if state_code == "US" else select_county_employment)
        result = connection.execute(query)
        result_list_state_employment = [{'area_name': row[0], 'labor_force': row[1], 'employment': row[2]} for row in result]
        df_state_employment = pd.DataFrame(result_list_state_employment)

    if not check_area_name_presence(df_industry_employment, df_state_employment):
        raise ValueError("area_name not found in both DataFrames")

    df = pd.merge(df_industry_employment, df_state_employment, how="inner", on="area_name")

    df["unemployment_rate"] = 100 * (df["labor_force"] - df["employment"]) / df["labor_force"]
    df["average_unemployment_rate"] = 100 * (df["labor_force"].sum() - df["employment"].sum()) / df["labor_force"].sum()
    df["forecasted_unemployment_rate"] = 100 * (df["labor_force"] - (df["employment"] - (reduction / 100) * df["industry_employment"])) / df["labor_force"]

    #df["unemployment_rate"] = df["unemployment_rate"].apply(lambda x: f"{x:.2f}%")
    #df["average_unemployment_rate"] = f"{df['average_unemployment_rate'].iloc[0]:.2f}%"
    #df["forecasted_unemployment_rate"] = df["forecasted_unemployment_rate"].apply(lambda x: f"{x:.2f}%")

    return df.to_dict('records')

# API endpoint
#@app.route("/api/v1.0/get_unemployment_rate/<string:state_code>/<int:industry_code>", methods=["GET"])
@app.route("/api/v1.0/get_unemployment_rate/<string:state_code>/<int:industry_code>/<int:reduction>")
def api_get_unemployment_rate(state_code, industry_code, reduction):
    #reduction = request.args.get("reduction", default=0, type=int)
    
    try:
        unemployment_data = get_unemployment_rate(state_code, industry_code, reduction)
        return unemployment_data #jsonify(unemployment_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Example call to the function
#result = api_get_unemployment_rate(state_code="US", industry_code=1011, reduction=15)
#print(result)

@app.route("/api/v1.0/get_income_map/<string:state_code>/<int:industry_code>/<int:reduction>")
def get_income_map(state_code, industry_code, reduction):
    # Check the area level
    if state_code == "US":
        select_statement = f"""
        WITH 
        industry_income
        AS
        (
            SELECT c.state_code,
                   SUM(bls_total_annual_wages) AS industry_wage,
                   SUM(bls_annual_employment) AS industry_employment
                FROM county_industry_metric cim
                     INNER JOIN
                     county c ON c.county_fips = cim.county_fips
                WHERE industry_code = {industry_code}
                  AND year = (SELECT MAX(year) FROM county_industry_metric)
            GROUP BY c.state_code
        ),
        state_income
        AS
        (
            SELECT c.state_code,
                   SUM(bea_total_income) AS total_income,
                   SUM(population) AS population
                FROM county_metric m
                     INNER JOIN
                     county c ON c.county_fips = m.county_fips
                WHERE m.year = (SELECT MAX(year) FROM county_metric)
            GROUP BY c.state_code
        )
        SELECT si.state_code,
               si.total_income,
               si.population,
               ii.industry_wage,
               ii.industry_employment
            FROM state_income si
                 INNER JOIN
                 industry_income ii ON ii.state_code = si.state_code
        """
    else:
        select_statement = f"""
        WITH 
        industry_income
        AS
        (
            SELECT c.county_name,
                   c.state_code,
                   bls_total_annual_wages AS industry_wage,
                   bls_annual_employment AS industry_employment
                FROM county_industry_metric cim
                     INNER JOIN
                     county c ON c.county_fips = cim.county_fips
                WHERE industry_code = {industry_code}
                  AND year = (SELECT MAX(year) FROM county_metric)
                  AND state_code = '{state_code}'
        ),
        county_income
        AS
        (
            SELECT c.county_name,
                   c.state_code,
                   bea_total_income AS total_income,
                   population
                FROM county_metric m
                     INNER JOIN
                     county c ON c.county_fips = m.county_fips
                WHERE m.year = (SELECT MAX(year) FROM county_metric)
                  AND state_code = '{state_code}'
        )
        SELECT ci.county_name,
               ci.state_code,
               ci.total_income,
               ci.population,
               ii.industry_wage,
               ii.industry_employment
            FROM county_income ci
                 INNER JOIN
                 industry_income ii ON ii.county_name = ci.county_name
        """

    # print(select_statement)

    # Execute the query
    with engine.connect() as connection:

        query = text(select_statement) 
        result = connection.execute(query)
        
        # Convert result to a list of dictionaries
        result_list = [dict(row) for row in result]

    # Convert result to DataFrame to simplify calculations
    df = pd.DataFrame(result_list)

    # Calculate current per capita income
    df["per_capita_income"] = df["total_income"] / df["population"]

    # Calculate current per capita industry wage
    df["per_capita_industry_wage"] = df["industry_wage"] / df["industry_employment"]

    # Calculate total reduced income
    df["total_reduced_income"] = df["total_income"] - (reduction / 100) * df["industry_wage"]

    # Calculate per capita reduced income
    df["per_capita_reduced_income"] = df["total_reduced_income"] / df["population"]

    # Calculate change in per capita income
    df["change_in_per_capita_income"] = 100 * (df["per_capita_reduced_income"] - df["per_capita_income"]) / df["per_capita_income"]

    # Adding geo data
    # Depending of the area selection (national or a particular state), creating geoPandas DataFrame
    if state_code == "US":
        # Create a copy of states GeoPandas DataFrame
        geoPandas = states.copy()

        # Merge states geoJSON with a metric
        geoPandas = geoPandas.merge(df, how="inner", left_on="STUSPS", right_on="state_code")

        # Drop unnecessary column
        geoPandas.drop(columns="state_code", inplace=True)
    else:
        # Create a copy of states GeoPandas DataFrame
        geoPandas = counties.copy()

        # Merge states geoJSON with a metric
        geoPandas = geoPandas.merge(df, how="inner", left_on=["STUSPS", "NAME"], right_on=["state_code", "county_name"])

        # Drop unnecessary columns
        geoPandas.drop(columns=["state_code", "county_name"], inplace=True)

    # Convert result to GeoJSON
    return geoPandas.to_json()


#################################################
# Run Flask
#################################################
if __name__ == '__main__':
    app.run(debug=True)