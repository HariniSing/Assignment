import json
from collections import defaultdict

f = open('accounts.json')
data = json.load(f)
email_dict = defaultdict(list)

applications = {}
edges = set()

# Helper Methods


def get_applications(obj):
    if 'applications' in obj:
        return obj['applications']
    return [obj['application']]


def merge_objects(obj1, obj2):
    """
    Merges obj2 into obj1 and updates index in objects to point to obj1
    """
    if obj1['id'] == obj2['id']:
        return
    obj1['emails'] = list(set(obj1['emails'] + obj2['emails']))
    obj1['applications'] = list(
        set(get_applications(obj1) + get_applications(obj2)))
    applications[obj2['id']] = obj1


# adding id in our objects/dictionary entries
for i, j in enumerate(data):
    j['id'] = i
    applications[i] = j

# adding emails with their accounts in email_dict object/dictionary
for i in data:
    for j in i["emails"]:
        email_dict[j].append(i['id'])

# adding edges
for email, ids in email_dict.items():
    for index1 in range(len(ids)):
        for index2 in range(index1 + 1, len(ids)):
            edges.add((ids[index1], ids[index2]))

# now merge all the edges
for edge in edges:
    merge_objects(applications[edge[0]], applications[edge[1]])

final_items = []
for i in data:
    if i['id'] == applications[i['id']]['id']:
        final_items.append(i)

for i in final_items:
    i['applications'] = get_applications(i)
    del i['application']
    del i['id']
print(final_items)
