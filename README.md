# Technical Report

## Abstract

Aegis is an account audit tool designed to be used by organizations to support the awareness layer of the defence in depth security model. It is a Python application that utilizes a low-budget password strength estimation algorithm against active directory account files to highlight weak passwords. It utilizes the HaveIBeenPwned API to check each account's credentials to see if they have been involved in prior data breaches.

The software supports both automatic and manual extraction of account information from an active directory server. Once extracted, the account file can be opened within the application and generate a report highlighting weaknesses along with other statistical information. The report can then be used to make informed decisions on security policy in order to fortify weak accounts.


## Contents


[TOC]





## Introduction

This report will cover the design and development of Aegis; the ideas behind each of the features and how they evolved throughout the requirements, design, and implementation stages. It will also detail the usage of the software, and what the user can do to adequately utilize it's capabilities.


### The Brief

The project brief was "Write a program someone could run to check an Active Directory (or similar) to assess if network users have any weak passwords (e.g. duplicates, weak, common, etc). The program should also run a check on the users to check if anyone has an account that has been compromised in a data breach using the haveibeenpwned service."


### What is Aegis?

Aegis is a Linux application developed in Python. The primary function is to perform a scan on an active directory and flag weak passwords based on a predetermined criteria. Furthermore, the application will check the given emails associated with the accounts using the HaveIBeenPwned API to determine if the email address has been subject to any prior data breaches that compromise the security of their frequently used passwords.


## Requirements Analysis

The primary target audience is medium to large businesses that utilise computer systems which manage multiple accounts on an active directory server. Security is a key concern for any company that needs to store data on computer systems and weak passwords open up a large attack vector. This means Aegis can efficiently highlight any weak accounts and passwords so they can be adequately secured. Due to the product being enterprise facing, the application prioritises functionality over form, and provides the end-user some more advanced settings that can be used to tailor the software to fit their needs.

**Minimum viable product:**



1. Must check passwords in an active directory against predetermined criteria for a strong password
2. Must use the HaveIBeenPwned API to check accounts and show if it has been in a breach previously.
3. Must support manual extraction of account data from an active directory

**Additional Features:**



4. Should have customizable reporting including text output, email output and a wordcloud of frequently used passwords
5. Should support automatic remote extraction of password data from a Windows Server
6. Passwords should not be visible to any external API
7. Password statistic reporting, displaying worst passwords, password length distributions and how many meet strength requirements


### User Stories

User stories were generated for various use cases of the program in order to develop a complete set of features.


<table>
  <tr>
   <td>#
   </td>
   <td>Feature Title
   </td>
   <td>Description
   </td>
   <td>Priority
   </td>
   <td>Notes
   </td>
  </tr>
  <tr>
   <td>1
   </td>
   <td>Password Strength
   </td>
   <td>User wants to check the strength of passwords in an active directory
   </td>
   <td>Must Have
   </td>
   <td>Password strength research on trello
   </td>
  </tr>
  <tr>
   <td>2
   </td>
   <td>Email breach detection
   </td>
   <td>User wants to check if emails in the active directory have been in data breaches 
   </td>
   <td>Must Have
   </td>
   <td>HaveIBeenPwned api
   </td>
  </tr>
  <tr>
   <td>3
   </td>
   <td>Manual Extraction Support
   </td>
   <td>User wants to extract account files from the active directory themselves (useful if it's not on the same network)
   </td>
   <td>Must Have
   </td>
   <td>Manual selection of SAM & System files /w instructions
   </td>
  </tr>
  <tr>
   <td>4
   </td>
   <td>Privacy
   </td>
   <td>User wants to ensure that their account data is secure when using the program
   </td>
   <td>Must Have
   </td>
   <td>HIBP's k-privacy model
   </td>
  </tr>
  <tr>
   <td>5
   </td>
   <td>Automatic Extraction Support
   </td>
   <td>User wants to extract account files from an active directory on the same network automatically
   </td>
   <td>Should Have
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>6
   </td>
   <td>Password breach detection
   </td>
   <td>User wants to check if passwords in the active directory have been in data breaches
   </td>
   <td>Should Have
   </td>
   <td>HaveIBeenPwned API
   </td>
  </tr>
  <tr>
   <td>7
   </td>
   <td>Wordcloud Support
   </td>
   <td>User wants to display the most commonly used passwords in a wordcloud
   </td>
   <td>Should Have
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>8
   </td>
   <td>Top 10 Passwords
   </td>
   <td>User wants to see the best passwords used on the active directory along with their statistics
   </td>
   <td>Should Have
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>9
   </td>
   <td>Top 10 Worst Passwords
   </td>
   <td>User wants to see the worst passwords used on the active directory along with their statistics
   </td>
   <td>Should Have
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>10
   </td>
   <td>Password Length Distributions
   </td>
   <td>User wants to see most common length distributions to make decisions on password policy
   </td>
   <td>Should have
   </td>
   <td>
   </td>
  </tr>
</table>



    


## User Interaction & Design

**UI Considerations**

The target audience plays a large part in how our UI is designed. One of the primary objectives was to ensure functionality over form as it's targeted at more advanced users. Over time this was pivoted from the idea of making it purely command line interface to make it somewhat more accessible with a graphical user interface. 

**Early UI Mockup**



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Technical-Report0.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Technical-Report0.png "image_tooltip")


