set -o errexit

pip install -r requiremnets.txt

python manage.py collectstatic --no-input
python manage.py migrate