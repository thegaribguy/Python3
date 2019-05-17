import sqlite3

conn = sqlite3.connect('spyder.sqlite')
cur = conn.cursor()

cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()

for row in cur:
	from_ids.append(row[0])

to_ids = list()
links = list()

cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
	from_id = row[0]
	to_id = row[1]
	if from_id == to_id : continue
	if from_id not in from_ids : continue
	if to_id not in from_ids : continue
	links.append(row)
	
	if to_id not in to_ids : to_ids.append(to_id)

prev_ranks = dict()
for node in from_ids:
	cur.execute('SELECT new_rank FROM Pages WHERE id = ?',(node,))
	row = cur.fetchone()
	prev_ranks[node] = row[0]

sval = input('How many iterations: ')
many = 1
if (len(sval)>0) : many = int(sval)

for i in range(many):
	next_ranks = dict()
	for (node,old_rank) in prev_ranks.items():
		next_ranks[node] = 0.0

	for (node,old_rank) in prev_ranks.items():
		give_ids = list()
		for (from_id, to_id) in links:
			if from_id != node : continue
			if to_id not in to_ids : continue
			give_ids.append(to_id)

			if (len(give_ids) < 1) : continue
			amt = old_rank/len(give_ids)

		for id in give_ids:
			next_ranks[id] = next_ranks[id] + amt

	prev_ranks = next_ranks

print(list(next_ranks.items())[:5])
cur.execute('UPDATE Pages SET old_rank= new_rank')
for (id,new_rank) in next_ranks.items():
	cur.execute('UPDATE Pages SET new_rank=? WHERE id=?',(new_rank,id))

conn.commit()
cur.close()
