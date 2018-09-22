creds = Secret('impact_449961').get()

key1 = creds['key1']
key2 = creds['key2']

start = datetime.now() - timedelta(days=65)
end = datetime.now() - timedelta(days=1)

url = 'https://' + key1 + ':' + key2 + '@api.impactradius.com/Mediapartners/' + key1 + '/'
url += 'Reports/mp_performance_by_day?compareEnabled=false&timeRange=CUSTOM&START_DATE=' + start.strftime('%Y-%m-%d')
url += '&END_DATE=' + end.strftime('%Y-%m-%d')

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

all_data = []
for row in soup.findAll('record'):
    new = {}
    new['date'] = pd.to_datetime(row.find('date_display').get_text(), format='%b %d, %Y')
    new['clicks'] = int(row.find('clicks').get_text())
    new['calls'] = int(row.find('calls').get_text())
    new['actions'] = int(row.find('actions').get_text())
    new['sale_amount'] = float(row.find('sale_amount').get_text())
    new['action_cost'] = float(row.find('action_cost').get_text())
    new['total_cost'] = float(row.find('total_cost').get_text())
    new['epc'] = float(row.find('epc').get_text())
    all_data.append(new)
all_data = pd.DataFrame(all_data)

all_data['account_num'] = 449961
all_data['site'] = 'thesleepjudge.com'```
