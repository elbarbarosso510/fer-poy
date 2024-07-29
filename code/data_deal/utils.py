

def clean_string(string):
	return string.strip().lower()

domain_chars_set = set([chr(ord("a") + i) for i in range(0, 26)] + [str(i) for i in range(10)] + ["-", "."])
def have_other_characters(domain):
    if len(set(domain)-domain_chars_set) > 0:
        return True
    return False


