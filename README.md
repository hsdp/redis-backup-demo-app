redis-backup-demo-app
=====================

This application demonstrates how to use Cloud Foundry tasks with a docker
based application to backup a redis database to an s3 bucket.  HSDP specific
service brokers are used in the instructions so other platforms may require
modifications to work.

Using Diego tasks for administration has couple of benefits.  When a task is
run a new container is created from the parent applications droplet.  The task
container also inherits the environment from the parent.  This creates a
convenient way to execute a task within the context of a running application.
Using a docker image makes it fairly painless to package up all the tools that
may be needed to manage things like backups that are not directly part of the
application but are part of the application lifecycle.

The demo app will return a JSON response with random data pulled from the bound
redis instance.  Tasks can be used to populate/flush/backup/restore the redis
instance with some randomly generated test data.  The demo application can be
deployed by simply cloning this repo and running a `cf push` from the repo root.
The backing services will need to be created before pushing the application.  You
may need to modify the manifest file if your backing services have names other
than the names used in the example commands.

**Create backing services**
```
cf cs hsdp-redis-sentinel redis-development redis
cf cs hsdp-s3 s3_bucket s3
```
The `hsdp-redis-sentinel` service broker is asynchronous so you will need to
wait until provisioning is completed before proceeding.  Check the status of
provisioning with the `cf services` and wait until it is in the `succeeded`
state before proceeding.

**Push application**
```
cf push
```
The default manifest file will push with the `random-route: true` setting so
you will need to get the route from the output of push or the output of the
`cf apps` command.  You should be able to reach the application at this point.
Pointing your web browser to the endpoint should return a `"No data exists!"`
response.  At this point you may also want to open a separate terminal and
run use `cf logs redis-backup` to watch the logging output from the
application.

**Seed Redis with random data**
```
cf run-task redis-backup "/application/scripts/redis-seed.py"
```
If you are watching the logs you should see some output like this -
`2018-02-25T07:52:17.28-0800 [APP/TASK/068ea2c7/0] OUT Added 100 records
to redis.`  You should how be able to point your web browser at the endpoint
and get back a response with a JSON key/value pair.  The response should have a
GUID asthe key and some random latin words as the value.  You can rerun the
seed task as many times as you want and it will add an additional 100 records
on each run.

**Backup data to S3**
```
cf run-task redis-backup "/application/scripts/redis-backup.py"
```
This will backup all the data currently in redis to the S3 service instance
bound to the application.  You can verify by going to the S3 service dashboard
and inspecting the bucket contents.  If you are watching the logs you should
see a message like this when the backup in complete --
`2018-02-25T08:19:36.19-0800 [APP/TASK/b5a6d8ba/0] OUT Redis backup complete.`

**Flush data from Redis**
```
cf run-task redis-backup "/application/scripts/redis-flush.py"
```
This task should purge all the data currently in the Redis instance.  You
should get the default response of `"No data exists!"` again in your web
browser.  You should also see a log message like this --
`2018-02-25T08:21:03.67-0800 [APP/TASK/3bb855da/0] OUT Redis data flushed!`

**Restore data to Redis**
```
cf run-task redis-backup "/application/scripts/redis-restore.py"
```
This will restore the data backup in S3 to the running Redis instance.  You
should see a log message like this when the restore is complete --
`2018-02-25T08:24:21.05-0800 [APP/TASK/889efbb7/0] OUT Redis restore complete.`
Test by pointing your browser back to the application endpoint to see a valid
response.
