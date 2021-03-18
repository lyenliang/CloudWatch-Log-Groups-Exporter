# CloudWatch Log Groups Exporter

This program allows you to export multiple AWS CloudWatch log groups to an S3 bucket.


## Benefits of this Program

AWS only allows us to export 1 CloudWatch log group at a time. 

When we have multiple log groups to export, we have to do it one by one. This would require a lot of time and manual operations.

With this program, you can run those exports in one command. You no longer have to export, wait, export, and wait ...


## Usage

1. Set your AWS credentials in `config.yml`.

2. Set the `destination_bucket` field in `config.yml`. This field specifies which S3 bucket you want the logs to export to. 

3. Write down the log groups that you want to export to `config.yml`

4. Specify the time range of your export in `config.yml`

5. Run `python3 export_cloudwatch_logs.py`


## Format of the Export

Suppose you want to export the data under cloudwatch log group `my/log/group` from 2018/01/01 through 2018/04/01.

After executing the program, you will find the following folders generated under `<destination_bucket>` S3 bucket.

* `<destination_bucket>/my/log/group/2018-01-01_2018-02-01/`
* `<destination_bucket>/my/log/group/2018-02-01_2018-03-01/`
* `<destination_bucket>/my/log/group/2018-03-01_2018-04-01/`