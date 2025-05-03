# ELECTRONIC VOTING SYSTEM 

## Steps to run the project
- Install the dependencies
```bash
pip install -r requirements.py
```
- Create a `.env` file with the following DB details
```bash
DB_HOST=<DB_HOST>
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DB_NAME>
```
- Run the `helper.py` file to create the tables, constraints, stored procedures and initialize them with sample data
```
python helper.py
```
- Run application
```bash
python app.py
```