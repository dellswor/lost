# Run the python script to insert the roles and output the role maping
python3 gen_inserts1.py > tmp.sql

# run the sql script
psql $1 -p $2 -f tmp.sql > map.txt

# run the script to generate the user inserts
python3 gen_inserts2.py > tmp.sql

# insert the users
psql $1 -p $2 -f tmp.sql

# clean up the temp file
rm tmp.sql map.txt
