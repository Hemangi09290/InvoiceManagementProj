one = ["", "One ", "Two ", "Three ", "Four ",
       "Five ", "Six ", "Seven ", "Eight ",
       "Nine ", "Ten ", "Eleven ", "Twelve ",
       "Thirteen ", "Fourteen ", "Fifteen ",
       "Sixteen ", "Seventeen ", "Eighteen ",
       "Nineteen "]

# strings at index 0 and 1 are not used,
# they is to make array indexing simple
ten = ["", "", "Twenty ", "Thirty ", "Forty ",
       "Fifty ", "Sixty ", "Seventy ", "Eighty ",
       "Ninety "]


# n is 1- or 2-digit number
def num_to_words(n, s):
    str_num = ""

    # if n is more than 19, divide it
    if n > 19:
        str_num += ten[n // 10] + one[n % 10];
    else:
        str_num += one[n]

        # if n is non-zero
    if n:
        str_num += s

    return str_num


# Function to print a given number in words
def convert_to_words(n):
    # stores word representation of given
    # number n

    if len(str(n)) > 9:
        return n
    out = ""

    # handles digits at ten millions and
    # hundred millions places (if any)
    out += num_to_words((n // 10000000), "Crore ")

    # handles digits at hundred thousands
    # and one millions places (if any)
    out += num_to_words(((n // 100000) % 100), "Lakh ")

    # handles digits at thousands and tens
    # thousands places (if any)
    out += num_to_words(((n // 1000) % 100), "Thousand ")

    # handles digit at hundreds places (if any)
    out += num_to_words(((n // 100) % 10), "Hundred ")

    if n > 100 and n % 100:
        out += "and "

        # handles digits at ones and tens
    # places (if any)
    out += num_to_words((n % 100), "")

    return out

