# Clone the repository
git remote add origin https://github.com/Omina123/SMARTFARM.git
cd smartseason

# Install dependencies
pip install -r requirements.txt


# Run migrations
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
Access the app at http://127.0.0.1:8000/
Under staff register (i hav provided users to select roles by themselves )
If they chooos field agent thy wll be redirected to agent field else they will be  rediercted to the admin dash
=================================================================================
 Design Decisions
🏗 Data Architecture
I implemented a two-tier data model to separate botanical data from operational logistics:

Crop Model: Stores "Static" growth data (Variety, Planting Date, Expected Harvest Date, Acreage).

Field Model: Stores "Dynamic" operational data (Field Name, Assigned Agent, Current Stage, and Observation Notes).
==============================================================
🔐 Access Control (RBAC)
The system uses a custom User model with user_type distinctions:

Admin: Access to the global dashboard, field creation, and agent assignment.

Field Agent: Restricted view showing only assigned fields with the ability to update stages and notes.
==================================================================
📊 Business Logic: Field Status Logic
One of the core requirements was a Computed Status. I chose to implement this using a Python @property decorator rather than a database field. This ensures the status is always "live" and recalculates every time the page is refreshed.
========================================================================
Status Rules:
Completed: Automatically set when the field stage is moved to Harvested.

At Risk: Triggered if:
========================================================
The current date is past the expected_harvest_date but the stage is not "Harvested".

The crop has been in the "Planted" or "Growing" stage for over 100 days (indicating stalled progress).

Active: The default state for any field within its expected growth window.
=========================================================================
📝 Assumptions
Linear Lifecycle: Crops move strictly from Planted → Growing → Ready → Harvested.

Agent Assignment: A field can only be assigned to one agent at a time for accountability.

Stalled Growth: 100 days is used as the threshold for "stalled" growth to trigger a risk alert if the agent hasn't updated the stage.


============================================================================================
Field Status Logic Approach

The system uses a dynamic computation strategy for field statuses to ensure data accuracy without manual intervention.

Completed: Triggered strictly by the operational stage. Once a Field Agent marks a field as "Harvested," the status shifts to Completed.

At Risk: This is an automated "Watchdog" status. It flags a field if the current date exceeds the expected_harvest_date defined during crop creation. It also flags fields where progress appears stalled (e.g., remaining in the 'Growing' stage for over 100 days).

Active: The default state for any field currently within its expected growth window.