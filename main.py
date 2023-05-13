from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Define the data model for a trip
class Planner(BaseModel):
    id: Optional[int] = None  # Optional ID for the trip
    destination: str         # Destination of the trip
    DateOfTrip: str          # Date of the trip
    Accommodations: str      # Accommodations for the trip

# Endpoint to create a new trip
@app.post("/trips/")
def create_trips(trip: Planner):
    with open('trips.json', 'r') as f:
        data = json.load(f)                 # Load existing data from the file
        trips = data['trips']                # Get the list of trips from the data
        trip.id = len(trips) + 1             # Assign a unique ID to the new trip
        trips.append(trip.dict())            # Add the new trip to the list
    
    with open('trips.json', 'w') as f:
        json.dump(data, f, indent=4)         # Write the updated data back to the file
    
    return trip                            # Return the created trip

# Endpoint to retrieve a list of trips
@app.get("/trips/")
def read_trips(skip: int = 0, limit: int = 10):
    with open('trips.json', 'r') as f:
        data = json.load(f)                 # Load data from the file
        trips = data['trips']                # Get the list of trips from the data
    
    return trips[skip : skip + limit]      # Return a subset of trips based on the skip and limit parameters

# Endpoint to update a trip
@app.put("/trips/{trip_id}")
def update_trip(trip_id: int, trip: Planner):
    with open('trips.json', 'r') as f:
        data = json.load(f)                 # Load data from the file
        trips = data['trips']                # Get the list of trips from the data
        for i, t in enumerate(trips):
            if t['id'] == trip_id:           # Find the trip with the specified ID
                trips[i] = trip.dict()       # Update the trip with the new data
                break
        else:
            raise HTTPException(status_code=404, detail="Trip not found")  # Raise an exception if the trip is not found
    
    with open('trips.json', 'w') as f:
        json.dump(data, f, indent=4)         # Write the updated data back to the file
    
    return trip                            # Return the updated trip

# Endpoint to cancel a trip
@app.delete("/trips/{trip_id}")
def cancel_trip(trip_id: int):
    with open('trips.json', 'r') as f:
        data = json.load(f)                 # Load data from the file
        trips = data['trips']                # Get the list of trips from the data
        for i, trip in enumerate(trips):
            if trip['id'] == trip_id:        # Find the trip with the specified ID
                del trips[i]                 # Delete the trip from the list
                break
        else:
            raise HTTPException(status_code=404, detail="Trip not found")  # Raise an exception if the trip is not found
    
    with open('trips.json', 'w') as f:
        json.dump(data, f, indent=4)         # Write the updated data back to the

    return {"message": "Trip canceled"}


########################################################################################################

# Note: The 'trips.json' file is being used as a static database to store trip information.
# Ensure that the file exists in the same directory as this script and contains valid JSON data.
# The file should have an initial structure like: {'trips': []} if no trips have been added yet.
# To connect to the server and interact with the API endpoints, follow these steps:
# 1. Ensure you have FastAPI and Uvicorn installed. You can install them using pip:
#    ```
#    pip install fastapi uvicorn
#    ```
# 2. Save the code in a Python file (e.g., `main.py`).
# 3. Open a terminal or command prompt and navigate to the directory where the Python file is saved.
# 4. Start the server by running the following command:
#    ```
#    uvicorn main:app --reload
#    ```
#    This command will start the server, and you should see output indicating that the server is running.
# 5. Open your web browser and visit http://localhost:8000/docs to access the API documentation.
#    This documentation provides detailed information about each endpoint and allows you to send requests directly.
#    - To create a new trip, click on the "POST /trips/" endpoint and provide the trip data in the request body.
#    - To retrieve a list of trips, click on the "GET /trips/" endpoint.
#    - To update a trip, click on the "PUT /trips/{trip_id}" endpoint and provide the updated trip data in the request body.
#      Replace `{trip_id}` with the ID of the trip you want to update.
#    - To cancel a trip, click on the "DELETE /trips/{trip_id}" endpoint.
#      Replace `{trip_id}` with the ID of the trip you want to cancel.
#    The documentation also provides examples and shows the expected request formats and data structures.
# 6. Explore and interact with the API endpoints according to your requirements.
# 7. After you finish using the API, you can stop the server by pressing `Ctrl + C` in the terminal or command prompt.

# Note: Make sure to modify the server host and port if needed, as specified in the `uvicorn.run` function in the code.