**Final UI Design**



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Technical-Report1.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Technical-Report1.png "image_tooltip")



## Implementation

This section will cover the implementation of the requirements set out in the requirements analysis phrase.


#### Check passwords in an active directory against predetermined criteria for a strong password

When the user generates a report from a '.pot' file that contains the extracted passwords from the active directory it uses a low budget password strength estimation algorithm to score the password from 0-4, 0 being easy to crack and 4 being extremely difficult to crack.


#### HaveIBeenPwned API to check accounts and show if it has been in a breach previously.

This is implemented in two forms:



*   **Password checking **- When the report is generated it will show how many times a password has been caught in a data breach.
*   **Email checking** - The user can choose to check an individual email address. This is a separate function from the core report as active directory accounts often won't have an email associated with them.


#### Manual extraction of account data from an Active Directory

To manually extract the hashes the user must first follow the provided instructions inside the program or the user guide to extract a copy of the SYSTEM and ntds.dit files that store the account information. The user can then enter their file paths in Aegis to decrypt the ntds.dit file using the keys stored in the SYSTEM hive so the hashes can be cracked by external software.


#### Automatic remote extraction of password data from a Active Directory

This was implemented as a simpler method to the manual extraction, if the user is on the same network they can enter the account username and password along with the IP address of the domain controller to automatically extract the files in a hashed format, ready to crack.


#### Reports including text output and a wordcloud of frequently used passwords

This is implemented as two buttons:



*   Generate Report - This will use the account file to generate a report showing detailed information on accounts and passwords
*   Generate Password Cloud - This will use the account file to generate a wordcloud with word size based on its frequency, and colour based on its strength.


#### Passwords should not be visible to any external API

When sending passwords to the HaveIBeenPwned API we utilize it's 'k-anonymity' model which allows us to only send the first 5 characters of password's hash and still get the same results [1][2].


#### Password statistic reporting, displaying worst passwords, password length distributions and how many meet strength requirements

This is implemented through the report which will display:



*   Top 10 Best Passwords
*   Top 10 Worst Passwords
*   Password Length Distribution Graph
*   Password composition statistics


## User Guide


## Installation

Python 2.7+ and pip are required. Then:

_(Tested on Kali Linux running Python 2.7.15)_



1. pip install -r requirements.txt
2. python aegisui.py


### Step 1. Database Extraction

To start, you need to extract a copy of ntds.dit, the file that contains the password hashes for the active directory. You can do this either remotely (a) or manually (b):


#### 
a. Remote database extraction

Note: Requires you to be on the same network as the domain controller.



