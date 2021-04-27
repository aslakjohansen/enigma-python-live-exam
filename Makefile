TARGETS = \
	var/name.basics.tsv \
	var/title.akas.tsv \
	var/title.basics.tsv \
	var/title.crew.tsv \
	var/title.episode.tsv \
	var/title.principals.tsv \
	var/title.ratings.tsv \
	var/data/group_grades.json \

all: ${TARGETS}

var:
	mkdir var

var/data: var
	mkdir var/data

var/%.tsv.gz: var
	cd var ; wget https://datasets.imdbws.com/$*.tsv.gz

var/%.tsv: var/%.tsv.gz
	cd var ; gunzip $*.tsv.gz

var/data/group_grades.json: var/data
	cd var ; ./generate-fake-dataset.py

