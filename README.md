# Aegis - Technical Report

## Abstract

Aegis is an audit tool designed to be used by organizations to support the awareness layer of the defence in depth security model. It is a Python application that utilizes a low-budget password strength estimation algorithm on active directory account files to highlight weak passwords. Along with this, it utilizes the HaveIBeenPwned API to check each account's credentials to see if they have been caught in past breeches.

The software supports both automatic and manual extraction of account information from an active directory server. Once extracted, the account file can be opened within the application and generate a report highlighting weaknesses along with other statistical information. The report can then be used to make informed decisions on security policy in order to fortify weak accounts.


## Introduction

### The Brief

Our project brief was "Write a program someone could run to check an Active Directory (or similar) to assess if network users have any weak passwords (e.g. duplicates, weak, common, etc). The program should also run a check on the users to check if anyone has an account that has been compromised in a data breach using the haveibeenpwned service."


### What is Aegis?

Aegis is a Linux application developed in Python. The primary function is to perform a scan on an active directory and flag weak passwords based on a predetermined criteria. Furthermore, the application will check the given emails associated with the accounts using the HaveIBeenPwned API to determine if the email address has been subject to any prior data breaches that compromise the security of their frequently used passwords.


## Requirements Analysis

Our primary target audience is medium to large businesses that utilise computer systems which manage multiple accounts on an active directory server. Security is a key concern for any company that needs to store data on computer systems and weak passwords open up a large attack vector, so a tool like this can help efficiently highlight any weak accounts and passwords so they can be adequately secured. Due to the product being enterprise facing, the application prioritises functionality over form, and provides the end-user some more advanced settings that they can use to tailor the software to fit their needs.


### User Stories


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


**Minimum viable product:**



1. Must check passwords in an active directory against predetermined criteria for a strong password
2. Must use the HaveIBeenPwned API to check accounts and show if it has been in a breach previously.
3. Must support manual extraction of account data from an active directory

**Additional Features:**



4. Should have customizable reporting including text output, email output and a wordcloud of frequently used passwords
5. Should support automatic remote extraction of password data from a Windows Server
6. Passwords should not be visible to any external API
7. Password statistic reporting, displaying worst passwords, password length distributions and how many meet strength requirements

    



## User Interaction & Design

**UI Considerations**

Our target audience plays a large part in how our UI is designed. We wanted to aim primarily for functionality over form as it's targeted at more advanced users but we pivoted away from the idea of making it a command line interface to make it somewhat more accessible. 

**Early UI Mockup**



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Technical-Report0.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Technical-Report0.png "image_tooltip")


**Final UI Mockup design**



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


#### Reporting including text output and a wordcloud of frequently used passwords

This is implemented as two buttons:



*   Generate Report - This will use the account file to generate a report showing detailed information on accounts and passwords
*   Generate Password Cloud - This will use the account file to generate a wordcloud with word size based on its frequency, and colour based on its strength.


#### Passwords should not be visible to any external API

When sending passwords to the HaveIBeenPwned API we utilize it's 'k-anonymity' model which allows us to only send the first 5 characters of password's hash and still get the same results [1][2].


#### Password statistic reporting, displaying worst passwords, password length distributions and how many meet strength requirements

This is implemented through the report where we display:



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

### 
Step 1. Database Extraction


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




### 
Step 2. Extracting hashes

_(Skip this step if you used remote extraction)_

If we extracted the hashes manually then we'll need to decrypt them using the SYSTEM hive:



1. Enter the file path for the SYSTEM and ntds.dit files that you manually extracted in the appropriately labeled text boxes in the local extraction section.
2. Once extracted your hash file can be found at yourdomain.hashes.ntlm

### 
Step 3. Cracking passwords


Now we need to crack the hashes in order to generate a .pot file with containing the raw passwords to be analysed by Aegis. For this you'll need to use a password cracking tool like John the Ripper or Hashcat. I would recommend a Hashcat dictionary attack with H0bRules for the most complete results.



1. Install hashcat using 'apt-get install hashcat'
2. Put your desired wordlist (e.g. rockyou.txt) and rule file (e.g. hob04.rule) in the directory
3. Run 'hashcat -m 1000 --potfile-path yourdomain.pot --username yourdomain.hashes.ntlm rockyou.txt -r hob064.rule'

### 
Step 4. Generating the report


Now that the hashes have been cracked, you can load them with Aegis and generate your report:



1. Now you have the .pot file with your cracked hashes, enter the name of the pot file and your active directory domain name and click Generate Report for a text output or Generate Password Cloud for a wordcloud output.


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

**Python Libraries Used:**


<table>
  <tr>
   <td><strong>Library</strong>
   </td>
   <td><strong>Use</strong>
   </td>
  </tr>
  <tr>
   <td>asn1crypto
   </td>
   <td>Serializing ASN.1 structures
   </td>
  </tr>
  <tr>
   <td>backports.functools-lru-cache
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>cffi
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Cryptography
   </td>
   <td>Provides cryptographic tools we used for extracting the hashes
   </td>
  </tr>
  <tr>
   <td>cycler
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>enum34
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>idna
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>ipaddress
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>ldap3
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>matplotlib
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>numpy
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pandas
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Pillow
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pyasn1
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pycparser
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pycrypto
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pyOpenSSL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pyparsing
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>python-dateutil
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>pytz
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>six
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>subprocess32
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>tinydb
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>tinydb-serialization
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>ujson
   </td>
   <td>
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
   <td>Dropbox's low budget password strength estimation library
   </td>
  </tr>
</table>



## Conclusions


## References

[1] Troy Hunt - Pwned Passwords v2 - K-Anonymity [https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/](https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/)

[2] Cloudflare - Validating Leaked Passwords with K-Anonymity [https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/)


## Bibliography


## Appendices



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Technical-Report2.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Technical-Report2.png "image_tooltip")



<!-- Docs to Markdown version 1.0β16 -->
