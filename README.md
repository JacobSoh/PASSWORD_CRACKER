## PASSWORD_CRACKER

A simple zipfile password cracker, either using a rainbow table or using a brute force.

# Things to look out for before using:

Available options when editing Settings.json
```json
{
  "METHOD": ["RAINBOW", "BRUTE FORCE"],
  "BRUTE_FORCE_LENGTH": ["Min: 1", "Max: 64"],
  "DICTIONARY": "Full Path",
  "FILE_PATH": "Full Path"
}
```
/h
The passwords for the two example files:
| File Name                 | Passwords |
|---------------------------|-----------|
| Example (Brute Force).zip | K21       |
| Example (Rainbow).zip     | pompus    |
