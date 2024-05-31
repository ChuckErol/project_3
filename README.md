# Labor-Market-Trends-Analyzer

+ *Group Members*: Amit Suresh, Chuck Erol, Harleen Kang, Natalia Shevchenko, Nelson Lin, Tico Brown

## Overview of the Project and its Purpose

+ Artificial intelligence (AI) could replace up to 300 million full-time jobs, particularly affecting white-collar workers and manufacturing employees, according to various reports. Goldman Sachs predicts AI could automate a quarter of work tasks in the US and Europe, boosting global economic productivity by 7%. Researchers from the University of Pennsylvania and OpenAI highlight that educated workers earning up to $80,000 annually are most at risk. By 2025, MIT and Boston University estimate AI will replace two million manufacturing jobs, and the World Economic Forum anticipates AI will replace 85 million jobs, with 65% of retail jobs potentially automated. McKinsey Global Institute reports that by 2030, 14% of employees worldwide may need to change careers due to AI and related technological advancements.

+ With the emergence of AI technology, our team believes that a web application exploring the potential impact of AI on various industries is essential. This application will focus on the following questions:
    + Changes in industry employment over population with respect to state, industry, and reduction rate.
    + Changes in income with respect to state, industry, and reduction rate.
    + Changes in industry employment trends over time with respect to state, industry, and reduction rate.
    + Areas (states/counties) with total unemployment with respect to state, industry, and reduction rate.

+ This web application aims to provide a comprehensive analysis of the potential impact of AI on employment across different industries and regions, helping stakeholders to better understand and prepare for the future job market.