1. In the remote extraction section, enter the administrator username and password along with the IP address of the Domain Controller.
2. Click the 'Extract' button
3. **Skip to step 3**

#### 
b. Local database extraction

1. Open a command prompt as admin on the domain controller
2. Run ntdsutil "ac i ntds" "ifm" "create full c:\temp" q q
3. Securely extract c:\temp\Active Directory\ntds.dit and c:\temp\registry\SYSTEM to your device that is running Aegis.
4. Move on to Step 2.




### Step 2. Extracting hashes

_(Skip this step if you used remote extraction)_

If you extracted the hashes manually then you will need to decrypt them using the SYSTEM hive:



1. Enter the file path for the SYSTEM and ntds.dit files that you manually extracted in the appropriately labeled text boxes in the local extraction section.
2. Once extracted your hash file can be found at yourdomain.hashes.ntlm


### Step 3. Cracking passwords

Now we need to crack the hashes in order to generate a .pot file with containing the raw passwords to be analysed by Aegis. For this you'll need to use a password cracking tool like John the Ripper or Hashcat. I would recommend a Hashcat dictionary attack with H0bRules for the most complete results.



1. Install hashcat using 'apt-get install hashcat'
2. Put your desired wordlist (e.g. rockyou.txt) and rule file (e.g. hob064.rule) in the directory
3. Run 'hashcat -m 1000 --potfile-path yourdomain.pot --username yourdomain.hashes.ntlm rockyou.txt -r hob064.rule'


### Step 4. Generating the report

Now that the hashes have been cracked, you can load them with Aegis and generate your report:



1. Now you have the .pot file with your cracked hashes, enter the name of the pot file and the active directory domain name and click Generate Report for a text output or Generate Password Cloud for a wordcloud output.


### Step 5. Checking Email Breaches

Aegis automatically checks passwords with the HaveIBeenPwned API, however it does not automatically check email addresses, due to the fact that an active directory account will often not have an email address associated with it.



1. Enter the email address you want to check in the text box
2. Press 'Check Email'


### Step 6. Understanding the Results


#### Report


<table>
  <tr>
   <td><strong>Column</strong>
   </td>
   <td><strong>Function</strong>
   </td>
  </tr>
  <tr>
   <td>Password
   </td>
   <td>Extracted password in plaintext
   </td>
  </tr>
  <tr>
   <td>Length
   </td>
   <td>The numerical length of the password
   </td>
  </tr>
  <tr>
   <td>Count
   </td>
   <td>Frequency which the password was used
   </td>
  </tr>
  <tr>
   <td>Score
   </td>
   <td>Score (0-4; with 0 being too guessable and 4 being very unguessable) based on the quality of the password based on Dropbox's zxcvbn password strength estimation algorithm.
   </td>
  </tr>
  <tr>
   <td>Pwned #
   </td>
   <td>Number of times the password has been found in breaches by HaveIBeenPwned
   </td>
  </tr>
  <tr>
   <td>Users
   </td>
   <td>List of all users using this password
   </td>
  </tr>
</table>


**Note:** Passwords are transmitted to HaveIBeenPwned using the k-Anonymity model which only sends a partial hash, therefore they can never been seen externally.

**_Word Cloud_**

The Word Cloud is coloured based on the password's score, and sized based on the frequency of the password.


## Handover Report


### Key Python Libraries Used:

These are some of the most important libraries have been used and their function within Aegis. The full list of libraries can be found in the requirements section of the appendix.


<table>
  <tr>
   <td><strong>Library</strong>
   </td>
   <td><strong>Use</strong>
   </td>
  </tr>
  <tr>
   <td>Cryptography
   </td>
   <td>Provides the cryptographic tools used for extracting the hashes
   </td>
  </tr>
  <tr>
   <td>Wordcloud
   </td>
   <td>Used to generate the password cloud
   </td>
  </tr>
  <tr>
   <td>zxcvbn
   </td>
   <td>Dropbox's low budget password strength estimation library - used for scoring passwords
   </td>
  </tr>
  <tr>
   <td>Impacket
   </td>
   <td>Suite of cryptography tools used to parse NTDS.dit
   </td>
  </tr>
