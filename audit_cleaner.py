# Author:   Priyesh Rajamohanan
# Date:     22 January 2017
# Desc:     To analyse audit data from JIRA server and summarize data.

import pandas as pd
pd.options.mode.chained_assignment = None


def print_summary(filename):
    date_from = '2016-08-01 00:00:00'
    date_to = '2016-09-30 23:59:59'
    raw_data = pd.read_csv(filename, header=0, index_col=0)
    # clean empty space from header
    raw_data_clean_header = raw_data.rename(columns=lambda x: x.replace(" ", ""))

    # filtering author and excluding avatar modifications
    filtered_data = raw_data_clean_header[(raw_data_clean_header.Author == 'ruth.lennon') &
                                          (raw_data_clean_header.Changesummary != 'Project avatar changed')]
    # converting column to datetime
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], dayfirst=True)

    # filtering date range - August to September
    filtered_data = filtered_data[(filtered_data['Date'] >= date_from) & (filtered_data['Date'] <= date_to)]

    # remove time part from date
    filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.date().strftime('%d/%m/%Y'))

    # printing summary
    print('Total minutes spent by Ruth Lennon in administering JIRA server between August and September 2016')
    print(filtered_data['Date'].value_counts())

print_summary("Data\\JAuditingExport2017_01_18.csv")
