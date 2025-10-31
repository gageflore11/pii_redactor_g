import spacy
import re


def pii_redactor(input_path, output_path):

    nlp = spacy.load("en_core_web_sm")


    with open(input_path, 'r') as file:                            # Change file as needed
        content = file.read()
        doc = nlp(content)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # Matches Emails 
        # [a-zA-Z0-9_.+-]+ - Repeated one or more times: Any lowercase/capital letter, number, underscore, period, plus sign, and dash
        # @ - Symbol splitting local part and domain 
        # [a-zA-Z0-9-]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
        # \. - Matches one period
        # [a-zA-Z0-9-.]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+' 

        # Matches Phone numbers
        # \(? - Escapes parenthesis so it's taken as a literal character '(' instead of grouping
        # [0-9]{3} - Exactly 3 numbers in range of 0-9
        # \)? - Escapes parenthesis so it's taken as a literal character ')' instead of grouping
        # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
        # [0-9]{3} - Exactly 3 numbers in range of 0-9
        # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
        # [0-9]{4} - Exactly 4 numbers in range of 0-9
        phone_pattern = r'\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4}'
        
        # Macthes SSN
        # [0-9]{3} - Exactly 3 numbers in range of 0-9
        # \- - Exactly one dash
        # [0-9]{2} - Exactly 2 numbers in range of 0-9
        # \- - Exactly one dash
        # [0-9]{4} - Exactly 4 numbers in the range of 0-9
        social_pattern = r'[0-9]{3}\-[0-9]{2}\-[0-9]{4}'

        # Macthes Credit Card Numbers
        # [0-9]{4} - Exactly 4 numbers in range of 0-9
        # [\s] - macthes one space
        # [0-9]{4} - Exactly 4 numbers in range of 0-9
        # [\s] - macthes one space
        # [0-9]{4} - Exactly 4 numbers in range of 0-9
        # [\s] - macthes one space
        # [0-9]{4} - Exactly 4 numbers in range of 0-9
        credit_card_pattern = r'[0-9]{4}[\s][0-9]{4}[\s][0-9]{4}[\s][0-9]{4}'

        # Matches Bank Account Numbers
        # [0-9]{9} - Exactly 9 numbers in range of 0-9
        bank_account_pattern = r'[0-9]{9}'
        
        # Matches Addresses
        # [0-9]{1,5} - 1 to 5 numbers in the range of 0-9
        # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
        # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
        # [A-Z]{2}\s - Matches the state, two capital letters
        # [0-9]{5} - Matches the zip code, five numbers in range of 0-9
        address_pattern = r'[0-9]{1,5} [\sA-Za-z]+,\s[\sA-Za-z]+,\s[A-Z]{2}\s[0-9]{5}'

        ipv4_address_pattern = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'

        ipv6_address_pattern = r'[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}'

        mac_address_pattern = r'[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}'

        vin_pattern = r'[A-HJ-NPR-Z0-9]{17}'

        date_pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4}'

        license_plate_pattern = r'[A-Z]{3}-*\d{4}'

        #passport_pattern = r'[A-Z]{1}[0-9]{8}'
        passport_pattern = r'passport.*?[A-Z]{1}[0-9]{8}'
        
        student_id_pattern = r'[A-Z]{1}[0-9]{6,8}'

        drivers_licenses_pattern = [
            r"\d{7}",                       # AL, AK, DE, ME, OR, DC, WV
            r"[a-zA-Z]\d{8}",               # AZ, GA, NE, VA
            r"\d{9}",                       # AZ, CT, HI, IA, LA, MT, NM, SC, UT
            r"9\d{8}",                      # AR
            r"[a-zA-Z]\d{7}",               # CA
            r"\d{2}-\d{3}-\d{4}",           # CO
            r"[a-zA-Z](\d{3}-*){2}\d{2}-*\d{3}-*\d", # FL
            r"[a-zA-Z]{2}\d{6}[a-zA-Z]",    # ID
            r"[a-zA-Z]\d{3}-*(\d{4}-*){2}", # IL
            r"\d{4}-\d{2}-\d{4}",           # IN
            r"\d{3}[a-zA-Z]{2}\d{4}",       # IA
            r"[a-zA-Z](\d{2}-){2}\d{4}",    # KA
            r"[a-zA-Z]\d{2}-\d{3}-\d{4}",   # KY
            r"[a-zA-Z]-*(\d{3}-*){4}",      # MD
            r"[a-zA-Z]\d{9}",               # MA, MO, OK
            r"[a-zA-Z](\s\d{3}){4}",        # MI
            r"[a-zA-Z]\d{12}",              # MI, MN
            r"\d{3}-\d{2}-\d{4}",           # MS
            r"([0][1-9]|[1][0-2])\d{3}([1-9]\d{3})", # MT
            r"\d{10}",                      # NV
            r"([0][1-9]|[1][0-2])([a-zA-Z]\{3})(0[1-9]|[1-2][0-9]|3[0-1])\d", # NH
            r"[a-zA-Z]\d{4}-*(\d{5}-*){2}", # NJ
            r"(\d{3}){2}\s\d{3}",           # NY
            r"\d{12}",                      # NC
            r"[a-zA-Z]{3}-\d{2}-\d{4}",     # ND
            r"\d{8}",                       # OH, SD, TX, VT
            r"[a-zA-Z]{1}\d{4,8}",          # OH
            r"[a-zA-Z]{2}\d{3,7}",          # OH
            r"\d{2}( \d{3}){2}",            # PA
            r"[1-9]{2}\d{5}",               # RI
            r"\d{7,9}",                     # TN
            r"\d{7}[a-zA-Z]",               # VT
            r"[a-zA-Z](\d{2}-){2}\d{4}",    # VA
            r"[a-zA-Z]{3}\*\*[a-zA-Z]{2}\d{3}[a-zA-Z]\d", # WA
            r"[a-zA-Z]\d{6}",               # WV
            r"[a-zA-Z]\d{3}-(\d{4}-){2}\d{2}", # WI
            r"\d{6}-\d{3}",                 # WY
        ]    



        phone_redaction = '[PHONE]'
        ssn_redaction = '[SSN]'
        credit_card_redaction = '[CREDIT/DEBIT CARD]'
        bank_account_redaction = '[BANK ACCOUNT]'
        name_redaction = '[NAME]'
        email_redaction = '[EMAIL]'
        address_redaction = '[ADDRESS]'
        ipv4_redaction = '[ipv4]'
        ipv6_redaction = '[ipv6]'
        mac_redaction = '[MAC]'
        vin_redaction = '[VIN]'
        license_plate_redaction = '[LICENSE PLATE #]'
        passport_redaction = '[PASSPORT #]'
        date_redaction = '[DATE]'
        driver_license_redaction = '[DRIVER LICENSE #]'

        content = re.sub(phone_pattern, phone_redaction, content, flags=re.M)
        content = re.sub(social_pattern, ssn_redaction, content, flags=re.M)
        content = re.sub(credit_card_pattern, credit_card_redaction, content, flags=re.M)
        content = re.sub(bank_account_pattern, bank_account_redaction, content, flags=re.M)
        content = re.sub(email_pattern, email_redaction, content, flags=re.M)
        content = re.sub(address_pattern, address_redaction, content, flags=re.M)
        content = re.sub(ipv4_address_pattern, ipv4_redaction, content, flags=re.M)
        content = re.sub(ipv6_address_pattern, ipv6_redaction, content, flags=re.M)
        content = re.sub(mac_address_pattern, mac_redaction, content, flags=re.M)
        content = re.sub(vin_pattern, vin_redaction, content, flags=re.M)
        content = re.sub(license_plate_pattern, license_plate_redaction, content, flags=re.M)
        content = re.sub(passport_pattern, passport_redaction, content, flags=re.M | re.IGNORECASE)
        content = re.sub(date_pattern, date_redaction, content, flags=re.M)
        for num in drivers_licenses_pattern:
            content = re.sub(num, driver_license_redaction, content, flags=re.M)




        for name in names:
            content = content.replace(name, name_redaction)



        with open(output_path, 'w') as file:                         # Change file as needed
            file.write(content)