# CONTAINS ANY CONSTANS BEING USED IN THE PROJECT

#ISO 3166 country name and alpha-3 code
COUNTRIES = {
'Afghanistan' : 'AFG',
'Akrotiri' : 'GBR',
'Albania' : 'ALB',
'Algeria' : 'DZA',
'American Samoa' : 'ASM',
'Andorra' : 'AND',
'Angola' : 'AGO',
'Anguilla' : 'AIA',
'Antarctica' : 'ATA',
'Antigua and Barbuda' : 'ATG',
'Argentina' : 'ARG',
'Armenia' : 'ARM',
'Aruba' : 'ABW',
'Ashmore and Cartier Islands' : 'AUS',
'Australia' : 'AUS',
'Austria' : 'AUT',
'Azerbaijan' : 'AZE',
'Bahamas' : 'BHS',
'Bahrain' : 'BHR',
'Baker Island' : 'UMI' ,
'Bangladesh' : 'BGD',
'Barbados' : 'BRB',
'Belarus' : 'BLR',
'Belgium' : 'BEL',
'Belize' : 'BLZ',
'Benin' : 'BEN',
'Bermuda' : 'BMU',
'Bhutan' : 'BTN',
'Bolivia' : 'BOL',
'Bosnia and Herzegovina' : 'BIH',
'Botswana' : 'BWA',
'Bouvet Island' : 'BVT',
'Brazil' : 'BRA',
'British Indian Ocean Territory' : 'IOT',
'British Virgin Islands' : 'VGB',
'Brunei' : 'BRN',
'Bulgaria' : 'BGR',
'Burkina Faso' : 'BFA',
'Burma' : 'MMR',
'Burundi' : 'BDI',
'Cabo Verde' : 'CPV',
'Cambodia' : 'KHM',
'Cameroon' : 'CMR',
'Canada' : 'CAN',
'Cayman Islands' : 'CYM' ,
'Central African Republic' : 'CAF',
'Chad' : 'TCD',
'Chile' : 'CHL',
'China' : 'CHN',
'Christmas Island' : 'CXR',
'Clipperton Island' : 'FRA',
'Cocos Islands' : 'CCK',
'Colombia' : 'COL',
'Comoros' : 'COM',
'Congo' : 'COG',
'Cook Islands' : 'COK',
'Coral Sea Islands' : 'AUS',
'Costa Rica' : 'CRI',
'Cote d\'Ivoire' : 'CIV',
'Croatia' : 'HRV',
'Cuba' : 'CUB',
'Curacao' : 'CUW',
'Cyprus' : 'CYP',
'Czechia' : 'CZE',
'Denmark' : 'DNK',
'Dhekelia' : 'GBR',
'Djibouti' : 'DJI',
'Dominica' : 'DMA',
'Dominican Republic' : 'DOM',
'Ecuador' : 'ECU',
'Egypt' : 'EGY',
'El Salvador' : 'SLV',
'Equatorial Guinea' : 'GNQ',
'Eritrea' : 'ERI',
'Estonia' : 'EST',
'Eswatini' : 'SWZ',
'Ethiopia' : 'ETH',
'Falkland Islands ' : 'FLK',
'Faroe Islands' : 'FRO',
'Fiji' : 'FJI',
'Finland' : 'FIN',
'France' : 'FRA',
'French Guiana' : 'GUF',
'French Polynesia' : 'PYF',
'French Southern and Antarctic Lands' : 'ATF',
'Gabon' : 'GAB',
'Gambia' : 'GMB',
'Georgia' : 'GEO',
'Germany' : 'DEU',
'Ghana' : 'GHA',
'Gibraltar' : 'GIB',
'Greece' : 'GRC',
'Greenland' : 'GRL',
'Grenada' : 'GRD',
'Guadeloupe' : 'GLP',
'Guam' : 'GUM',
'Guatemala' : 'GTM',
'Guernsey' : 'GGY',
'Guinea' : 'GIN',
'Guinea-Bissau' : 'GNB',
'Guyana' :  'GUY',
'Haiti' : 'HTI',
'Heard Island and McDonald Islands' : 'HMD',
'Holy See (Vatican City)' : 'VAT',
'Honduras' : 'HND',
'Hong Kong' : 'HKG',
'Hungary' : 'HUN',
'Iceland':'ISL',
'India' : 'IND',
'Indonesia' : 'IDN',
'Iran' : 'IRN',
'Iraq' : 'IRQ',
'Ireland' : 'IRL',
'Isle of Man' : 'IMN',
'Israel' : 'ISR',
'Italy' : 'ITA',
'Jamaica' : 'JAM',
'Jan Mayen' : None,
'Japan' : 'JPN',
'Jersey' : 'JEY',
'Jordan' : 'JOR',
'Kazakhstan' : 'KAZ',
'Kenya' : 'KEN',
'Kiribati' : 'KIR',
'Korea' : 'PRK',
'Korea' : 'KOR',
'Kosovo' : None,
'Kuwait' : 'KWT',
'Kyrgyzstan' : 'KHZ',
'Laos' : 'LAO',
'Latvia' : 'LVA',
'Lebanon' : 'LBN',
'Lesotho' : 'LSO',
'Liberia' : 'LBR',
'Libya' : 'LBY',
'Liechtenstein' : 'LIE',
'Lithuania' : 'LTU',
'Luxembourg' : 'LUX',
'Macau' : 'MAC',
'Madagascar' : 'MDG',
'Malawi' : 'MWI',
'Malaysia' : 'MYS',
'Maldives' : 'MDV',
'Mali' : 'MLI',
'Malta' : 'MLT',
'Marshall Islands' : 'MHL',
'Martinique' : 'MTQ',
'Mauritania' : 'MRT',
'Mauritius' : 'MUS',
'Mayotte' : 'MYT',
'Mexico' : 'MEX',
'Micronesia' : 'FSM',
'Midway Islands' : None,
'Moldova' : 'MDA',
'Monaco' : 'MCO',
'Mongolia' : 'MNG',
'Montenegro' : 'MNE',
'Montserrat' : 'MSR',
'Morocco' : 'MAR',
'Mozambique' : 'MOZ',
'Myanmar' : 'MMR',
'Namibia' : 'NAM',
'Nauru' : 'NRU',
'Navassa Island' : None,
'Nepal' : 'NPL',
'Netherlands' : 'NLD',
'New Caledonia' : 'NCL',
'New Zealand' : 'NZL',
'Nicaragua' : 'NIC',
'Niger' : 'NER',
'Nigeria' : 'NGA',
'Niue' : 'NIU',
'Norfolk Island' :'NFK',
'North Macedonia' : 'MKD',
'Northern Mariana Islands' : 'MNP',
'Norway' : 'NOR',
'Oman' : 'OMN',
'Pakistan' : 'PAK',
'Palau' : 'PLW',
'Palestine' : 'PSE',
'Palmyra Atoll' : None,
'Panama' : 'PAN',
'Papua New Guinea' : 'PNG',
'Paracel Islands' : None,
'Paraguay' : 'PRY',
'Peru' : 'PER',
'Philippines' : 'PHL',
'Pitcairn Islands' : 'PCN',
'Poland' : 'POL',
'Portugal' : 'PRT',
'Puerto Rico' : 'PRI',
'Qatar' : 'QAT',
'Reunion' : 'REU',
'Romania' : 'ROU',
'Russia' : 'RUS',
'Rwanda' : 'RWA',
'Saint Barthelemy' : 'BLM',
'Saint Helena' : 'SHM',
'Saint Kitts and Nevis' : 'KNA',
'Saint Lucia' : 'LCA',
'Saint Martin' : 'MAF',
'Saint Pierre and Miquelon' : 'SPM',
'Saint Vincent and the Grenadines' : 'VCT',
'Samoa' : 'WSM',
'San Marino' : 'SMR',
'Sao Tome and Principe' : 'STP',
'Saudi Arabia' : 'SAU',
'Senegal' : 'SEN',
'Serbia' : 'SRB',
'Seychelles' : 'SYC',
'Sierra Leone' : 'SLE',
'Singapore' : 'SGP',
'Sint Maarten' : 'SXM',
'Slovakia' : 'SVK',
'Slovenia' : 'SVN',
'Solomon Islands' : 'SLB',
'Somalia' : 'SOM',
'South Africa' : 'ZAF',
'South Georgia and the Islands' : 'SGS',
'South Sudan' : 'SSD',
'Spain' : 'ESP',
'Spratly Islands' : None,
'Sri Lanka' : 'LKA',
'Sudan' : 'SDN',
'Suriname' : 'SUR',
'Svalbard' : 'SJM',
'Sweden' : 'SWE',
'Switzerland' : 'CHE',
'Syria' : 'SYR',
'Taiwan' : 'TWN',
'Tajikistan' : 'TJK',
'Tanzania' : 'TZA',
'Thailand' : 'THA',
'Timor-Leste' : 'TLS',
'Togo' : 'TGO',
'Tokelau' : 'TKL',
'Tonga' : 'TON',
'Trinidad and Tobago' : 'TTO',
'Tromelin Island' : None,
'Tunisia' : 'TUN',
'Turkey' : 'TUR',
'Turkmenistan' :'TKM',
'Turks and Caicos Islands' : 'TCA',
'Tuvalu' : 'TUV',
'Uganda' : 'UGA',
'Ukraine' : 'UKR',
'United Arab Emirates' : 'ARE',
'United Kingdom' : 'GBR',
'United States' : 'USA',
'United States Minor Outlying Islands' : 'UMI',
'Uruguay' : 'URY',
'Uzbekistan' : 'UZB',
'Vanuatu' : 'VUT',
'Venezuela' : 'VEN',
'Vietnam' : 'VNM',
'Virgin Islands' : 'VIR',
'Virgin Islands (UK)' : 'VG',
'Virgin Islands (US)' : 'VI',
'Wake Island' : None,
'Wallis and Futuna' : 'WLF',
'West Bank' : None,
'Western Sahara' : 'ESH',
'Western Samoa' : 'WSM',
'Yemen' : 'YEM',
'Zaire' : None,
'Zambia' : 'ZMB',
'Zimbabwe' : 'ZWE',
'England' : 'GBR',
'Scotland' : 'GBR',
'Wales' : 'GBR',
'Northern Island' : 'GBR'
}

DIM_YEAR_LOOKUP = {
    'year' : list(range(1800,2201)),
    'year_id' : list(range(1,402))    
}

CONNECTION_STRING = "host=127.0.0.1 dbname=udacityprojectdb user=student password=6GNjBQvF"


