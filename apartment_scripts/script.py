import json
with open('apartment.json', 'r') as f:
    data = json.load(f)
print('-------------------------------------------')
for apartment in data:
    beds_value = apartment['beds']
    num_bedrooms = 0 if 'Studio' in beds_value else int(beds_value.split()[0])
    print(f"('{apartment['location']['fullAddress']}', {apartment['rent']['min']}, {num_bedrooms}, {apartment['coordinates']['latitude']}, {apartment['coordinates']['longitude']}),")
print('-------------------------------------------')