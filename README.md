# dude-wheres-my-car

![Dude, Where's My Car?][logo]

Dude, where's my car?

## Quickstart

Run the following commands to bootstrap your environment

    git clone https://github.com/demosdemon/dude
    cd dude
    make install
    cp .env.example .env
    # TODO: add a run command

You should see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration

    flask db init
    flask db migrate
    flask db upgrade
    npm start

## Deployment

To deploy

    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export DATABASE_URL="<YOUR DATABASE URL>"
    make build
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment variable is unset or is set to ``0``.

## Shell

To open the interactive shell, run

    flask shell

By default, you will have access to the flask `app`.

## Running Tests

To run all tests, run

    flask test

## Migrations

Whenever a database migration needs to be made, run the following commands

    flask db migrate

This will generate a new migration script. Then run

    flask db upgrade

To apply the migration.

For full migration command reference, run `flask db --help`.

[logo]: assets/img/dude-wheres-my-car.png "Dude, Where's My Car?"
