set -euo pipefail
IFS=$'\n\t'

# Run a case command
case $1 in
    server)
    # Pull in Docker env
    WEBSITE_BASE_NAME="$(printenv WEBSITE_NAME)"
    BASE_PATH=/var/www/${WEBSITE_BASE_NAME}
    cd $BASE_PATH
    python3 manage.py makemigrations --no-input
    python3 manage.py migrate --no-input
    echo "Made Migrations..."
    python3 manage.py collectstatic --no-input
    echo "Collected Static"
    sudo apache2ctl -D FOREGROUND
    sudo a2enmod headers
    sudo service apache2 start
    echo "Apache server started"
    ;;

esac
