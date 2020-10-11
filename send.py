import click
import csv
import configparser
import smtplib
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read("config.ini")


@click.command()
@click.option(
    "-b",
    "--bodyfile",
    required=True,
    type=click.File("r"),
    help="Filename for content of the email, you can use str.format placeholders from the csv file here",
)
@click.option(
    "-t",
    "--tofile",
    required=True,
    type=click.File("r"),
    help="Filename to read for recipiencts. CSV format (with ',' separator and MUST contain 'email' column!",
)
@click.option(
    "--really",
    required=False,
    default=False,
    is_flag=True,
    help="Really send the email, if not set just prints out the first generated message for preview purposes.",
)
def send(bodyfile, tofile, really):
    # read the body
    body = bodyfile.read().rstrip()

    reader = csv.reader(tofile)
    # first line has the columns
    headers = next(reader)
    if "email" not in headers:
        raise ValueError("email column not found in tofile!")

    # init our email
    click.echo(f"Connecting to smtp server: {config['smtp']['host']} ... ", nl=False)
    s = smtplib.SMTP(host=config["smtp"]["host"], port=int(config["smtp"]["port"]))
    s.starttls()
    s.login(config["smtp"]["user"], config["smtp"]["password"])
    click.echo(f"Connected")

    # go through the csv, read the data into a dict with the headers
    # build the body from the template and send away
    for row in reader:
        # read the line into a data dict
        data = {headers[i]: row[i] for i in range(len(headers))}
        # format the message with the data
        message = body.format(**data)

        # First line is our subject
        subject, message = message.split("\n", 1)

        msg = MIMEText(message)
        msg["From"] = config["smtp"]["from"]
        msg["To"] = data["email"]
        msg["Subject"] = subject

        # only preview if really is not set
        if not really:
            click.echo("'--really' not set not really sending")
            click.echo(
                "Here is a dump of the generated email data from the first row of the list of recipients:"
            )
            click.echo("=" * 80)
            click.echo(msg.as_string())
            click.echo("=" * 80)
            click.echo(f"The message would be sent to email address: {data['email']}")
            break


        click.echo(f"Sending to: {data['email']} ... ", nl=False)

        s.sendmail(config["smtp"]["from"], data["email"], msg.as_string())

        click.echo(" sent")

    s.quit()


if __name__ == "__main__":
    send()
