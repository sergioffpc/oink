# OINK! Test Framework
The `oink` test framework is an automated testing environment oriented to SIP call testing.

## Build
To build the `oink` test framework project you need to run the following command inside the `test/` directory.

```buildoutcfg
docker-compose build
```

## Set up target environment
To set up the target environment you need to edit the `docker-compose.yml` and change the following user-specific data:

```buildoutcfg
-Dapi=[http|https]://<host>:<port> -Dusername=<username> -Dpassword=<password> -Daccount_name=<account-name> -Dproxy=<host>:<port>
```

User-specific data meanings:
* `api`, The `Crossbar` application HTTP(S) REST API used for provisioning.
* `username`, The account username.  Need to have permissions to create and delete child accounts and regular users and
  devices. 
* `password`, The account password.
* `account_name`, The master account name.  This account SHOULD be exclusive to testing environment because all it's
  children accounts will be removed `before` and `after` every scenario.
* `proxy`, The SIP Proxy server to which the UAC test agents will connect to register and make calls.

**WARNING**: You SHOULD create a dedicated account for you tests because all the children accounts will be automatically
removed by the test framework.

## Run tests
To run the `oink` test framework you need to be inside the `test/` directory and execute the following command:
```buildoutcfg
docker-compose run integration-tests [arguments]
```

You can use the following arguments:
* `-d, --dry-run`, Invokes formatters without executing the steps.
* `--no-capture`, Don’t capture stdout any output will be printed immediately.
* `-t, --tags`, Only execute features or scenarios with tags matching **TAG_EXPRESSION**.
* `--show-timings`, Print the time taken, in seconds, of each step after the step has completed. This is the default behaviour. This switch is used to override a configuration file setting.
* `-v, --verbose`, Show the files and features loaded.
* `-w, --wip`, Only run scenarios tagged with `wip`. Additionally: use the `plain` formatter, do not capture stdout or logging output and stop at the first failure.

For more information you can see: https://behave.readthedocs.io/en/latest/behave.html#command-line-arguments .

### Tag Expression
Scenarios inherit tags that are declared on the Feature level. The simplest **TAG_EXPRESSION** is simply a tag:

> --tags=@dev

You may even leave off the `@`.

You can also exclude all features / scenarios that have a tag, by using boolean NOT:
> --tags="not @dev"

A tag expression can also use a logical OR:
> --tags="@dev or @wip"

The –tags option can be specified several times, and this represents logical AND, for instance this represents the boolean expression:
> --tags="(@foo or not @bar) and @zap"

You can also exclude several tags:
> --tags="not (@fixme or @buggy)"

