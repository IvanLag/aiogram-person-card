import re
phone_regexp_1 = r"^(\+|)[0-9]+$"
phone_check_pattern_1 = re.compile(phone_regexp_1)
phone_num = '-55595555'
s = phone_check_pattern_1.fullmatch(phone_num)
print(not not s)