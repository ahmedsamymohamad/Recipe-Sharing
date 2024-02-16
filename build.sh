set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

mkdir -p /media/images
chmod 775 /media/images