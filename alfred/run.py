import alfred

@alfred.command("run", help="execute the application")
def run():
    """
    execute the application

    >>> $ alfred run
    """
    streamsync = alfred.sh("streamsync", "streamsync should be present")
    alfred.run(streamsync, ['run', 'src/app'])


@alfred.command("edit", help="design the application")
@alfred.option("--remote", help="enable edition through public connection", is_flag=True)
def edit(remote: bool = False):
    """
    execute the application in edition mode

    >>> $ alfred edit
    """
    args = []
    if remote:
        args.append('--enable-remote-edit')
    args += ['edit', 'src/app']

    streamsync = alfred.sh("streamsync", "streamsync should be present")
    alfred.run(streamsync, args)


@alfred.command("run.db", help="run the database and pgadmin")
def run_db():
    """
    execute the application

    >>> $ alfred run.db
    """
    docker_compose = alfred.sh("docker-compose", "docker_compose should be present")
    alfred.run(docker_compose, ['up', 'db', 'pgadmin'])


@alfred.command("run.db.init", help="populate the database with the Adventureworks dataset")
def run_init_db():
    """
    execute the application

    >>> $ alfred run.db.init
    """
    docker_compose = alfred.sh("docker-compose", "docker_compose should be present")
    alfred.run(docker_compose, ['exec', 'db', 'bash', '-c', 'cd /data; psql --user admin -d Adventureworks < install.sql'])
