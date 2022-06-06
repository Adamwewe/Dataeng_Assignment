echo "Installing required python libraries..."

pip install pandas
pip install python-dotenv
pip install psycopg2
pip install numpy
pip install pytest

echo "Building local server..."

docker build . -t testdb
docker run  -e POSTGRES_PASSWORD=password -d -p 5432:5432 testdb
