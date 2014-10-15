import re, string

__DOSE_SYMBOL_RE = 'g|ug|mg|kg|l|ml|p|d|s|OP|CP|Mu|u|mg/kg|ml/kg|/kg|cm|in|micrograms'
__STRENGTH_RE = '([0-9.]+( )*(' + __DOSE_SYMBOL_RE + ')( |$|/)+)'

__DAILY_REPETITION_SYMBOL_RE = 'd|ad|d3|d4|d5|qw|tw|bw|ow|om|w2|mwf'
__DAILY_REPETITION_RE = '(^|[^\w\d])+(' + __DAILY_REPETITION_SYMBOL_RE + ')([^\w\d]|$)+'

__INTERVAL_FREQUENCY_SYMBOL_RE ='hh|h1|h2|h3|h4|h5|h6|h8|h12|h18|h24|hd|pd|qd|td|tid|bd|od'
__INTERVAL_FREQUENCY_RE = '(^|[^\w\d])+(' + __INTERVAL_FREQUENCY_SYMBOL_RE + ')([^\w\d]|$)+'

__DOSE_SYNTAX_HUMAN_MAP = {
    # Interval Frequence
    'hh': 'every30 minutes',
    'h1': 'every hour',
    'h2': 'every 2 hours',
    'h3': 'every 3 hours',
    'h4': 'every 4 hours',
    'h5': 'every 5 hours',
    'h6': 'every 6 hours',
    'h8': 'every 8 hours',
    'h12': 'every 12 hours',
    'h18': 'every 18 hours',
    'h24': 'every 24 hours',
    'hd': 'six times a day',
    'pd': 'five times a day',
    'qd': 'four times a day',
    'td': 'three times a day',
    'tid': 'three times a day',
    'bd': 'twice a day',
    'od': 'once a day',
    # Daily Repetition
    'd':  'daily',
    'ad': 'alternate days',
    'd3': 'every 3 days',
    'd4': 'every 4 days',
    'd5': 'every 5 days',
    'qw': 'four times a week',
    'tw': 'twice a week',
    'bw':  'twice a week',
    'ow':  'once a week',
    'om':  'once a month',
    'mwf': 'Monday, Wednesday, Friday',
    }


# def translate_non_alphanumerics(to_translate, translate_to=u'_'):
#     not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
#     translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
#     return to_translate.translate(translate_table)

def clean_token(token):
    translation_table = dict((ord(char), None) for char in string.punctuation)

    return token.translate(translation_table).strip()

def get_medicine_text_as_components(medicine_text):

    medicine_text_lower = medicine_text.lower()

    medicine_dict = {}

    # Medicine
    m = re.search('([A-Za-z ]{4,})', medicine_text)
    if m:
        medicine_dict['medicine'] = clean_token(m.group(0))

    # Strength
    m = re.search(__STRENGTH_RE, medicine_text_lower)
    if m:
        medicine_dict['medicine'] += ', ' + m.group(0).strip(string.punctuation)

    # Daily Repetition
    m = re.search(__DAILY_REPETITION_RE, medicine_text_lower)
    if m:
        medicine_dict['daily_repetition'] = __DOSE_SYNTAX_HUMAN_MAP[clean_token(m.group(0))]

    # Interval Frequency
    m = re.search(__INTERVAL_FREQUENCY_RE, medicine_text_lower)
    if m:
        medicine_dict['interval_frequency'] = __DOSE_SYNTAX_HUMAN_MAP[clean_token(m.group(0))]

    # # Instructions
    # m = re.search(__DOSE_RE, medicine_text_lower)
    # if m:
    #     interval = m.group(0).lower().strip()
    #     medicine_dict['dose'] = __DOSE_SYNTAX_HUMAN_MAP[interval]

    return medicine_dict