</table>



### Core Modules

**AegisUI.py**

Tkinter based UI, uses text input boxes and buttons to perform functions identical to the command line in a more accessible environment. Absolute positioning is used for UI elements which could be problematic for wider compatibility. ScrolledText mirrors the standard output of the CLI.

**Aegis.py**

Command line backend to the UI. Allows user to interact with the program through only the command line to increase compatibility in enterprise scenarios.

**ntds_parser.py**

Uses imports from CoreSecurity's impacket, a collection of python classes for working with network protocols to parse NTLM authentications using password hashes. This is what is used for decrypting the ntds.dit file using the SYSTEM hive.

**Output Modules**

Separate output modules are used for different types of outputs, allowing for greater future compatibility with other output options like email or PDF. The current build contains a stdout module for printing to the console/ScrolledText box in the UI, and the password_cloud module for outputting to the password cloud.

**stdout.py**

This was originally created as a module for printing the report into the console window, however when the UI was created it was efficient to have the ScrolledText box mirror the console's STDOUT. This has lead to a number of text formatting and alignment problems which are unresolved thus far, however the functionality is all there.

The handling for analysing the passwords with the zxcvbn low budget password strength estimation algorithm and HaveIBeenPwned is also done inside this module. 

**password_cloud.py**

Used the 'WordCloud' and 'matplotlib' libraries to generate a word cloud based on the strength and frequency of a password.


## Conclusions


### Aegis and Your Company

Despite its potential use as a penetration testing tool, the in-house security applications of Aegis is where it shines the most, we've developed a series of tips through research and testing on how you can use Aegis to bolster your company's defence in depth.



1. Phase in training on password and account security, discuss why they're important and simple techniques people can pick up as habits. It is vital people understand the full intent of policy changes they may find annoying otherwise.
2. Progressively increase the minimum password length and complexity requirements over time. The introduction of the idea of passphrases, using words that wouldn't commonly be used together is useful for making this easier for employees to adapt to.
3. Roll out a password manager like KeePass or something similar along with training for all employees.
4. Use Aegis to find problem employees with poor security and educate them on good security practice. Consider introducing a strike system for employees that are repeat offenders, as they are opening up a serious attack vector within your company.
5. Schedule performing an account audit using Aegis regularly, this will ensure people are sticking with the new standards.
6. Avoid forcing users to reset their password after a certain number of days, there is substantial research [3] suggesting this encourages weaker passwords rather than stronger ones.


### Project Takeaways

Throughout the course of this project we discovered a lot about active directories, how they work, their security measures and most importantly, subverting those security measures. The product of that being producing a well rounded, versatile tool that could be effectively utilized by a CEO and a penetration tester alike. The research we undertook concerning account policy, and how that fits into the defence in depth security model was extremely valuable for the development of the product, as implementing cutting edge research makes this a tool that could be a solid addition to any company's security arsenal. 




## References

[1] Troy Hunt - Pwned Passwords v2 - K-Anonymity [https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/)

[2] Cloudflare - Validating Leaked Passwords with K-Anonymity [https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/)

