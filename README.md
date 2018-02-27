dumpTwitterFollowers
====================

## Description
`dumpTwitterFollowers.py` is [yet another](https://github.com/search?l=Python&q=twitter+followers+python&type=Repositories) python utility created to easily dump the list of a Twitter user's followers in CSV format.

Unlike other similar solutions, dumpTwitterFollowers.py features:
* Configurable location of tweetrc file (with consumer and access tokens)
* Configurable fields to dump, through external file *USER_FIELDS*
* Configurable logging, through external file *logging.conf*
* Ability to specify multiple twitter usernames through cmd line or inside a given file.
* Automatically retries on recoverable disconnect errors.
* Optionally runs output CSV through gzip compression (where available).

## Dependencies
You may need to install the following dependencies.

* [python 3.4+](https://www.python.org/downloads)
* pip install python-twitter
* pip install unicodecsv

## Usage
```bash
usage: dumpTwitterFollowers.py [-h] [-rc TWEETRC] [-ff FROM_FILE] [-z]
                               [screen_name [screen_name ...]]

positional arguments:
  screen_name           list of screen names

optional arguments:
  -h, --help            show this help message and exit
  -rc TWEETRC, --tweetrc TWEETRC
                        tweetrc file for API auth
  -ff FROM_FILE, --from-file FROM_FILE
                        read screen names from file
  -z, --gzip            run CSV output through gzip
```

## Tweetrc file
The script needs a tweetrc file with a Twitter application's consumer and user access tokens. A sample file is provided with dummy values.

To create a twitter application go to [apps.twitter.com](https://apps.twitter.com), and follow the simple instructions in the [python-twitter docs](https://python-twitter.readthedocs.io/en/latest/getting_started.html). Once you have the consumer and user access tokens, paste them in a file in the same format as *tweetrc-sample*, name it **.tweetrc** and place it in your home directory. The script tries to load by default ~/.tweetrc, unless you pass it the -rc argument with a different path.

## Examples of Usage
To dump all your Twitter followers to CSV file named *aTwitterScreenName-%Y%m%d.csv*
```bash
./dumpTwitterFollowers.py aTwitterScreenName
```

Same as above, but run through gzip, resulting in a file named *aTwitterScreenName-%Y%m%d.csv.gz*
```bash
./dumpTwitterFollowers.py -z aTwitterScreenName
```

You may also dump the followers of several accounts at once, providing their screen names as a blank-separated list.
Each will be dumped to its own separate file.
```bash
./dumpTwitterFollowers.py aTwitterScreenName anotherTwitterScreenName yetAnotherTwitterScreenName
```

For long-running processes you may want to invoke the script with `nohup` and send to background (Linux/Unix only)
```bash
nohup ./dumpTwitterFollowers.py accountWithThousandsOfFollowers &
```

If you wish to dump all followers of a long list of users, you may provide instead a file containing 1 username per line.
```bash
nohup ./dumpTwitterFollowers -ff listOfScreenNames.txt &
```

## Customizing output
The list of user fields to be dumped for each follower is listed, and can be customized, in the file named **USER_FIELDS**.
A full description of user fields available is given in Twitter's API [User object page](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object)

## Related resources
* Check out [python-twitter](https://github.com/bear/python-twitter), if you want to contribute to or modify this script.
* [twarc](https://github.com/docnow/twarc) is a great command-line tool (also written in python) to query Twitter's api.

## Contact
Follow us on Twitter, [@expectbigdata](https://twitter.com/expectbigdata)