[See more details about the project in the presentation](https://docs.google.com/presentation/d/1PB3I37HJ30viPCbzTPQ8OWInUR1JcpulpccwwwgVWkQ/edit#slide=id.p)


## Instructions to Utilize and Interact with the Project

+ The "Labor Market Trends Analyzer" project consists of a database, a query system, a Flask application, and an interactive maps and charts for end users. To use the project, users start the Flask application to initiate the web application. See Installation section below for more details.
 
+ Once activated, users interact with three dropdown menus: Area (selecting an individual state or all states in the USA), Industry (selecting different job sectors), and Reduction (indicating job percentage replaced by AI). The inputs from these menus generate the following outputs: 

  + a map showing the change in employment (reduced industry share by employment with tooltips displaying also the current industry share)
  + a map showing changes in per capita income (tooltips are also displaying the current and reduced per capita income and the average industry wage)
  + a line chart forecasting the number of employees in 2030 at the national or state level
  + a bar chart highlighting areas with the highest unemployment after changes, displaying current, forecasted, and average unemployment rates 
   
Data is presented for 2020-2022, not all federal agencies can provide required data for 2023, that is why the application uses 2022 as the most recent year for the analysis.

+ Below is an example of the Web Application

![Alt text](Images/Sample%20Output.png)

## Ethical Considerations made in the Project

+ Fairness and Impartiality
    + Avoiding Bias: It is crucial to ensure that the data and algorithms used in the project do not introduce or perpetuate biases against certain groups. This includes racial, gender, age, and socioeconomic biases.
    + Inclusive Data Sources: Data should be collected from diverse and representative sources to avoid skewed results. Ensuring data diversity helps in creating more equitable predictions.
    + Algorithm Transparency: The algorithms used should be transparent and auditable. This allows stakeholders to understand how decisions are made and ensures accountability.

+ Clear Understandable Metrics
    + Transparency: Metrics used in the analysis should be clearly defined and easy to understand for all users, regardless of their technical background. This includes explaining how metrics like employment reduction rate and income changes are calculated.
    + Accessibility: Ensure that the information is presented in a way that is accessible to a wide audience, including policymakers, business leaders, and the general public.
    + User Education: Provide educational resources or documentation to help users understand the implications of the metrics and how to interpret the data correctly.

+ Data Privacy
    + Confidentiality: Protecting the privacy of individuals whose data is used in the analysis is paramount. This includes anonymizing data to prevent the identification of individuals.
    + Data Policies: Implement clear policies regarding data collection, storage, and usage. Users should be informed about what data is being collected and how it will be used.
    + Security Measures: Employ robust security measures to prevent data breaches and unauthorized access. This includes encryption, secure servers, and regular security audits.

+ Accountability for Errors
    + Error Identification: The system should be capable of identifying and acknowledging errors in predictions or data analysis.
    + Correction Mechanisms: Provide mechanisms for correcting errors promptly. This might include a feedback loop where users can report inaccuracies and a process for updating the data and models accordingly.
    + Minimizing Impact: Implement strategies to minimize the negative impact of errors on users. This could involve providing disclaimers about the limitations of predictions and avoiding over-reliance on automated decisions.

+ Ethical Use of Results
    + Beneficial Applications: Ensure that the predictions and insights generated by the application are used for societal benefits, such as developing employment support programs, educational initiatives, and workforce reskilling programs.
    + Avoiding Manipulation: Prevent the misuse of data and predictions for manipulating labor markets, political gain, or other unethical purposes. This includes setting guidelines and usage policies for stakeholders.
    + Stakeholder Engagement: Engage with various stakeholders, including labor organizations, policymakers, and community groups, to ensure the ethical use of results and address any concerns they might have.

+ Additional Considerations
    + Inclusivity in Development: Involve diverse perspectives in the development process, including those of affected workers, to ensure the tool addresses their needs and concerns.
    + Long-term Impact: Consider the long-term societal impacts of AI-driven job displacement and work towards solutions that promote economic stability and growth.
    + Regulatory Compliance: Ensure compliance with relevant regulations and standards related to data privacy, labor laws, and AI ethics.

## Data insights

+ The application allows to model effects of various reductions in different industries. The current analysis is based on a moderate reduction level 15%. The application helps to identify areas (let's use a state level for simplicity) that will be mostly affected. The list of affected areas and forecasted change in income and unemployment rate depend on the industry. Let's consider the following results:
  + *1011 - National resources and mining*: 
    + max change in per capita income is -0.6%, the most affected states are North Dakota and Wyoming (-0.6%), Alaska (-0.5%)
    + from unemployment perspective the most affected states are Alaska (from 4.23 to 4.72%), California (from 4.28 to 4.62%), New Mexico (from 4.1 to 4.57%), North Dakota (from 2.03 to 2.78%), Washington (from 4.12 to 4.47%), West Virginia (from 3.91 to 4.29%), Wyoming (from 3.43 to 4.39%)
  + *1012 - Construction*:
    + max change in per capita income is -0.65%, the most affected states are Virginia (-0.65%), Utah (-0.63%), Nevada (-0.58%), Lousiana (-0.54%), Montana (-0.53%), Oregon (-0.5%)
    + from unemployment perspective many states will be affected, let's list only those whose current unemployment rate is below the current (2022) national average unemployment rate (3.66%), but will exceed it: Arkansas (from 3.21 to 3.91%), Colorado (from 3.07 to 3.95%), Florida (from 3.01 to 3.84%), Georgia (from 3.14 to 3.75%), Idaho (from 2.84 to 3.84%), Indiana (from 3.06 to 3.76%), Lousiana (from 3.65 to 4.61%), Montana (from 2.7 to 3.69%), Oklahoma (from 3.06 to 3.69%), Virginia (from 2.82 to 4.04%), Wyoming (from 3.43 to 4.49%) 
  + *1013 - Manufacturing*
    + max change in per capita income is -1.47%, the most affected states are Indiana (-1.47%), Wisconsin (-1.31%), Iowa (-1.21%), Michigan (-1.19%)
    + from unemployment perspective almost all states are hardly affected, let's list those state whose forecated unemployment rate will exceed 5%: California (from 4.28 to 5.33%), Connecticut (from 4.1 to 5.33%), Ilinois (from 4.59 to 5.91%), Indiana (from 3.06 to 5.45%), Kentucky (from 4.04 to 5.88%), Michigan (from 4.15 to 6.01%), Missisipi (from 3.84 to 5.6%), Nevada (from 5.22 to 5.84%), Ohio (from 4.01 to 5.79%), Oregon (from 3.3 to 5.26%), Pennsylvania (from 4.07 to 5.38%)
  + *1021 - Trade, transportation and utilities*
    + max change in per capita income is -1.69%, most affected states are Virginia (-1.69%), Tennessee (-1.52%), Kentucky (-1.47%), Georgia (-1.47%), North Dakota (-1.43%)
    + from unemployment perspective all states are hardly affected, let's list those state whose forecated unemployment rate will exceed 7%: Alaska (from 4.23 to 7.07%), Illinois (from 4.58 to 7.49%), Kentucky (from 4.04 to 7.26%), Nevada (from 5.22 to 8.02%)
  + *1022 - Information*
    + max change in per capita income is -1.07%, most affected states are Washington (-1.07%), District of Columbia (-0.93%), California (-0.65%), New York (-0.5%)
    + from unemployment perspective only a few states are affected: California (from 4.28 to 4.76%), District of Columbia (from 4.75 to 5.68%), New York (from 4.35 to 4.82%), Washinghton (from 4.11 to 4.77%)
  + *1023 - Financial activities*
    + max change in per capita income is -1.69%, most affected states are New York (-1.69%), Delaware (-1.3%), District of Columbia (-1.2%), Connecticut (-1.09%)
    + from unemployment perspective many states are affected, the most significant changes in unemployment rate are for Delaware (from 4.27 to 5.74%), District of Columbia (from 4.75 to 5.87%)
  + *1024 - Professional and business services*
    + max change in per capita income is -5.9%, most affected states are District of Columbia (-5.9%), Virginia (-3.72%), Massachusetts (-2.19%)
    + from unemployment perspective many states are affected, the most significant changes in unemployment rate are for District of Columbia (from 4.75 to 11.62%), Virginia (from 2.82 to 7.48%)
  + *1026 - Leisure and hospitality*
    + max change in per capita income is -1.05%, most affected states are Nevada (-1.05%), District of Columbia (-0.89%), Hawaii (-0.82%), Virginia (-0.47%), Florida (-0.44%), Arizona (-0.4%)
    + from unemployment perspective many states are affected, the most significant changes in unemployment rate are for District of Columbia (from 4.75 to 7.6%), Hawaii (from 3.28 to 5.98%), Nevada (from 5.22 to 8.44%)
  + *1028 - Public administration*
    + max change in per capita income is -5.68%, most affected states are District of Columbia (-5.68%), Virginia (-1.02%), Alaska (-0.86%)
    + from unemployment perspective almost all states are slighty affected, with only two exceptions: Alaska (from 4.23 to 5.97%) and District of Columbia (from 4.75 to 12.09%)
  

+ *Conclusions*: 
  + from change in income perspective the most *sensitive* industries are 1024 - Professional and business services (max change is -5.9%) and 1028 - Public administration (-5.68%); the most *issensitive* industries are 1011 - National resources and mining (-0.6%), 1012 - Construction (-0.65%)
  + from unemployment perspective the most *sensitive* industries are 1028 - Public administration (max forecasted unemployment rate is 12.09%), 1024 - Professional and business services (11.62%), 1026 - Leisure and hospitality (8.44%), 1021 - Trade, transportation and utilities (8.02%)
  + even if change in per capita income is relatively small for some states, changes in an overall unemployment rate could be more significant. It is true for industries with relatively low wages. In opposite, industries with high average wages produce higher negative impact on changes in per capita income than on changes in the overall unemployment rate
  + states (and counties) with diverse economy will be affected less. Also economy divertissement should help fired employees to find new jobs (probably after trainings)
  + such analysis should help state and county authorities to be prepared for the labor market changes due to AI and related technological advancements

## References for the Data Source

+ BEA -Bureau of Economic Analysis:
    + Personal Income and Employment by Major Component: Bureau of Economic Analysis (2023). CAINC4 Personal Income and Employment by Major Component. Retrieved from BEA iTable: https://www.bea.gov/itable/

+ Bureau of Labor Statistics (BLS):
    + Labor Force and Employment by County: Bureau of Labor Statistics (BLS) (2023). Establishments, Employment and Wages by Industry. Retrieved from BLS LAU Tables: https://www.bls.gov/lau/tables.htm#cntyaa
    + Establishments, Employment and Wages by Industry: Bureau of Labor Statistics (2023). Establishment and Wages by Industry. Retrieved from BLS Data Views: https://data.bls.gov/cew/apps/data_views/data_views.htm#tab=Tables


+ How will Artificial Intelligenve affect Jobs 2024-2030
    + Talmage-Rostron, M. (2024, May 14). How will artificial intelligence affect jobs 2024-2030. Nexford University. https://www.nexford.edu/insights/how-will-ai-affect-jobs

+ The Ethical Considerations of Artificial Intelligence | Capitol Technology University
    + The Ethical Considerations of Artificial Intelligence | Capitol Technology University. (n.d.). https://www.captechu.edu/blog/ethical-considerations-of-artificial-intelligence

+ Federal Data Strategy Data Ethics Framework
    + Bradley, T., Ambrose, K., Bernstein, M., DeLoatch, I., Dreisigmeyer, D., Gonzales, J., Grubb, C., Haralampus, L., Hawes, M., Johnson, B., Kopp, B., Krebs, J., Marsico, J., Morgan, D., Osatuke, K., Vidrine, E., General Services Administration, Chief Data Officer Council, Interagency Council on Statistical Policy, & Federal Privacy Council. (n.d.). Federal Data Strategy Data Ethics Framework. In Federal Data Strategy Data Ethics Framework. https://resources.data.gov/assets/documents/fds-data-ethics-framework.pdf

+ AI and the quest for diversity and inclusion: a systematic literature review
    + Shams, R. A., Zowghi, D., & Bano, M. (2023). AI and the quest for diversity and inclusion: a systematic literature review. AI And Ethics. https://doi.org/10.1007/s43681-023-00362-w

## Python module that was not shown in class

+ For this project we used GeoPandas module that allows to add new properties to datasets in GeoJSON format. In Flask API we used GeoPandas DataFrames with states and counties boundaries from census.gov. Then we merged Pandas DataFrames with calculated metrics (e.g. industry share by employment or change in income) with those standard GeoPandas DataFrames and converted the result to GeoJSON, which is later used by JavaScript to create choropleth layers for maps.

## References for Code Used not our own

+ Remove legend on leaflet map
    + Remove legend on leaflet map. (n.d.). Stack Overflow. https://stackoverflow.com/questions/28265730/remove-legend-on-leaflet-map

+ Python TypeError: cannot convert dictionary update sequence element #1 to a sequence
    + Python TypeError: cannot convert dictionary update sequence element #1 to a sequence. (n.d.). Stack Overflow. https://stackoverflow.com/questions/27573687/python-typeerror-cannot-convert-dictionary-update-sequence-element-1-to-a-sequ
    
## Setup instructions

### Prerequisites

+ Python 3.x
+ Pandas and GeoPandas
+ Flask (including Flask CORS)
+ D3.js
+ Leaflet.js
+ Plotly.js
+ Bootstrap

### Folder structure

```plaintext
├── source                     # The folder contains all original and derived data that was used for the application. Prepared data is stored in SQLite DB
├── static
│   ├── css
│   │   └── style.css          # Contains the custom CSS styles for the application.
│   └── js
│       ├── choropleth.js      # Provides functionality for rendering choropleth maps using Leaflet.
│       └── logic.js           # Includes JavaScript functions to handle data fetching, map and chart rendering, and user interactions.
├── app.py                     # Backend server script to handle API requests and data processing.
├── index.html                 # The main HTML file that structures the web application.
└── data.sqlite                # SQLite database that contains all data required for the application.
```

#### Detailed descriptions of main files

+ **static/css/style.css**:
  + This file contains custom CSS styles for the application, ensuring a consistent and visually appealing design for all elements, including the maps and charts.

+ **static/js/choropleth.js**:
  + This JavaScript file provides the necessary functions to create and manage choropleth maps using the Leaflet library. It handles the color scales, legends, and data binding for the maps.

+ **static/js/logic.js**:
  + This file contains the main JavaScript logic for the application. It includes functions to fetch data from the API, render maps and charts, and handle user interactions with the dropdown menus and selectors.

+ **app.py**:
  + This script sets up a Flask server to handle API requests, processes data, and serves the front-end application. It contains endpoints to fetch state and industry data, as well as to generate employment and income maps, and unemployment rate data.
  
+ **index.html**:
  + The main HTML file that structures the web application. It includes references to the CSS and JavaScript files and sets up the layout of the page, including the dropdown menus, map containers, and chart containers.

+ **data.sqlite**:
  + SQLite database that contains the following tables:
    + state - a list of all 50 states and District of Columbia
    + county - a list of all counties related to the states
    + industry - a list of main 11 industries, the classification is provided by BLS
    + county_metric - a fact table that contains total income, population, labor force and employed metrics at county and year granularity
    + county_industry_metric - a fact table that contains annual establishments (not used), annual employment and total annual wages at county, year and industry granularity

![DB schema](DB%20schema.png)

### Installation
1. Clone the repository: 
```bash
git clone https://github.com/NataliiaShevchenko620/labor-market-trends-analyzer.git
cd labor-market-trends-analyzer
```

2. Install the required Python packages: 
```bash
pip install flask flask-cors geopandas pandas sqlalchemy
```
   
3. Run the Flask API server: 
```bash
python app.py
```

4. Open **index.html** in your web browser to view the application

### API Endpoints

+ GET /api/v1.0/get_states: Fetches the list of states.
+ GET /api/v1.0/get_industries: Fetches the list of industries.
+ GET /api/v1.0/get_employment_map/<state_code>/<industry_code>/<reduction>: Returns employment data for the map.
+ GET /api/v1.0/get_income_map/<state_code>/<industry_code>/<reduction>: Returns income data for the map.
+ GET /api/v1.0/get_unemployment_rate/<state_code>/<industry_code>/<reduction>: Returns unemployment rate data for the bar chart.
+ GET /api/v1.0/get_employment_trend/<state_code>/<industry_code>/<reduction>: Returns employment trend data for the line chart.

### Usage

+ Select an area (a particular state or *All states*), industry, and reduction percentage from the dropdown menus.
+ View the updated maps and charts reflecting the selected parameters.
+ Hover over map regions and chart elements to see detailed information.