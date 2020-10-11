# Tre hacklab email sender

Sends email to list of users. Mainly used for notifying a group of users of something important.

## Usage

Copy config.ini.example to config.ini and configure your smtp server settings into it.

Write your message into `example_message.txt` (example provided). Collect your recipients into a `example_list.csv` (example provided).

Run the script without --really flag to test the connection to the smtp server and getting a dump of the message that would be sent.

```
pipenv shell
python send.py -b example_message.txt -t example_list.txt
```

After that looks ok rerun with the --really flag set

```
pipenv shell
python send.py -b example_message.txt -t example_list.txt --really
```

## TODO

* Better documentation
* Better secret handling
* Add error checking everywhere
* Check that the message was really sent