[3] Why the 90 Day Rule for Password Changing? [https://www.sans.org/security-awareness-training/blog/why-90-day-rule-password-changing](https://www.sans.org/security-awareness-training/blog/why-90-day-rule-password-changing)

[4] asn1crypto==0.24.0

[https://github.com/wbond/asn1crypto](https://github.com/wbond/asn1crypto)

[5] backports.functools-lru-cache==1.4

[https://github.com/jaraco/backports.functools_lru_cache](https://github.com/jaraco/backports.functools_lru_cache)

[6] cffi==1.11.2

[https://pypi.org/project/cffi/](https://pypi.org/project/cffi/)

[7] cryptography==2.1.4

[https://pypi.org/project/cryptography/](https://pypi.org/project/cryptography/)

[8] cycler==0.10.0

[https://github.com/matplotlib/cycler](https://github.com/matplotlib/cycler)

[9] enum34==1.1.6

[https://pypi.org/project/enum34/](https://pypi.org/project/enum34/)

[10] idna==2.6

[https://pypi.org/project/idna/](https://pypi.org/project/idna/)

[11] ipaddress==1.0.19

[https://github.com/phihag/ipaddress](https://github.com/phihag/ipaddress)

[12] ldap3==2.2.3

[https://pypi.org/project/ldap3/](https://pypi.org/project/ldap3/)

[13] matplotlib==2.1.1

[https://matplotlib.org/](https://matplotlib.org/)

[14] numpy==1.13.3

[https://github.com/numpy/numpy](https://github.com/numpy/numpy)

[15] pandas==0.21.1

[https://github.com/pandas-dev/pandas](https://github.com/pandas-dev/pandas)

[16] Pillow==5.0.0

[https://github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow)

[17] pyasn1==0.4.2

[https://github.com/etingof/pyasn1](https://github.com/etingof/pyasn1)

[18] pycparser==2.18

[https://github.com/eliben/pycparser](https://github.com/eliben/pycparser)

[19] crackedit==1.0.0

[https://github.com/eth0izzle/cracke-dit](https://github.com/eth0izzle/cracke-dit)

[20] pycrypto==2.6.1

[https://github.com/dlitz/pycrypto](https://github.com/dlitz/pycrypto)

[21] pyOpenSSL==17.5.0

[https://github.com/pyca/pyopenssl](https://github.com/pyca/pyopenssl)

[22] pyparsing==2.2.0

[https://github.com/pyparsing/pyparsing](https://github.com/pyparsing/pyparsing)

[23] python-dateutil==2.6.1

[https://github.com/dateutil/dateutil](https://github.com/dateutil/dateutil)

[24] pytz==2017.3

[https://github.com/stub42/pytz](https://github.com/stub42/pytz)

[25] six==1.11.0

[https://github.com/benjaminp/six](https://github.com/benjaminp/six)

[26] subprocess32==3.2.7

[https://github.com/google/python-subprocess32](https://github.com/google/python-subprocess32)

[27] tinydb==3.7.0

[https://github.com/msiemens/tinydb](https://github.com/msiemens/tinydb)

[28] tinydb-serialization==1.0.4

[https://github.com/msiemens/tinydb-serialization](https://github.com/msiemens/tinydb-serialization)

[29] ujson==1.35

[https://github.com/esnme/ultrajson](https://github.com/esnme/ultrajson)

[30] wordcloud==1.3.1

[https://github.com/amueller/word_cloud/tree/master/wordcloud](https://github.com/amueller/word_cloud/tree/master/wordcloud)

[31] zxcvbn==1.0

[https://github.com/dropbox/zxcvbn](https://github.com/dropbox/zxcvbn)


## Appendix


### Requirements

_Contained within requirements.txt for easy installation with 'pip install -r requirements.txt'_

asn1crypto==0.24.0
backports.functools-lru-cache==1.4
cffi==1.11.2
cryptography==2.1.4
cycler==0.10.0
enum34==1.1.6
idna==2.6
ipaddress==1.0.19
ldap3==2.2.3
matplotlib==2.1.1
numpy==1.13.3
pandas==0.21.1
Pillow==5.0.0
pyasn1==0.4.2
pycparser==2.18
pycrypto==2.6.1
pyOpenSSL==17.5.0
pyparsing==2.2.0
python-dateutil==2.6.1
pytz==2017.3
six==1.11.0
subprocess32==3.2.7
tinydb==3.7.0
tinydb-serialization==1.0.4
ujson==1.35
wordcloud==1.3.1
zxcvbn==1.0


<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Technical-Report2.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Technical-Report2.png "image_tooltip")



<!-- Docs to Markdown version 1.0β16 -->
