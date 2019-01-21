# ProUnitas
Mapping for services
Welcome to the ProUnitas mapping service. The goal of this program is to help students and educators locate resources via an interactive map of services. This program will take raw services data and map them onto a marker laden map to show where the services for students are located. It performs this action with the following steps:
1. Load a csv file with ProUnitas Services (this generally comes from a salesforce data dump)
2. Clean data - adding fields like 'State' filling in missing entries with blank strings, and taking \n (new line characters) and turning them into spaces. 
3. Add lat/lon coordinates to the data - this is required because some mapping services do not plot addresses
4. Create a map of Houston
5. Add markers to the map that show the services and their names
6. Save the map to the maps directory


To Run:
1. Clone the repo from GitHub onto your local machine
2. Install python 3.X
3. Navigate to the directory ProUnitas in command line/terminal
4. On Windows Machines, run the setup.bat file. On non Windows machines (linux, macOS), open terminal, enter <pip install -r requirements.txt>
5. In cmd/terminal, enter >python prounitas_map.py
6. After run, open up the map in the maps directory


TO DO:
Optimize lat/lon constructor
Optimize get_lat_long method
Create google map api key and move mapper to google maps
add name, address, primary service area, and rating of the service
