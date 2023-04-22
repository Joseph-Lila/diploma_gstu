# About project


## Installation

1. Clone repository
2. Run commands (they will run postgresql database):
    
`docker build .`

`docker-compose build`

`docker-compose up -d`

3. Create `.env` file and add fields which are met in `src/config.py`
4. Run `main.py` (don't forget about requirements)
5. If you want to create tables and init them with initial data, check `src/bootstrap.py`


## Review

The App helps to make a schedule for the university. There are two mods: 
manual and automatic. 

Also you can:

- Generate PDF with schedule
- Fill the schedule using two views at the same time 
(groups/mentors/audiences/workloads)
- Mark that mentor cannot teach in certain time


## About author

My phone number: +375333242810

Email: arturprokopenko01@gmail.com

### Feel free to contact me!


Kind regards, Joseph-Lila
